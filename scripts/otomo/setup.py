import sqlite3
import otomo.CONFIG

def create_db_analysis_status(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS sample")
    cur.execute("create table sample (%s)" % (",".join(otomo.CONFIG.SAMPLE_COLUMUNS)))
    con.commit()
    con.close()

def create_db_qreport(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS job")
    cur.execute("create table job (%s)" % (",".join(otomo.CONFIG.JOB_COLMUNS)))
    con.commit()
    con.close()

def main(args):
    import os 
    os.makedirs(args.wdir, exist_ok = True)

    #setup config
    otomo.CONFIG.setup_conf(args.wdir)
    
    conf = otomo.CONFIG.load_conf()
    db_sample = conf.get("db", "sample_db")
    db_job = conf.get("db", "job_db")
    os.makedirs(os.path.dirname(db_sample), exist_ok = True)
    os.makedirs(os.path.dirname(db_job), exist_ok = True)
    
    create_db_analysis_status(db_sample)
    create_db_qreport(db_job)

if __name__ == "__main__":
    pass
