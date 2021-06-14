import sqlite3
import otomo.CONFIG
import json

def insert_samples(samples_file, conf_file=otomo.CONFIG.DEFAULT_CONF):
    data = json.load(open(samples_file))
    
    # analysis DB
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "analysis_db")
    
    insert_list = []
    for key in data:
        study = data[key]["study"]
        runid = data[key]["runid"]
        insert_list.append((key, runid, study, "init", ""))
    
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.executemany("insert into analysis values (?, ?, ?, ?, ?)", insert_list)
    con.commit()
    con.close()

    # upload DB
    db = conf.get("db", "upload_db")
    
    insert_list = []
    for key in data:
        for output in data[key]["upload"]:
            insert_list.append((key, output, data[key]["upload"][output]))
    
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.executemany("insert into upload values (?, ?, ?)", insert_list)
    con.commit()
    con.close()
    
def main(args):    
    insert_samples(args.samples, args.conf)

if __name__ == "__main__":
    pass
