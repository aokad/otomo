DB_NAME_SAMPLE_DEFAULT = "analysis_status.sqlite3"
DB_NAME_JOB_DEFAULT = "qreport.sqlite3"

SAMPLE_COLUMUNS = [
    "sample text",
    "runid integer",
    "study text",
    "last_status text",
    "status_describe text"
]

JOB_COLMUNS = [
    "jobnumber integer",
    "taskid integer",
    "jobname text",
    "sample text",
    "failed integer",
    "use_cpu_rate real",
    "use_maxvmem_g real",
    "l_slots integer",
    "l_mem_g real",
    "qname text",
    "hostname text",
    "qsub_time datetime",
    "start_time datetime",
    "end_time datetime",
    "wait_time_h real",
    "run_time_h real",
]

import os
DEFAULT_CONF = os.path.expanduser('~/.otomo.conf')

def setup_conf(wdir):
    f = open(DEFAULT_CONF, "w")
    f.write("""[db]
sample_db = {wdir}/admin/sample.sqlite3
job_db = {wdir}/admin/job.sqlite3
[work]
dir = {wdir}
""".format(wdir = wdir))
    f.close()

def load_conf():
    import configparser
    parsed_conf = configparser.ConfigParser()
    parsed_conf.read(DEFAULT_CONF)
    return parsed_conf
