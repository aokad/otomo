# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:18:34 2016

@author: okada

"""

import unittest
import subprocess
import datetime
import os
import otomo.analysis_status
import otomo.qreport

cur = os.path.dirname(__file__)
samples1 = cur + "/samples1.json"
samples2 = cur + "/samples2.json"
output_dir = os.path.dirname(cur) + "/temp"
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
        subprocess.check_call("otomo setup --wdir %s" % (output_dir), shell=True)
        subprocess.check_call("otomo regsample --samples %s" % (samples1), shell=True)
        subprocess.check_call("otomo regsample --samples %s" % (samples2), shell=True)
        
        ret_sample = otomo.analysis_status.get_sample_w_status("init")
        self.assertEqual (len(ret_sample), 20)
        
        # set status
        otomo.analysis_status.set_status_request("SRP219151_SRR10015386", "run", stage="fastq")
        otomo.analysis_status.set_status_request("SRP219151_SRR10015386", "run", stage="star")
        otomo.analysis_status.set_status_request("SRP219151_SRR10015386", "failure")

        otomo.analysis_status.set_status_request("SRP219151_SRR10015396", "run", stage="fastq")
        otomo.analysis_status.set_status_request("SRP219151_SRR10015396", "run", stage="star")
        otomo.analysis_status.set_status_request("SRP219151_SRR10015396", "run", stage="expression")
        otomo.analysis_status.set_status_request("SRP219151_SRR10015396", "failure")

        otomo.analysis_status.set_status_request("SRP219151_SRR10015394", "run", stage="fastq")
        otomo.analysis_status.set_status_request("SRP219151_SRR10015394", "run", stage="star")
        otomo.analysis_status.set_status_request("SRP219151_SRR10015394", "run", stage="expression")
        otomo.analysis_status.set_status_request("SRP219151_SRR10015394", "run", stage="ir_count")
        otomo.analysis_status.set_status_request("SRP219151_SRR10015394", "failure")

        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015388 --status run --stage fastq", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015388 --status run --stage star", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015388 --status run --stage expression", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015388 --status run --stage ir_count", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015388 --status run --stage iravnet", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015388 --status run --stage juncmut", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015388 --status success", shell=True)

        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015390 --status run --stage fastq", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015390 --status run --stage star", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015390 --status run --stage expression", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015390 --status run --stage ir_count", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015390 --status run --stage iravnet", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015390 --status run --stage juncmut", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015390 --status success", shell=True)

        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015392 --status run --stage fastq", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015392 --status run --stage star", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015392 --status run --stage expression", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015392 --status run --stage ir_count", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015392 --status run --stage iravnet", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015392 --status run --stage juncmut", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015392 --status success", shell=True)

        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015398 --status run --stage fastq", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015400 --status run --stage fastq", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015400 --status run --stage star", shell=True)
        subprocess.check_call("otomo analysis --sample SRP219151_SRR10015398 --status run --stage fastq", shell=True)
        subprocess.check_call("otomo analysis --commit", shell=True)

        ret_sample = otomo.analysis_status.get_sample_w_status("failure")
        self.assertEqual (ret_sample, ["SRP219151_SRR10015386","SRP219151_SRR10015394", "SRP219151_SRR10015396"])

        ret_sample = otomo.analysis_status.get_sample_w_status("success")
        self.assertEqual (ret_sample, ["SRP219151_SRR10015388", "SRP219151_SRR10015390", "SRP219151_SRR10015392"])

        ret_count = otomo.analysis_status.get_run_count_w_sample("SRP219151_SRR10015398")
        self.assertEqual (ret_count, {'fastq': 2})

        ret_count = otomo.analysis_status.get_run_count_w_sample("SRP219151_SRR10015400")
        self.assertEqual (ret_count, {'fastq': 1, 'star': 1})

        ret_sample = otomo.analysis_status.get_sample_count_groupby_status_stage()
        self.assertEqual (ret_sample["init"][""], 12)
        self.assertEqual (ret_sample["run"]["fastq"], 1)
        self.assertEqual (ret_sample["run"]["star"], 1)
        self.assertEqual (ret_sample["success"]["juncmut"], 3)
        self.assertEqual (ret_sample["failure"]["star"], 1)
        self.assertEqual (ret_sample["failure"]["ir_count"], 1)
        self.assertEqual (ret_sample["failure"]["expression"], 1)

        # reduction
        os.makedirs("%s/fastq/%s" % (output_dir, "SRP219151_SRR10015386"), exist_ok = True)
        os.makedirs("%s/star/%s" % (output_dir, "SRP219151_SRR10015386"), exist_ok = True)
        os.makedirs("%s/expression/%s" % (output_dir, "SRP219151_SRR10015386"), exist_ok = True)
        os.makedirs("%s/ir_count/%s" % (output_dir, "SRP219151_SRR10015386"), exist_ok = True)
        os.makedirs("%s/iravnet/%s" % (output_dir, "SRP219151_SRR10015386"), exist_ok = True)
        os.makedirs("%s/juncmut/%s" % (output_dir, "SRP219151_SRR10015386"), exist_ok = True)
        os.makedirs("%s/log/%s" % (output_dir, "SRP219151_SRR10015386"), exist_ok = True)
        fw = open("%s/log/%s/star.e123" % (output_dir, "SRP219151_SRR10015386"), "w")
        fw.write("This Error is not STOP.\n")
        fw.close()

        os.makedirs("%s/fastq/%s" % (output_dir, "SRP219151_SRR10015396"), exist_ok = True)
        os.makedirs("%s/star/%s" % (output_dir, "SRP219151_SRR10015396"), exist_ok = True)
        os.makedirs("%s/expression/%s" % (output_dir, "SRP219151_SRR10015396"), exist_ok = True)
        os.makedirs("%s/ir_count/%s" % (output_dir, "SRP219151_SRR10015396"), exist_ok = True)
        os.makedirs("%s/iravnet/%s" % (output_dir, "SRP219151_SRR10015396"), exist_ok = True)
        os.makedirs("%s/juncmut/%s" % (output_dir, "SRP219151_SRR10015396"), exist_ok = True)
        os.makedirs("%s/log/%s" % (output_dir, "SRP219151_SRR10015396"), exist_ok = True)
        fw = open("%s/log/%s/star_alignment.e123" % (output_dir, "SRP219151_SRR10015396"), "w")
        fw.write("EXITING because of FATAL ERROR in reads input: short read sequence line: \n")
        fw.close()

        subprocess.check_call("otomo reduction", shell=True)

        ret_sample = otomo.analysis_status.get_sample_w_status("analysis_error")
        self.assertEqual (ret_sample, ["SRP219151_SRR10015386"])
        ret_sample = otomo.analysis_status.get_sample_w_status("remove_error")
        self.assertEqual (ret_sample, ["SRP219151_SRR10015394"])
        ret_sample = otomo.analysis_status.get_sample_w_status("stop")
        self.assertEqual (ret_sample, ["SRP219151_SRR10015396"])

        # job
        subprocess.check_call("otomo regjob --qacct %s" % (qacct), shell=True)
        subprocess.check_call("otomo qreport --max 10 -f -b 202106221445", shell=True)

        # view table
        subprocess.check_call('otomo view --table analysis', shell=True)
        subprocess.check_call('otomo view --table upload --option "where sample=\'SRP219151_SRR10015386\'"', shell=True)
        subprocess.check_call('otomo view --table sample_stage', shell=True)
        subprocess.check_call('otomo view --table job --option "limit 10"', shell=True)

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
        ret_sample = otomo.analysis_status.get_sample_w_status("upload_error")
        self.assertEqual (ret_sample, ["SRP219151_SRR10015390"])
        ret_sample = otomo.analysis_status.get_sample_w_status("remove_error")
        self.assertEqual (ret_sample, ["SRP219151_SRR10015392", "SRP219151_SRR10015394"])

    def test_02_duplicate(self):
        #  setup
        subprocess.check_call("otomo setup --wdir %s" % (output_dir), shell=True)
        subprocess.check_call("otomo regsample --samples %s" % (samples2), shell=True)

        otomo.analysis_status.set_status_request("SRP212755_SRR10080437", "failure")
        otomo.analysis_status.set_status_commit()
        subprocess.check_call("otomo regsample --samples %s" % (samples2), shell=True)
        ret_sample = otomo.analysis_status.get_sample_w_status("failure")
        self.assertEqual (ret_sample, ["SRP212755_SRR10080437"])

        # job
        subprocess.check_call("otomo regjob --qacct %s" % (qacct), shell=True)
        subprocess.check_call("otomo qreport --max 10 -f -b 202106050900", shell=True)
        subprocess.check_call("otomo regjob --qacct %s" % (qacct), shell=True)
        subprocess.check_call("otomo qreport --max 10 -f -b 202106050900", shell=True)

    def test_02_conflict(self):
        #  setup
        subprocess.check_call("otomo setup --wdir %s" % (output_dir), shell=True)
        subprocess.check_call("otomo regsample --samples %s" % (samples2), shell=True)
        subprocess.check_call("cat %s | parallel -a - --jobs 20 otomo analysis --status run --stage fastq --sample 2>&1" % (samples2.replace(".json", ".txt")), shell=True)
        subprocess.check_call("otomo analysis --commit", shell=True)
        subprocess.check_call("otomo view --table analysis", shell=True)
        subprocess.check_call("otomo view --table sample_stage", shell=True)

    def test_03_notify(self):
        subprocess.check_call("otomo notify_quota --quota %s" % (quota), shell=True)

    def test_03_slice_jobcount(self):
        subprocess.check_call("otomo setup --wdir %s" % (output_dir), shell=True)
        subprocess.check_call("otomo regjob --qacct %s" % (qacct), shell=True)
        ret_sample = otomo.qreport.slice_jobcount_all(end_time = datetime.datetime.strptime("202106221500", '%Y%m%d%H%M'))
        counts = []
        for c in ret_sample:
            counts.append(c[1])
        self.assertEqual (counts, [1, 15, 19, 1])

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(OtomoTest))
    return suite

