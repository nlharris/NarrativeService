import time
import json
import uuid
from Workspace.WorkspaceClient import Workspace
from NarrativeService.ServiceUtils import ServiceUtils
from NarrativeMethodStore.NarrativeMethodStoreClient import NarrativeMethodStore

# Migration to python of JavaScript class from https://github.com/kbase/kbase-ui/blob/4d31151d13de0278765a69b2b09f3bcf0e832409/src/client/modules/plugins/narrativemanager/modules/narrativeManager.js#L414

class NarrativeManager:
    
    KB_CELL = 'kb-cell'
    KB_TYPE = 'type'
    KB_APP_CELL = 'kb_app'
    KB_FUNCTION_CELL = 'function_input'
    KB_OUTPUT_CELL = 'function_output'
    KB_ERROR_CELL = 'kb_error'
    KB_CODE_CELL = 'kb_code'
    KB_STATE = 'widget_state'
    
    def __init__(self, workspaceURL, narrativeMethodStoreURL, token, user_id):
        self.workspaceURL = workspaceURL
        self.narrativeMethodStoreURL = narrativeMethodStoreURL
        self.token = token
        self.user_id = user_id
        self.ws = Workspace(self.workspaceURL, token=self.token)
        self.nms = NarrativeMethodStore(self.narrativeMethodStoreURL, token=self.token)
        #self.nms = 

    def create_temp_narrative(self, cells, parameters, importData):
        narr_id = int(round(time.time() * 1000))
        workspaceName = self.user_id + ':' + str(narr_id)
        narrativeName = "Narrative." + str(narr_id)
        
        ws = self.ws
        ws_info = ws.create_workspace({'workspace': workspaceName, 'description': ''})
        newWorkspaceInfo = ServiceUtils.workspaceInfoToObject(ws_info)
        [narrativeObject, metadataExternal] = self.fetchNarrativeObjects(workspaceName, cells, 
                                                                         parameters)
        objectInfo = ws.save_objects({'workspace': workspaceName,
                                      'objects': [{'type': 'KBaseNarrative.Narrative',
                                                   'data': narrativeObject,
                                                   'name': narrativeName,
                                                   'meta': metadataExternal,
                                                   'provenance': [{'script': 'NarrativeManager.py',
                                                                   'description': 'Created new ' +
                                                                   'Workspace/Narrative bundle.'}],
                                                   'hidden': 0}]})[0]
        objectInfo = ServiceUtils.objectInfoToObject(objectInfo)
        self.completeNewNarrative(newWorkspaceInfo['id'], objectInfo['id'], importData)
        return {'workspaceInfo': newWorkspaceInfo, 'narrativeInfo': objectInfo}

    def fetchNarrativeObjects(self, workspaceName, cells, parameters):
        if not cells:
            cells = []
        # fetchSpecs
        appSpecIds = []
        methodSpecIds = []
        specMapping = {'apps': {}, 'methods': {}}
        for cell in cells:
            if 'app' in cell:
                appSpecIds.append(cell['app'])
            elif 'method' in cell:
                methodSpecIds.append(cell['method'])
        if len(appSpecIds) > 0:
            appSpecs = self.nms.get_app_spec({'ids': appSpecIds})
            for spec in appSpecs:
                spec_id = spec['info']['id']
                specMapping['apps'][spec_id] = spec
        if len(methodSpecIds) > 0:
            methodSpecs = self.nms.get_method_spec({'ids': methodSpecIds})
            for spec in methodSpecs:
                spec_id = spec['info']['id']
                specMapping['methods'][spec_id] = spec
        # end of fetchSpecs
        metadata = {'job_ids': {'methods': [], 
                                'apps': [], 
                                'job_usage': {'queue_time': 0, 'run_time': 0}},
                    'format': 'ipynb',
                    'creator': self.user_id,
                    'ws_name': workspaceName,
                    'name': 'Untitled',
                    'type': 'KBaseNarrative.Narrative',
                    'description': '',
                    'data_dependencies': []}
        cellData = self.gatherCellData(cells, specMapping, parameters)
        narrativeObject = {'nbformat_minor': 0,
                           'cells': cellData,
                           'metadata': metadata,
                           'nbformat': 4}
        metadataExternal = {}
        for key in metadata:
            value = metadata[key]
            if isinstance(value, basestring):
                metadataExternal[key] = value
            else:
                metadataExternal[key] = json.dumps(value)
        return [narrativeObject, metadataExternal]

    def gatherCellData(self, cells, specMapping, parameters):
        cell_data = []
        for cell_pos, cell in enumerate(cells):
            if 'app' in cell:
                cell_data.append(self.buildAppCell(len(cell_data), 
                                                   specMapping['apps'][cell['app']],
                                                   parameters))
            elif 'method' in cell:
                cell_data.append(self.buildMethodCell(len(cell_data), 
                                                      specMapping['methods'][cell['method']], 
                                                      parameters))
            elif 'merkdown' in cell:
                cell_data.append({'cell_type': 'markdown', 'source': cell['markdown'], 
                                  'metadata': {}})
            else:
                raise ValueError("cannot add cell #" + str(cell_pos) + 
                                 ", unrecognized cell content")
        return cell_data

    def buildAppCell(self, pos, spec, params):
        cellId = 'kb-cell-' + str(pos) + '-' + str(uuid.uuid4())
        cell = {'cell_type': 'markdown',
                'source': "<div id='" + cellId + "'></div>" +
                    "\n<script>" +
                    "$('#" + cellId + "').kbaseNarrativeAppCell({'appSpec' : '" + 
                    self.safeJSONStringify(spec) + "', 'cellId' : '" + cellId + "'});" +
                    "</script>",
                'metadata': {}}
        cellInfo = {}
        widgetState = []
        cellInfo[self.KB_TYPE] = self.KB_APP_CELL;
        cellInfo['app'] = spec;
        if params:
            steps = {};
            for param in params:
                stepid = 'step_' + str(param[0])
                if stepid not in steps:
                    steps[stepid] = {}
                    steps[stepid]['inputState'] = {}
                steps[stepid]['inputState'][param[1]] = param[2]
            state = {'state': {'step': steps}};
            widgetState.append(state);
        cellInfo[self.KB_STATE] = widgetState;
        cell['metadata'][self.KB_CELL] = cellInfo;
        return cell

    def buildMethodCell(self, pos, spec, params):
        cellId = 'kb-cell-' + str(pos) + '-' + str(uuid.uuid4())
        cell = {'cell_type': 'markdown',
                'source': "<div id='" + cellId + "'></div>" +
                    "\n<script>" +
                    "$('#" + cellId + "').kbaseNarrativeMethodCell({'method' : '" + 
                    self.safeJSONStringify(spec) + "'});" +
                    "</script>",
                'metadata': {}}
        cellInfo = {'method': spec,
                    'widget': spec['widgets']['input']}
        cellInfo[self.KB_TYPE] = self.KB_FUNCTION_CELL
        widgetState = []
        if params:
            wparams = {}
            for param in params:
                wparams[param[1]] = param[2];
            widgetState.append({'state': wparams});
        cellInfo[self.KB_STATE] = widgetState;
        cell['metadata'][self.KB_CELL] = cellInfo;
        return cell

    def completeNewNarrative(self, workspaceId, objectId, importData):
        self.ws.alter_workspace_metadata({'wsi': {'id': workspaceId},
                                          'new': {'narrative': str(objectId), 
                                                  'is_temporary': 'true'}})
        # copy_to_narrative:
        if not importData:
            return
        objectsToCopy = [{'ref': x} for x in importData]
        infoList = self.ws.get_object_info_new({'objects': objectsToCopy, 'includeMetadata': 0})
        for item in infoList:
            objectInfo = ServiceUtils.objectInfoToObject(item)
            self.ws.copy_object({'from': {'ref': objectInfo['ref']}, #!! assume same ordering
                                 'to': {'wsid': workspaceId, 'name': objectInfo['name']}})

    def safeJSONStringify(self, obj):
        return json.dumps(self.safeJSONStringifyPrepare(obj))
        
    def safeJSONStringifyPrepare(self, obj):
        if isinstance(obj, basestring):
            return obj.replace("'", "&apos;").replace('"', "&quot;")
        elif isinstance(obj, list):
            for pos in range(len(obj)):
                obj[pos] = self.safeJSONStringifyPrepare(obj[pos])
        elif isinstance(obj, dict):
            obj_keys = list(obj.keys())
            for key in obj_keys:
                obj[key] = self.safeJSONStringifyPrepare(obj[key])
        else:
            pass # it's boolean/int/float/None
        return obj
