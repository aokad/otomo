ANALYSIS_COLUMNS = [
    "sample text primary key",
    "study text",
    "runid text",
    "status text",
    "stage text",
    "last_update datetime",
    "error_text text",
    "stop_reason text",
    "size integer",
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
    "failed text",
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

ECSUB_COLUMNS = [
    "taskname text",
    "taskid text",
    "status text",
    "image text",
    "instance_type text",
    "cpu integer",
    "memory integer",
    "disk_size integer",
    "max_pct_cpu_util integer",
    "max_pct_memory_util integer",
    "max_pct_disk_util integer",
    "start_time datetime",
    "end_time datetime",
    "run_time_h real",
    "spot integer",
    "goofys integer",
    "region text",
]

MONITOR_COLUMNS_INT = [
    "timestamp int primary key",
    "value integer",
]
MONITOR_COLUMNS_REAL = [
    "timestamp int primary key",
    "value real",
]

import os
DEFAULT_CONF = os.path.expanduser('~/.otomo.conf')

def setup_conf(wdir, conf_file=DEFAULT_CONF):
    """
    otomo.cfgを作成する。あれば上書きする。
    
    Parameters
    ----------
    wdir : str
        Path to working directory of the pipeline you want to use otomo
    
    conf_file : str, default otomo.CONFIG.DEFAULT_CONF
        Path to otomo.cfg
    """

    f = open(conf_file, "w")
    f.write("""[db]
analysis_db = {wdir}/admin/analysis.sqlite3
upload_db = {wdir}/admin/upload.sqlite3
sample_stage_db = {wdir}/admin/sample_stage.sqlite3
job_db = {wdir}/admin/job.sqlite3
monitor_db = {wdir}/admin/monitor.sqlite3
ecsub_db = {wdir}/admin/ecsub.sqlite3
request_dir = {wdir}/admin/request

[work]
dir = {wdir}
ecsub_dir = 

[notify]
slack_url = 
channel = #channel
label = NAME

[reduction]
enable = True
remove_dirs = fastq,star,expression,ir_count,iravnet,juncmut,join

[upload]
endpoint_url = 
profile = 
remove_dirs = fastq,star,expression,ir_count,iravnet,juncmut,join

""".format(wdir = wdir.rstrip("/")))
    f.close()

def load_conf(conf_file):
    """
    otomo.cfgを読み込む
    
    Parameters
    ----------
    conf_file : str, default otomo.CONFIG.DEFAULT_CONF
        Path to otomo.cfg
    
    Returns
    -------
    parsed_conf : configparser.ConfigParser
        parsed conf
    """
    import configparser
    parsed_conf = configparser.ConfigParser()
    parsed_conf.read(conf_file)
    return parsed_conf

def date_to_text(dt):
    """
    datettimeをテキストに変換する
    
    Parameters
    ----------
    dt : datettime.datetime
        datetime
    
    Returns
    -------
    text : str
        %Y/%m/%d %H:%M:%S
    """
    return dt.strftime('%Y/%m/%d %H:%M:%S')
