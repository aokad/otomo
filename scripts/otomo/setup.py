import sqlite3
import otomo.CONFIG

def create_db_analysis(db):
    """
    Initialize the analysis-DB.
    
    Parameters
    ----------
    db : str
        Path to analysis-DB
    """
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS analysis")
    cur.execute("create table analysis (%s)" % (",".join(otomo.CONFIG.ANALYSIS_COLUMNS)))
    con.commit()
    con.close()

def create_db_upload(db):
    """
    Initialize the upload-DB.
    
    Parameters
    ----------
    db : str
        Path to upload-DB
    """
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS upload")
    cur.execute("create table upload (%s)" % (",".join(otomo.CONFIG.UPLOAD_COLUMNS)))
    con.commit()
    con.close()

def create_db_sample_stage(db):
    """
    Initialize the sample_stage-DB.
    
    Parameters
    ----------
    db : str
        Path to sample_stage-DB
    """
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS sample_stage")
    cur.execute("create table sample_stage (%s)" % (",".join(otomo.CONFIG.SAMPLE_STAGE_COLUMNS)))
    con.commit()
    con.close()
    
def create_db_job(db):
    """
    Initialize the job-DB.
    
    Parameters
    ----------
    db : str
        Path to job-DB
    """
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS job")
    cur.execute("create table job (%s, primary key(jobnumber, taskid))" % (",".join(otomo.CONFIG.JOB_COLUMNS)))
    con.commit()
    con.close()

def create_db_monitor(db):
    """
    Initialize the monitor-DB.
    
    Parameters
    ----------
    db : str
        Path to monitor-DB
    """
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS success")
    cur.execute("create table success (%s)" % (",".join(otomo.CONFIG.MONITOR_COLUMNS_INT)))
    cur.execute("DROP TABLE IF EXISTS stop")
    cur.execute("create table stop (%s)" % (",".join(otomo.CONFIG.MONITOR_COLUMNS_INT)))
    cur.execute("DROP TABLE IF EXISTS job_count")
    cur.execute("create table job_count (%s)" % (",".join(otomo.CONFIG.MONITOR_COLUMNS_INT)))
    cur.execute("DROP TABLE IF EXISTS hdd_usage")
    cur.execute("create table hdd_usage (%s)" % (",".join(otomo.CONFIG.MONITOR_COLUMNS_REAL)))
#    cur.execute("DROP TABLE IF EXISTS error")
#    cur.execute("create table error (%s)" % (",".join(otomo.CONFIG.MONITOR_COLUMNS_INT)))
    cur.execute("DROP TABLE IF EXISTS unresolv")
    cur.execute("create table unresolv (%s)" % (",".join(otomo.CONFIG.MONITOR_COLUMNS_INT)))
    cur.execute("DROP TABLE IF EXISTS analysis_error")
    cur.execute("create table analysis_error (%s)" % (",".join(otomo.CONFIG.MONITOR_COLUMNS_INT)))
    cur.execute("DROP TABLE IF EXISTS stop_error")
    cur.execute("create table stop_error (%s)" % (",".join(otomo.CONFIG.MONITOR_COLUMNS_INT)))
    cur.execute("DROP TABLE IF EXISTS upload_error")
    cur.execute("create table upload_error (%s)" % (",".join(otomo.CONFIG.MONITOR_COLUMNS_INT)))
    cur.execute("DROP TABLE IF EXISTS remove_error")
    cur.execute("create table remove_error (%s)" % (",".join(otomo.CONFIG.MONITOR_COLUMNS_INT)))

    con.commit()
    con.close()

def main(args):
    """
    command line I/F : Create otomo.cfg and initialize the DBs.
    """
    import os 
    os.makedirs(args.wdir, exist_ok = True)

    #setup config
    otomo.CONFIG.setup_conf(args.wdir, args.conf)
    
    conf = otomo.CONFIG.load_conf(args.conf)
    db_analysis = conf.get("db", "analysis_db")
    db_upload = conf.get("db", "upload_db")
    db_sample_stage = conf.get("db", "sample_stage_db")
    db_job = conf.get("db", "job_db")
    db_monitor = conf.get("db", "monitor_db")
    request_dir = conf.get("db", "request_dir")

    os.makedirs(os.path.dirname(db_analysis), exist_ok = True)
    os.makedirs(os.path.dirname(db_upload), exist_ok = True)
    os.makedirs(os.path.dirname(db_sample_stage), exist_ok = True)
    os.makedirs(os.path.dirname(db_job), exist_ok = True)
    os.makedirs(os.path.dirname(db_monitor), exist_ok = True)
    os.makedirs(request_dir, exist_ok = True)

    create_db_analysis(db_analysis)
    create_db_upload(db_upload)
    create_db_sample_stage(db_sample_stage)
    create_db_job(db_job)
    create_db_monitor(db_monitor)
    
if __name__ == "__main__":
    pass
