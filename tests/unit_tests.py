# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:18:34 2016

@author: okada

"""

import unittest
import subprocess

import os
cur = os.path.dirname(__file__)
samples1 = cur + "/samples1.txt"
samples2 = cur + "/samples2.txt"
output_dir = cur + "/../temp"
qacct = cur + "/qacct.txt"

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
    
    def test_02_setup(self):
        subprocess.check_call(("otomo setup --wdir %s" % (output_dir)), shell=True)
        subprocess.check_call(("otomo regsample --samples %s" % (samples1)), shell=True)
        subprocess.check_call(("otomo regsample --samples %s" % (samples2)), shell=True)
        
        import otomo.conn_sample
        ret_sample = otomo.conn_sample.get_sample_w_status("init")
        self.assertEqual (len(ret_sample), 120)
        
    # sample        
    def test_03_function(self):
        import otomo.conn_sample
        otomo.conn_sample.set_status_w_sample("SRP219151_SRR10015386", "run")
        ret_sample = otomo.conn_sample.get_sample_w_status("run")
        self.assertEqual (ret_sample, ["SRP219151_SRR10015386"])

    def test_03_command(self):
        subprocess.check_call("otomo sample --sample SRP219151_SRR10015388 --status error", shell=True)

        import otomo.conn_sample
        ret_sample = otomo.conn_sample.get_sample_w_status("error")
        self.assertEqual (ret_sample, ["SRP219151_SRR10015388"])
        
    # job
    def test_04_regjob(self):
        subprocess.check_call(("otomo regjob --qacct %s" % (qacct)), shell=True)

    def test_05_qreport(self):
        subprocess.check_call("otomo qreport --max 10 -f -b 202106050900", shell=True)

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(OtomoTest))
    return suite

