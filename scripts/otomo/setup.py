import sqlite3
import otomo.CONFIG

def create_db_analysis(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS analysis")
    cur.execute("create table analysis (%s)" % (",".join(otomo.CONFIG.ANALYSIS_COLUMNS)))
    con.commit()
    con.close()

def create_db_upload(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS upload")
    cur.execute("create table upload (%s)" % (",".join(otomo.CONFIG.UPLOAD_COLUMNS)))
    con.commit()
    con.close()

def create_db_sample_stage(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS sample_stage")
    cur.execute("create table sample_stage (%s)" % (",".join(otomo.CONFIG.SAMPLE_STAGE_COLUMNS)))
    con.commit()
    con.close()
    
def create_db_job(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS job")
    cur.execute("create table job (%s, primary key(jobnumber, taskid))" % (",".join(otomo.CONFIG.JOB_COLUMNS)))
    con.commit()
    con.close()

def create_db_monitor(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS success")
    cur.execute("create table success (%s)" % (",".join(otomo.CONFIG.MONITOR_INT_COLUMNS)))
    cur.execute("DROP TABLE IF EXISTS error")
    cur.execute("create table error (%s)" % (",".join(otomo.CONFIG.MONITOR_INT_COLUMNS)))
    cur.execute("DROP TABLE IF EXISTS stop")
    cur.execute("create table stop (%s)" % (",".join(otomo.CONFIG.MONITOR_INT_COLUMNS)))
    cur.execute("DROP TABLE IF EXISTS job_count")
    cur.execute("create table job_count (%s)" % (",".join(otomo.CONFIG.MONITOR_INT_COLUMNS)))
    cur.execute("DROP TABLE IF EXISTS hdd_usage")
    cur.execute("create table hdd_usage (%s)" % (",".join(otomo.CONFIG.MONITOR_REAL_COLUMNS)))

    con.commit()
    con.close()

def main(args):
    import os 
    os.makedirs(args.wdir, exist_ok = True)

    #setup config
    otomo.CONFIG.setup_conf(args.wdir)
    
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
