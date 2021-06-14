# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:18:34 2016

@author: okada

"""

import unittest
import subprocess
import os
import otomo.analysis_status

cur = os.path.dirname(__file__)
samples1 = cur + "/samples1.json"
samples2 = cur + "/samples2.json"
output_dir = cur + "/../temp"
qacct = cur + "/qacct.txt"
quota = cur + "/quota.txt"

class OtomoTest(unittest.TestCase):
    # init class
    @classmethod
    def setUpClass(self):
        pass

    # terminated class
    @classmethod
    def tearDownClass(self):
        pass

    # init method
    def setUp(self):
        pass

    # terminated method
    def tearDown(self):
        pass
    
    def test_01_version(self):
        subprocess.check_call(['otomo', '--version'])
    
    def test_02_local(self):
        #  setup
        subprocess.check_call(("otomo setup --wdir %s" % (output_dir)), shell=True)
        subprocess.check_call(("otomo regsample --samples %s" % (samples1)), shell=True)
        subprocess.check_call(("otomo regsample --samples %s" % (samples2)), shell=True)
        
        ret_sample = otomo.analysis_status.get_sample_w_status("init")
        self.assertEqual (len(ret_sample), 120)
        
        # set status
        otomo.analysis_status.set_status_w_sample("SRP219151_SRR10015386", "analysis_failure")
        otomo.analysis_status.set_status_w_sample("SRP219151_SRR10015394", "analysis_failure")
        ret_sample = otomo.analysis_status.get_sample_w_status("analysis_failure")
        self.assertEqual (ret_sample, ["SRP219151_SRR10015386", "SRP219151_SRR10015394"])

        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015388 --status success", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015390 --status success", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015392 --status success", shell=True)
        ret_sample = otomo.analysis_status.get_sample_w_status("success")
        self.assertEqual (ret_sample, ["SRP219151_SRR10015388","SRP219151_SRR10015390", "SRP219151_SRR10015392"])

        ret_sample = otomo.analysis_status.get_sample_count_g_status()
        self.assertEqual (ret_sample["init"], 115)
        self.assertEqual (ret_sample["success"], 3)
        self.assertEqual (ret_sample["analysis_failure"], 2)

        # reduction
        os.makedirs("%s/fastq/%s" % (output_dir, "SRP219151_SRR10015386"), exist_ok = True)
        os.makedirs("%s/star/%s" % (output_dir, "SRP219151_SRR10015386"), exist_ok = True)
        os.makedirs("%s/expression/%s" % (output_dir, "SRP219151_SRR10015386"), exist_ok = True)
        os.makedirs("%s/ir_count/%s" % (output_dir, "SRP219151_SRR10015386"), exist_ok = True)
        os.makedirs("%s/iravnet/%s" % (output_dir, "SRP219151_SRR10015386"), exist_ok = True)
        os.makedirs("%s/juncmut/%s" % (output_dir, "SRP219151_SRR10015386"), exist_ok = True)
        subprocess.check_call("otomo reduction", shell=True)

        ret_sample = otomo.analysis_status.get_sample_w_status("analysis_failure")
        self.assertEqual (ret_sample, ["SRP219151_SRR10015386"])
        ret_sample = otomo.analysis_status.get_sample_w_status("reduction_failure")
        self.assertEqual (ret_sample, ["SRP219151_SRR10015394"])

        # job
        subprocess.check_call(("otomo regjob --qacct %s" % (qacct)), shell=True)
        subprocess.check_call("otomo qreport --max 10 -f -b 202106050900", shell=True)

    def test_02_upload(self):

        self.test_02_local()

        # upload
        def __prep(key):
            os.makedirs(os.path.dirname(("%s/%s" % (output_dir, key))), exist_ok = True)
            fw = open("%s/%s" % (output_dir, key), "w")
            fw.write(key)
            fw.close()

        import json
        f = open(samples1)
        samples = json.load(f)
        f.close()
        
        import glob
        import shutil
        for subdir in glob.glob(output_dir + "/*"):
            if subdir.split("/")[-1] == "admin":
                continue
            shutil.rmtree(subdir)

        for key in samples["SRP219151_SRR10015388"]["upload"]:
            __prep(key)
        for key in samples["SRP219151_SRR10015390"]["upload"]:
            if key == "expression/SRP219151_SRR10015390/SRP219151_SRR10015390.txt.gz":
                continue
            __prep(key)
        for key in samples["SRP219151_SRR10015392"]["upload"]:
            __prep(key)

        os.makedirs("%s/fastq/%s" % (output_dir, "SRP219151_SRR10015388"), exist_ok = True)
        os.makedirs("%s/fastq/%s" % (output_dir, "SRP219151_SRR10015390"), exist_ok = True)

        subprocess.check_call("otomo upload", shell=True)

        ret_sample = otomo.analysis_status.get_sample_w_status("finish")
        self.assertEqual (ret_sample, ["SRP219151_SRR10015388"])
        ret_sample = otomo.analysis_status.get_sample_w_status("upload_failure")
        self.assertEqual (ret_sample, ["SRP219151_SRR10015390"])
        ret_sample = otomo.analysis_status.get_sample_w_status("remove_failure")
        self.assertEqual (ret_sample, ["SRP219151_SRR10015392"])

    def test_03_notify(self):
        subprocess.check_call(("otomo notify_quota --quota %s" % (quota)), shell=True)

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(OtomoTest))
    return suite

