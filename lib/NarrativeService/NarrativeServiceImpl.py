# -*- coding: utf-8 -*-
#BEGIN_HEADER
import time
import json
from biokbase.workspace.client import Workspace as workspaceService
from SetAPI.SetAPIClient import SetAPI
#END_HEADER


class NarrativeService:
    '''
    Module Name:
    NarrativeService

    Module Description:
    A KBase module: NarrativeService
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/rsutormin/NarrativeService"
    GIT_COMMIT_HASH = "aada7ed859d5f0e1f211f2585c809bdd16dde185"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        self.serviceWizardURL = config['service-wizard']
        self.SetAPI_version = config['setapi-version']
        #END_CONSTRUCTOR
        pass


    def list_objects_with_sets(self, ctx, params):
        """
        :param params: instance of type "ListObjectsWithSetsParams" ->
           structure: parameter "ws_name" of String, parameter "ws_id" of Long
        :returns: instance of type "ListObjectsWithSetsOutput" -> structure:
           parameter "data" of list of type "ListItem" (object_info -
           workspace info for object (including set object), set_items -
           optional property listing info for items of set object) ->
           structure: parameter "object_info" of type "object_info"
           (Information about an object, including user provided metadata.
           obj_id objid - the numerical id of the object. obj_name name - the
           name of the object. type_string type - the type of the object.
           timestamp save_date - the save date of the object. obj_ver ver -
           the version of the object. username saved_by - the user that saved
           or copied the object. ws_id wsid - the workspace containing the
           object. ws_name workspace - the workspace containing the object.
           string chsum - the md5 checksum of the object. int size - the size
           of the object in bytes. usermeta meta - arbitrary user-supplied
           metadata about the object.) -> tuple of size 11: parameter "objid"
           of Long, parameter "name" of String, parameter "type" of String,
           parameter "save_date" of type "timestamp" (A time in the format
           YYYY-MM-DDThh:mm:ssZ, where Z is either the character Z
           (representing the UTC timezone) or the difference in time to UTC
           in the format +/-HHMM, eg: 2012-12-17T23:24:06-0500 (EST time)
           2013-04-03T08:56:32+0000 (UTC time) 2013-04-03T08:56:32Z (UTC
           time)), parameter "version" of Long, parameter "saved_by" of
           String, parameter "wsid" of Long, parameter "workspace" of String,
           parameter "chsum" of String, parameter "size" of Long, parameter
           "meta" of mapping from String to String, parameter "set_items" of
           type "SetItems" -> structure: parameter "set_items_info" of list
           of type "object_info" (Information about an object, including user
           provided metadata. obj_id objid - the numerical id of the object.
           obj_name name - the name of the object. type_string type - the
           type of the object. timestamp save_date - the save date of the
           object. obj_ver ver - the version of the object. username saved_by
           - the user that saved or copied the object. ws_id wsid - the
           workspace containing the object. ws_name workspace - the workspace
           containing the object. string chsum - the md5 checksum of the
           object. int size - the size of the object in bytes. usermeta meta
           - arbitrary user-supplied metadata about the object.) -> tuple of
           size 11: parameter "objid" of Long, parameter "name" of String,
           parameter "type" of String, parameter "save_date" of type
           "timestamp" (A time in the format YYYY-MM-DDThh:mm:ssZ, where Z is
           either the character Z (representing the UTC timezone) or the
           difference in time to UTC in the format +/-HHMM, eg:
           2012-12-17T23:24:06-0500 (EST time) 2013-04-03T08:56:32+0000 (UTC
           time) 2013-04-03T08:56:32Z (UTC time)), parameter "version" of
           Long, parameter "saved_by" of String, parameter "wsid" of Long,
           parameter "workspace" of String, parameter "chsum" of String,
           parameter "size" of Long, parameter "meta" of mapping from String
           to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN list_objects_with_sets
        ws_id = params.get("ws_id", None)
        ws_name = params.get("ws_name", None)
        token = ctx["token"]
        ws = workspaceService(self.workspaceURL, token=token)
        ws_info = ws.get_workspace_info({"id": ws_id, "workspace": ws_name})
        if not ws_name:
            ws_name = ws_info[1]
        sapi = SetAPI(self.serviceWizardURL, token=token, service_ver=self.SetAPI_version)
        sets = sapi.list_sets({'workspace': ws_name, 'include_set_item_info': 1})['sets']
        ref_to_set = {}
        for set_info in sets:
            ref_to_set[set_info['ref']] = set_info
        max_obj_count = ws_info[4]
        ws_names = None
        ws_ids = None
        if "ws_id" in params:
            ws_ids = [ws_id]
        elif "ws_name" in params:
            ws_names = [ws_name]
        min_obj_id = 1
        data = []
        while min_obj_id <= max_obj_count:
            max_obj_id = min_obj_id + 10000 - 1
            part = ws.list_objects({"workspaces": ws_names, "ids": ws_ids, 
                                    "minObjectID": min_obj_id,
                                    "maxObjectID": max_obj_id})
            for info in part:
                item = {"object_info": info}
                item_ref = str(info[6]) + '/' + str(info[0]) + '/' + str(info[4])
                if item_ref in ref_to_set:
                    set_info = ref_to_set[item_ref]
                    target_set_items = []
                    for set_item in set_info['items']:
                        target_set_items.append(set_item['info'])
                    item['set_items'] = {'set_items_info': target_set_items}
                data.append(item)
            min_obj_id += 10000
        returnVal = {"data": data}
        #END list_objects_with_sets

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method list_objects_with_sets return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def copy_narrative(self, ctx, params):
        """
        :param params: instance of type "CopyNarrativeParams" (workspaceId -
           optional workspace ID, if not specified then property from
           workspaceRef object info is used.) -> structure: parameter
           "workspaceRef" of String, parameter "workspaceId" of Long,
           parameter "newName" of String
        :returns: instance of type "CopyNarrativeOutput" -> structure:
           parameter "newWsId" of Long, parameter "newNarId" of Long
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN copy_narrative
        newName = params['newName']
        workspaceRef = params['workspaceRef']
        user_id = ctx['user_id']
        time_ms = int(round(time.time() * 1000))
        newWsName = user_id + ':' + str(time_ms)
        # add the 'narrative' field to newWsMeta later.
        newWsMeta = {"is_temporary": "false", "narrative_nice_name": newName}
        token = ctx["token"]
        ws = workspaceService(self.workspaceURL, token=token)
        
        # start with getting the existing narrative object.
        currentNarrative = ws.get_objects([{'ref': workspaceRef}])[0]
        workspaceId = params.get('workspaceId', None)
        if not workspaceId:
            workspaceId = currentNarrative['info'][6]
        # clone the workspace EXCEPT for currentNarrative object:
        newWsId = ws.clone_workspace({'wsi': {'id': workspaceId}, 'workspace': newWsName,
                                      'meta': newWsMeta,
                                      'exclude': [{'objid': currentNarrative['info'][0]}]})[0]
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
            newNarInfo = ws.save_objects({'id': newWsId, 'objects': 
                                          [{'type': currentNarrative['info'][2],
                                            'data': currentNarrative['data'],
                                            'provenance': currentNarrative['provenance'],
                                            'name': currentNarrative['info'][1],
                                            'meta': newNarMetadata}]})
            # now, just update the workspace metadata to point
            # to the new narrative object
            newNarId = newNarInfo[0][0]
            ws.alter_workspace_metadata({'wsi': {'id': newWsId}, 
                                         'new': {'narrative': str(newNarId)}})
            returnVal = {'newWsId': newWsId, 'newNarId': newNarId}
        except:
            # let's delete copy of workspace so it's out of the way - it's broken
            ws.delete_workspace({'id': newWsId})
            raise # continue raising previous exception
        #END copy_narrative

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method copy_narrative return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def create_new_narrative(self, ctx, params):
        """
        :param params: instance of type "CreateNewNarrativeParams" (app -
           name of app (optional, either app or method may be defined) method
           - name of method (optional, either app or method may be defined)
           appparam - paramters of app/method packed into string in format:
           "step_pos,param_name,param_value(;...)*" (alternative to appData)
           appData - parameters of app/method in unpacked form (alternative
           to appparam) markdown - markdown text for cell of 'markdown' type
           (optional) copydata - packed inport data in format
           "import(;...)*") -> structure: parameter "app" of String,
           parameter "method" of String, parameter "appparam" of String,
           parameter "appData" of list of type "AppParam" -> tuple of size 3:
           parameter "step_pos" of String, parameter "key" of String,
           parameter "value" of String, parameter "markdown" of String,
           parameter "copydata" of String
        :returns: instance of type "CreateNewNarrativeOutput" -> structure:
           parameter "workspaceInfo" of type "WorkspaceInfo" (Restructured
           workspace info 'wsInfo' tuple: id: wsInfo[0], name: wsInfo[1],
           owner: wsInfo[2], moddate: wsInfo[3], object_count: wsInfo[4],
           user_permission: wsInfo[5], globalread: wsInfo[6], lockstat:
           wsInfo[7], metadata: wsInfo[8], modDate: no_timezone(wsInfo[3]))
           -> structure: parameter "id" of Long, parameter "name" of String,
           parameter "owner" of String, parameter "moddate" of type
           "timestamp" (A time in the format YYYY-MM-DDThh:mm:ssZ, where Z is
           either the character Z (representing the UTC timezone) or the
           difference in time to UTC in the format +/-HHMM, eg:
           2012-12-17T23:24:06-0500 (EST time) 2013-04-03T08:56:32+0000 (UTC
           time) 2013-04-03T08:56:32Z (UTC time)), parameter "object_count"
           of Long, parameter "user_permission" of type "permission"
           (Represents the permissions a user or users have to a workspace:
           'a' - administrator. All operations allowed. 'w' - read/write. 'r'
           - read. 'n' - no permissions.), parameter "globalread" of type
           "permission" (Represents the permissions a user or users have to a
           workspace: 'a' - administrator. All operations allowed. 'w' -
           read/write. 'r' - read. 'n' - no permissions.), parameter
           "lockstat" of type "lock_status" (The lock status of a workspace.
           One of 'unlocked', 'locked', or 'published'.), parameter
           "metadata" of mapping from String to String, parameter "modDate"
           of String, parameter "objectInfo" of type "ObjectInfo"
           (Restructured workspace object info 'data' tuple: id: data[0],
           name: data[1], type: data[2], save_date: data[3], version:
           data[4], saved_by: data[5], wsid: data[6], ws: data[7], checksum:
           data[8], size: data[9], metadata: data[10], ref: data[6] + '/' +
           data[0] + '/' + data[4], obj_id: 'ws.' + data[6] + '.obj.' +
           data[0], typeModule: type[0], typeName: type[1], typeMajorVersion:
           type[2], typeMinorVersion: type[3], saveDateNoTZ:
           no_timezone(data[3])) -> structure: parameter "id" of Long,
           parameter "name" of String, parameter "type" of String, parameter
           "save_date" of String, parameter "version" of Long, parameter
           "saved_by" of String, parameter "wsid" of Long, parameter "ws" of
           String, parameter "checksum" of String, parameter "size" of Long,
           parameter "metadata" of mapping from String to String, parameter
           "ref" of String, parameter "obj_id" of String, parameter
           "typeModule" of String, parameter "typeName" of String, parameter
           "typeMajorVersion" of String, parameter "typeMinorVersion" of
           String, parameter "saveDateNoTZ" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN create_new_narrative
        raise ValueError("Method is not supported yet")
        app = params.get('app', None)
        method = params.get('method', None)
        appparam = params.get('appparam', None)
        appData = params.get('appData', None)
        markdown = params.get('markdown', None)
        copydata = params.get('copydata', None)
        
        if app and method:
            raise ValueError("Must provide no more than one of the app or method params")
        if (not appData) and appparam:
            appData = []
            for tmpItem in appparam.split(';'):
                tmpTuple = tmpItem.split(',')
                step_pos = None
                if tmpItem[0]:
                    step_pos = int(tmpItem[0])
        # In progress...
        returnVal = None
        #END create_new_narrative

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method create_new_narrative return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
