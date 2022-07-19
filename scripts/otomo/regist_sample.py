import sqlite3
import json
import datetime
import otomo.CONFIG

def __samples(table, db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute('select sample from %s' % (table))
    
    ret = {}
    for row in cur.fetchall():
        ret[row[0]] = 0
    con.close()
    return ret

def insert_samples(samples_file, conf_file=otomo.CONFIG.DEFAULT_CONF):
    """
    sample情報をanalysis-DB, sample_stage-DBに登録する。すでにDBに登録されている場合、変更なし。
    
    Parameters
    ----------
    samples_file : str
        サンプル情報.json へのパス
        ```
        {
            "SRP219151_SRR10015386": {
                "study": "SRP219151",
                "runid": "SRR10015386",
                "upload": {
                    "expression/SRP219151_SRR10015386/output.txt.fpkm": "s3://BUCKET/expression/SRP219151_SRR10015386/output.txt.fpkm",
                    "expression/SRP219151_SRR10015386/output.txt.gz": "s3://BUCKET/expression/SRP219151_SRR10015386/output.txt.gz",
                    ...
                }
            },
            "SRP219151_SRR10015388": {
                "study": "SRP219151",
                "runid": "SRR10015388",
                "upload": {
                    ...
                }
            }
        }
        ```
    conf_file : str, default otomo.CONFIG.DEFAULT_CONF
        Path to otomo.cfg
    """
    data = json.load(open(samples_file))
    
    # analysis DB
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "analysis_db")
    
    samples = __samples("analysis", db)
    now = otomo.CONFIG.date_to_text(datetime.datetime.now())
    insert_list = []
    for key in data:
        if key in samples:
            continue
        study = data[key]["study"]
        runid = data[key]["runid"]
        size = 0
        if "size" in data[key]:
            size = data[key]["size"]
        insert_list.append((key, study, runid, "init", "", now, "", "", size))
    
    if len(insert_list) > 0:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.executemany("insert into analysis values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", insert_list)
        con.commit()
        con.close()

    # upload DB
    db = conf.get("db", "upload_db")
    
    samples = __samples("upload", db)
    insert_list = []
    for key in data:
        if key in samples:
            continue
        for output in data[key]["upload"]:
            insert_list.append((key, output, data[key]["upload"][output]))
    
    if len(insert_list) > 0:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.executemany("insert into upload values (?, ?, ?)", insert_list)
        con.commit()
        con.close()
        
def main(args):
    """
    command line I/F : sample情報をanalysis-DB, sample_stage-DBに登録する。すでにDBに登録されている場合、変更なし。
    """
    insert_samples(args.samples, args.conf)

if __name__ == "__main__":
    pass
