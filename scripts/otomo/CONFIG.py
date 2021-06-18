ANALYSIS_COLUMNS = [
    "sample text primary key",
    "study text",
    "runid text",
    "status text",
    "stage text",
    "last_update datetime",
    "error_text text",
    "stop_reason text",
]

UPLOAD_COLUMNS = [
    "sample text",
    "output text primary key",
    "uri text",
]

SAMPLE_STAGE_COLUMNS = [
    "sample text",
    "stage text",
    "start_time datetime",
]

JOB_COLUMNS = [
    "jobnumber integer",
    "taskid integer",
    "jobname text",
    "sample text",
    "failed integer",
    "use_cpu_rate real",
    "l_slots integer",
    "use_maxvmem_g real",
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
analysis_db = {wdir}/admin/analysis.sqlite3
upload_db = {wdir}/admin/upload.sqlite3
sample_stage_db = {wdir}/admin/sample_stage.sqlite3
job_db = {wdir}/admin/job.sqlite3
request_dir = {wdir}/admin/request

[work]
dir = {wdir}

[notify]
slack_url = 
channel = #channel
label = NAME

[upload]
endpoint_url = 
profile = 
remove_dirs = fastq,star,expression,ir_count,iravnet,juncmut

""".format(wdir = wdir.rstrip("/")))
    f.close()

def load_conf(conf):
    import configparser
    parsed_conf = configparser.ConfigParser()
    parsed_conf.read(conf)
    return parsed_conf

def date_to_text(dt):
    return dt.strftime('%Y/%m/%d %H:%M:%S')
