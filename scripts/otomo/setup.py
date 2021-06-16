import sqlite3
import otomo.CONFIG

def create_db_sample_analysis(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS analysis")
    cur.execute("create table analysis (%s)" % (",".join(otomo.CONFIG.ANALYSIS_COLUMUNS)))
    con.commit()
    con.close()

def create_db_sample_upload(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS upload")
    cur.execute("create table upload (%s)" % (",".join(otomo.CONFIG.UPLOAD_COLUMUNS)))
    con.commit()
    con.close()
    
def create_db_qreport(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS job")
    cur.execute("create table job (%s, primary key(jobnumber, taskid))" % (",".join(otomo.CONFIG.JOB_COLMUNS)))
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
    db_job = conf.get("db", "job_db")
    
    os.makedirs(os.path.dirname(db_analysis), exist_ok = True)
    os.makedirs(os.path.dirname(db_upload), exist_ok = True)
    os.makedirs(os.path.dirname(db_job), exist_ok = True)
    
    create_db_sample_analysis(db_analysis)
    create_db_sample_upload(db_upload)
    create_db_qreport(db_job)
    
if __name__ == "__main__":
    pass
