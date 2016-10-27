# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests

from os import environ
from NarrativeService.NarrativeManager import NarrativeManager
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from Workspace.WorkspaceClient import Workspace
from NarrativeService.NarrativeServiceImpl import NarrativeService
from NarrativeService.NarrativeServiceServer import MethodContext
from SetAPI.SetAPIClient import SetAPI
from NarrativeService.WorkspaceListObjectsIterator import WorkspaceListObjectsIterator


class NarrativeServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        user_id = requests.post(
            'https://kbase.us/services/authorization/Sessions/Login',
            data='token={}&fields=user_id'.format(token)).json()['user_id']
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'NarrativeService',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('NarrativeService'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.wsURL = cls.cfg['workspace-url']
        cls.serviceWizardURL = cls.cfg['service-wizard']
        cls.wsClient = Workspace(cls.wsURL, token=token)
        cls.serviceImpl = NarrativeService(cls.cfg)
        cls.SetAPI_version= cls.cfg['setapi-version']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_NarrativeService_" + str(suffix)
        self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_list_object_with_sets(self):
        reads_obj_ref = "KBaseExampleData/rhodobacter.art.q50.SE.reads"
        set_obj_name = "MyReadsSet.1"
        sapi = SetAPI(self.__class__.serviceWizardURL, token=self.getContext()['token'],
                      service_ver = self.__class__.SetAPI_version)
        sapi.save_reads_set_v1({'workspace': self.getWsName(), 'output_object_name': set_obj_name,
                                'data': {'description': '', 'items': [{'ref': reads_obj_ref}]}})
        ret = self.getImpl().list_objects_with_sets(self.getContext(), 
                                                    {"ws_name": self.getWsName()})[0]["data"]
        self.assertTrue(len(ret) > 0)
        set_count = 0
        for item in ret:
            self.assertTrue("object_info" in item)
            if "set_items" in item:
                set_count += 1
                set_items = item["set_items"]["set_items_info"]
                self.assertEqual(1, len(set_items))
        self.assertEqual(1, set_count)
        ws_id = self.getWsClient().get_workspace_info({"workspace": self.getWsName()})[0]
        ret2 = self.getImpl().list_objects_with_sets(self.getContext(),
                                                    {"ws_id": ws_id})[0]["data"]
        self.assertEqual(len(ret), len(ret2))
        type_filter = "KBaseSets.ReadsSet"
        ret3 = self.getImpl().list_objects_with_sets(self.getContext(),
                                                    {"types": [type_filter],
                                                     "workspaces": [str(ws_id)]})[0]["data"]
        self.assertTrue(len(ret3) > 0)
        for item in ret3:
            info = item['object_info']
            obj_type = info[2].split('-')[0]
            self.assertEqual(type_filter, obj_type)

    def test_copy_narrative(self):
        ws = self.getWsClient()
        with open("/kb/module/test/data/narrative1.json", "r") as f1:
            nar_obj_data = json.load(f1)
        user_id = self.getContext()['user_id']
        ws_name = self.getWsName()
        nar_obj_data['metadata']['creator'] = user_id
        nar_obj_data['metadata']['ws_name'] = ws_name
        nar_obj_data['metadata']['kbase']['creator'] = user_id
        nar_obj_data['metadata']['kbase']['ws_name'] = ws_name
        nar_obj_name = "Narrative." + str(int(round(time.time() * 1000))) 
        nar_obj_type = "KBaseNarrative.Narrative-4.0"
        job_info = json.dumps({"queue_time": 0, "running": 0, "completed": 0, 
                               "run_time": 0, "error": 0})
        nar_obj_meta = {"description": "", 
                        "format": "ipynb", 
                        "creator": user_id, 
                        "job_info": job_info, 
                        "data_dependencies": "[]", 
                        "jupyter.markdown": "1", 
                        "ws_name": ws_name, 
                        "type": "KBaseNarrative.Narrative", 
                        "name": "NarrativeCopyTest"}
        ws.save_objects({'workspace': ws_name, 'objects': 
                         [{'type': nar_obj_type,
                           'data': nar_obj_data,
                           'name': nar_obj_name,
                           'meta': nar_obj_meta}]})
        # Adding DP object:
        reads_ref = "KBaseExampleData/rhodobacter.art.q50.SE.reads"
        target_reads_name = "MyReads.copy.1"
        reads_info = ws.copy_object({'from': {'ref': reads_ref},
                                     'to': {'workspace': self.getWsName(),
                                            'name': target_reads_name}})
        copy_nar_name = "NarrativeCopyTest - Copy"
        ret = self.getImpl().copy_narrative(self.getContext(), 
                                            {'workspaceRef': ws_name + '/' + nar_obj_name,
                                             'newName': copy_nar_name})[0]
        copy_ws_id = ret['newWsId']
        copy_nar_id = ret['newNarId']
        try:
            copy_nar = ws.get_objects([{'ref': str(copy_ws_id) + '/' + str(copy_nar_id)}])[0]
            #print("Copy object: " + json.dumps(copy_nar, indent=4, sort_keys=True))
            copy_nar_data = copy_nar['data']
            # This is weird, so ws_name is the same as for old narrative:
            self.assertEqual(ws_name, copy_nar_data['metadata']['kbase']['ws_name'])
            # And here is proper new ws_name:
            self.assertNotEqual(ws_name, copy_nar_data['metadata']['ws_name'])
            self.assertEqual(copy_nar_name, copy_nar_data['metadata']['name'])
            ret = self.getImpl().list_objects_with_sets(self.getContext(), 
                                                        {"ws_id": copy_ws_id})[0]["data"]
            dp_found = False
            for item in ret:
                obj_info = item["object_info"]
                if obj_info[7] == self.getWsName():
                    self.assertEqual(target_reads_name, obj_info[1])
                    self.assertTrue('dp_info' in item)
                    self.assertEqual(reads_info[6], obj_info[6])
                    self.assertEqual(reads_info[0], obj_info[0])
                    dp_found = True
                else:
                    object_type = obj_info[2].split('-')[0]
                    self.assertTrue(object_type != "KBaseFile.SingleEndLibrary", 
                                    "Unexpected type: " + object_type)
            self.assertTrue(dp_found)
        finally:
            # Cleaning up new created workspace
            ws.delete_workspace({'id': copy_ws_id})
        #################################################################################
        # Now it's copy with refs in DataPalette
        reads_ws_name = "KBaseExampleData"
        reads_obj_name = "rhodobacter.art.q50.SE.reads"
        reads_ref = reads_ws_name + '/' + reads_obj_name
        # This reads object should appear in Narrative copy as well:
        self.getImpl().copy_object(self.getContext(), {'ref': reads_ref,
                                                       'target_ws_name': ws_name})
        copy_nar_name = "NarrativeCopyTest - Copy2"
        ret = self.getImpl().copy_narrative(self.getContext(), 
                                            {'workspaceRef': ws_name + '/' + nar_obj_name,
                                             'newName': copy_nar_name})[0]
        copy_ws_id = ret['newWsId']
        try:
            ret = self.getImpl().list_objects_with_sets(self.getContext(), 
                                                        {"ws_id": copy_ws_id})[0]["data"]
            dp_found = False
            for item in ret:
                obj_info = item["object_info"]
                if obj_info[7] == reads_ws_name:
                    self.assertTrue('dp_info' in item)
                    self.assertEqual(reads_obj_name, obj_info[1])
                    dp_found = True
            self.assertTrue(dp_found)
        finally:
            # Cleaning up new created workspace
            ws.delete_workspace({'id': copy_ws_id})


    def test_create_new_narrative(self):
        import_ref = "KBaseExampleData/rhodobacter.art.q50.SE.reads"
        ws = self.getWsClient()
        ret = self.getImpl().create_new_narrative(self.getContext(), 
                                                  {"method": "AssemblyUtil/import_assembly_fasta_ftp",
                                                   "appparam": "0,param1,value1;0,param2,value2",
                                                   "copydata": import_ref})[0]
        try:
            self.assertTrue('narrativeInfo' in ret)
        finally:
            new_ws_id = ret['workspaceInfo']['id']
            ws.delete_workspace({'id': new_ws_id})

    def test_copy_object(self):
        # Reads
        example_ws = "KBaseExampleData"
        import_ref = example_ws + "/rhodobacter.art.q50.SE.reads"
        ret = self.getImpl().copy_object(self.getContext(), {'ref': import_ref, 
                                                             'target_ws_name': self.getWsName()})
        self.assertEqual(example_ws, ret[0]['info']['ws'])
        # Let's check that we see reads copy in list_objects_with_sets
        ret = self.getImpl().list_objects_with_sets(self.getContext(), 
                                                    {"ws_name": self.getWsName()})[0]["data"]
        found = False
        for item in ret:
            obj_info = item["object_info"]
            if obj_info[7] == example_ws:
                self.assertTrue('dp_info' in item)
                found = True
        self.assertTrue(found)
        # Genome
        import_ref = example_ws + "/Rhodobacter_CACIA_14H1"
        target_name = "MyGenome.1"
        ret = self.getImpl().copy_object(self.getContext(), {'ref': import_ref, 
                                                             'target_ws_name': self.getWsName(),
                                                             'target_name': target_name})
        self.assertEqual(target_name, ret[0]['info']['name'])

    def test_workspace_list_objects_iterator(self):
        #ws_name = "KBasePublicGenomesV5"
        #part_size = 10000
        ws_name = "KBaseExampleData"
        part_size = 10
        ws_info = self.getWsClient().get_workspace_info({'workspace': ws_name})
        max_obj_count = ws_info[4]
        min_obj_id = 1
        obj_count = 0
        while min_obj_id <= max_obj_count:
            max_obj_id = min_obj_id + 10000 - 1
            part = self.getWsClient().list_objects({'workspaces': [ws_name], 
                                                    'minObjectID': min_obj_id,
                                                    'maxObjectID': max_obj_id})
            obj_count += len(part)
            min_obj_id += 10000
        obj_count2 = 0
        for info in WorkspaceListObjectsIterator(self.getWsClient(), ws_info_list=[ws_info],
                                                 part_size=part_size):
            self.assertEqual(11, len(info))
            obj_count2 += 1
        self.assertEqual(obj_count, obj_count2)

    def test_list_available_types(self):
        ws_name = "KBaseExampleData"
        type_stat = self.getImpl().list_available_types(self.getContext(),
                                                        {"workspaces": [ws_name]})[0]['type_stat']
        self.assertTrue("KBaseGenomes.Genome" in type_stat)
        self.assertTrue("KBaseFile.SingleEndLibrary" in type_stat)

    def test_bulk_list(self):
        NarrativeManager.DEBUG = False  #True
        try:
            ids = []
            for ws_info in self.getWsClient().list_workspace_info({'perm': 'r', 'excludeGlobal': 1}):
                if ws_info[4] < 1000:
                    ids.append(str(ws_info[0]))
                    if len(ids) >= 100:
                        break
            print("Workspaces selected for bulk list_objects_with_sets: " + str(len(ids)))
            t1 = time.time()
            ret = self.getImpl().list_objects_with_sets(self.getContext(), {'workspaces': ids})[0]["data"]
            print("Objects found: " + str(len(ret)) + ", time=" + str(time.time() - t1))
        finally:
            NarrativeManager.DEBUG = False
