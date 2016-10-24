import time
import json
import uuid
from NarrativeService.ServiceUtils import ServiceUtils
from NarrativeService.DataPaletteTypes import DataPaletteTypes

from Workspace.WorkspaceClient import Workspace
from NarrativeMethodStore.NarrativeMethodStoreClient import NarrativeMethodStore
from SetAPI.SetAPIClient import SetAPI
from DataPaletteService.DataPaletteServiceClient import DataPaletteService


class NarrativeManager:
    
    KB_CELL = 'kb-cell'
    KB_TYPE = 'type'
    KB_APP_CELL = 'kb_app'
    KB_FUNCTION_CELL = 'function_input'
    KB_OUTPUT_CELL = 'function_output'
    KB_ERROR_CELL = 'kb_error'
    KB_CODE_CELL = 'kb_code'
    KB_STATE = 'widget_state'
    
    DATA_PALETTES_TYPES = DataPaletteTypes()
    
    def __init__(self, config, ctx):
        self.workspaceURL = config['workspace-url']
        self.serviceWizardURL = config['service-wizard']
        self.narrativeMethodStoreURL = config['narrative-method-store']
        self.SetAPI_version = config['setapi-version']
        self.DataPaletteService_version = config['datapaletteservice-version']
        self.token = ctx["token"]
        self.user_id = ctx["user_id"]
        self.ws = Workspace(self.workspaceURL, token=self.token)

    def list_objects_with_sets(self, ws_id, ws_name):
        ws_info = self.ws.get_workspace_info({"id": ws_id, "workspace": ws_name})
        if not ws_name:
            ws_name = ws_info[1]
        data = []
        sapi = SetAPI(self.serviceWizardURL, token=self.token, service_ver=self.SetAPI_version)
        sets = sapi.list_sets({'workspace': ws_name, 'include_set_item_info': 1})['sets']
        processed_set_refs = {}
        for set_info in sets:
            # Process
            target_set_items = []
            for set_item in set_info['items']:
                target_set_items.append(set_item['info'])
            data.append({'object_info': set_info['info'], 
                         'set_items': {'set_items_info': target_set_items}})
            processed_set_refs[set_info['ref']] = True
        max_obj_count = ws_info[4]
        ws_names = [ws_name]
        min_obj_id = 1
        while min_obj_id <= max_obj_count:
            max_obj_id = min_obj_id + 10000 - 1
            part = self.ws.list_objects({"workspaces": ws_names, 
                                         "minObjectID": min_obj_id,
                                         "maxObjectID": max_obj_id})
            for info in part:
                item_ref = str(info[6]) + '/' + str(info[0]) + '/' + str(info[4])
                if item_ref not in processed_set_refs:
                    data.append({'object_info': info})
            min_obj_id += 10000
        dps = DataPaletteService(self.serviceWizardURL, token=self.token, 
                                 service_ver=self.DataPaletteService_version)
        dp_ret = dps.list_data({'workspaces': [self._get_workspace_name_or_id(ws_id, ws_name)]})
        list_objects_input = []
        dp_ref_to_info = {}
        for item in dp_ret['data']:
            ref = item['ref']
            if ref not in processed_set_refs:
                list_objects_input.append({'ref': ref})
                dp_ref_to_info[ref] = item
        infoList = self.ws.get_object_info_new({'objects': list_objects_input, 
                                                'includeMetadata': 0})
        for info in infoList:
            ref = str(info[6]) + '/' + str(info[0]) + '/' + str(info[4])
            dp_info = dp_ref_to_info[ref]
            data.append({'object_info': info, 'dp_info': {'meta': dp_info.get('meta'),
                                                          'src_nar': dp_info.get('src_nar')}})
        return {"data": data}

    def copy_narrative(self, newName, workspaceRef, workspaceId):
        time_ms = int(round(time.time() * 1000))
        newWsName = self.user_id + ':' + str(time_ms)
        # add the 'narrative' field to newWsMeta later.
        newWsMeta = {"is_temporary": "false", "narrative_nice_name": newName}
        
        # start with getting the existing narrative object.
        currentNarrative = self.ws.get_objects([{'ref': workspaceRef}])[0]
        if not workspaceId:
            workspaceId = currentNarrative['info'][6]
        # Let's prepare exceptions for clone the workspace. 
        # 1) currentNarrative object:
        exclude_list = [{'objid': currentNarrative['info'][0]}]
        # 2) let's exclude objects of types under DataPalette handling:
        dp_types = self.DATA_PALETTES_TYPES.keys()
        ws_info = self.ws.get_workspace_info({"id": workspaceId})
        max_obj_count = ws_info[4]
        add_to_palette_list = []
        for dp_type in dp_types:
            min_obj_id = 1
            while min_obj_id <= max_obj_count:
                max_obj_id = min_obj_id + 10000 - 1
                part = self.ws.list_objects({"ids": [workspaceId],
                                             "type": dp_type, 
                                             "minObjectID": min_obj_id,
                                             "maxObjectID": max_obj_id})
                for info in part:
                    add_to_palette_list.append({'ref': str(info[6]) + '/' + str(info[0]) + '/' +
                                                str(info[4])})
                    exclude_list.append({'objid': info[0]})
                min_obj_id += 10000
        # clone the workspace EXCEPT for currentNarrative object + obejcts of DataPalette types:
        newWsId = self.ws.clone_workspace({'wsi': {'id': workspaceId}, 'workspace': newWsName,
                                           'meta': newWsMeta, 'exclude': exclude_list})[0]
        if len(add_to_palette_list) > 0:
            dps = DataPaletteService(self.serviceWizardURL, token=self.token, 
                                     service_ver=self.DataPaletteService_version)
            dps.add_to_palette({'workspace': str(newWsId), 'new_refs': add_to_palette_list})

        try:
            # update the ref inside the narrative object and the new workspace metadata.
            newNarMetadata = currentNarrative['info'][10]
            newNarMetadata['name'] = newName
            newNarMetadata['ws_name'] = newWsName
            newNarMetadata['job_info'] = json.dumps({'queue_time': 0, 'running': 0, 
                                                     'completed': 0, 'run_time': 0, 'error': 0})
            
            currentNarrative['data']['metadata']['name'] = newName
            currentNarrative['data']['metadata']['ws_name'] = newWsName
            currentNarrative['data']['metadata']['job_ids'] = {'apps': [], 'methods': [], 
                                                               'job_usage': {'queue_time': 0, 
                                                                             'run_time': 0}}
            # save the shiny new Narrative so it's at version 1
            newNarInfo = self.ws.save_objects({'id': newWsId, 'objects': 
                                               [{'type': currentNarrative['info'][2],
                                                 'data': currentNarrative['data'],
                                                 'provenance': currentNarrative['provenance'],
                                                 'name': currentNarrative['info'][1],
                                                 'meta': newNarMetadata}]})
            # now, just update the workspace metadata to point
            # to the new narrative object
            newNarId = newNarInfo[0][0]
            self.ws.alter_workspace_metadata({'wsi': {'id': newWsId}, 
                                              'new': {'narrative': str(newNarId)}})
            return {'newWsId': newWsId, 'newNarId': newNarId}
        except:
            # let's delete copy of workspace so it's out of the way - it's broken
            self.ws.delete_workspace({'id': newWsId})
            raise # continue raising previous exception

    def create_new_narrative(self, app, method, appparam, appData, markdown, copydata, importData):
        if app and method:
            raise ValueError("Must provide no more than one of the app or method params")
        
        if (not importData) and copydata:
            importData = copydata.split(';')
        
        if (not appData) and appparam:
            appData = []
            for tmp_item in appparam.split(';'):
                tmp_tuple = tmp_item.split(',')
                step_pos = None
                if tmp_tuple[0]:
                    try:
                        step_pos = int(tmp_tuple[0])
                    except ValueError:
                        pass
                appData.append([step_pos, tmp_tuple[1], tmp_tuple[2]])
        cells = None
        if app:
            cells = [{"app": app}]
        elif method:
            cells = [{"method": method}]
        elif markdown:
            cells = [{"markdown": markdown}]
        return self._create_temp_narrative(cells, appData, importData)

    def _create_temp_narrative(self, cells, parameters, importData):
        # Migration to python of JavaScript class from https://github.com/kbase/kbase-ui/blob/4d31151d13de0278765a69b2b09f3bcf0e832409/src/client/modules/plugins/narrativemanager/modules/narrativeManager.js#L414
        narr_id = int(round(time.time() * 1000))
        workspaceName = self.user_id + ':' + str(narr_id)
        narrativeName = "Narrative." + str(narr_id)
        
        ws = self.ws
        ws_info = ws.create_workspace({'workspace': workspaceName, 'description': ''})
        newWorkspaceInfo = ServiceUtils.workspaceInfoToObject(ws_info)
        [narrativeObject, metadataExternal] = self._fetchNarrativeObjects(workspaceName, cells, 
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
        self._completeNewNarrative(newWorkspaceInfo['id'], objectInfo['id'], importData)
        return {'workspaceInfo': newWorkspaceInfo, 'narrativeInfo': objectInfo}

    def _fetchNarrativeObjects(self, workspaceName, cells, parameters):
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
        nms = NarrativeMethodStore(self.narrativeMethodStoreURL, token=self.token)
        if len(appSpecIds) > 0:
            appSpecs = nms.get_app_spec({'ids': appSpecIds})
            for spec in appSpecs:
                spec_id = spec['info']['id']
                specMapping['apps'][spec_id] = spec
        if len(methodSpecIds) > 0:
            methodSpecs = nms.get_method_spec({'ids': methodSpecIds})
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
        cellData = self._gatherCellData(cells, specMapping, parameters)
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

    def _gatherCellData(self, cells, specMapping, parameters):
        cell_data = []
        for cell_pos, cell in enumerate(cells):
            if 'app' in cell:
                cell_data.append(self._buildAppCell(len(cell_data), 
                                                   specMapping['apps'][cell['app']],
                                                   parameters))
            elif 'method' in cell:
                cell_data.append(self._buildMethodCell(len(cell_data), 
                                                      specMapping['methods'][cell['method']], 
                                                      parameters))
            elif 'merkdown' in cell:
                cell_data.append({'cell_type': 'markdown', 'source': cell['markdown'], 
                                  'metadata': {}})
            else:
                raise ValueError("cannot add cell #" + str(cell_pos) + 
                                 ", unrecognized cell content")
        return cell_data

    def _buildAppCell(self, pos, spec, params):
        cellId = 'kb-cell-' + str(pos) + '-' + str(uuid.uuid4())
        cell = {'cell_type': 'markdown',
                'source': "<div id='" + cellId + "'></div>" +
                    "\n<script>" +
                    "$('#" + cellId + "').kbaseNarrativeAppCell({'appSpec' : '" + 
                    self._safeJSONStringify(spec) + "', 'cellId' : '" + cellId + "'});" +
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

    def _buildMethodCell(self, pos, spec, params):
        cellId = 'kb-cell-' + str(pos) + '-' + str(uuid.uuid4())
        cell = {'cell_type': 'markdown',
                'source': "<div id='" + cellId + "'></div>" +
                    "\n<script>" +
                    "$('#" + cellId + "').kbaseNarrativeMethodCell({'method' : '" + 
                    self._safeJSONStringify(spec) + "'});" +
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

    def _completeNewNarrative(self, workspaceId, objectId, importData):
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
            self.copy_object(objectInfo['ref'], workspaceId, None, None, objectInfo)

    def _safeJSONStringify(self, obj):
        return json.dumps(self._safeJSONStringifyPrepare(obj))
        
    def _safeJSONStringifyPrepare(self, obj):
        if isinstance(obj, basestring):
            return obj.replace("'", "&apos;").replace('"', "&quot;")
        elif isinstance(obj, list):
            for pos in range(len(obj)):
                obj[pos] = self._safeJSONStringifyPrepare(obj[pos])
        elif isinstance(obj, dict):
            obj_keys = list(obj.keys())
            for key in obj_keys:
                obj[key] = self._safeJSONStringifyPrepare(obj[key])
        else:
            pass # it's boolean/int/float/None
        return obj

    def _get_workspace_name_or_id(self, ws_id, ws_name):
        ret = ws_name
        if not ret:
            ret = str(ws_id)
        return ret

    def copy_object(self, ref, target_ws_id, target_ws_name, target_name, src_info):
        # There should be some logic related to DataPalettes
        if (not target_ws_id) and (not target_ws_name):
            raise ValueError("Neither target workspace ID nor name is defined")
        if not src_info:
            src_info_tuple = self.ws.get_object_info_new({'objects': [{'ref': ref}], 
                                                          'includeMetadata': 0})[0]
            src_info = ServiceUtils.objectInfoToObject(src_info_tuple)
        type_name = src_info['typeModule'] + '.' + src_info['typeName']
        type_config = self.DATA_PALETTES_TYPES.get(type_name)
        if type_config is not None:
            # Copy with DataPaletteService
            if target_name:
                raise ValueError("'target_name' cannot be defined for DataPalette copy")
            dps = DataPaletteService(self.serviceWizardURL, token=self.token, 
                                     service_ver=self.DataPaletteService_version)
            target_ws_name_or_id = self._get_workspace_name_or_id(target_ws_id, target_ws_name)
            dps.add_to_palette({'workspace': target_ws_name_or_id, 'new_refs': [{'ref': ref}]})
            return {'info': src_info}
        else:
            if not target_name:
                target_name = src_info['name']
            obj_info_tuple = self.ws.copy_object({'from': {'ref': ref},
                                                  'to': {'wsid': target_ws_id,
                                                         'workspace': target_ws_name,
                                                         'name': target_name}})
            obj_info = ServiceUtils.objectInfoToObject(obj_info_tuple)
            return {'info': obj_info}
