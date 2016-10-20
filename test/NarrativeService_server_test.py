# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from NarrativeService.NarrativeServiceImpl import NarrativeService
from NarrativeService.NarrativeServiceServer import MethodContext
from SetAPI.SetAPIClient import SetAPI


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
        cls.wsClient = workspaceService(cls.wsURL, token=token)
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
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_list_object_with_sets(self):
        #t1 = time.time()
        #ret = self.getImpl().list_objects_with_sets(self.getContext(), 
        #                                            {"ws_name": "KBasePublicGenomesV5"})[0]["data"]
        #t1 = time.time() - t1
        #print("Return size: " + str(len(ret)) + ", time=" + str(t1))
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
        finally:
            # Cleaning up new created workspace
            ws.delete_workspace({'id': copy_ws_id})
