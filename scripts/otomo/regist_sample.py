import sqlite3
import json
import datetime
import otomo.CONFIG

def __exists(sample, table, db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute('select count(sample) from %s where sample="%s"' % (table, sample))
    
    ret = True
    if cur.fetchall()[0][0] == 0:
        ret = False
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
    
    now = otomo.CONFIG.date_to_text(datetime.datetime.now())
    insert_list = []
    for key in data:
        if __exists(key, "analysis", db):
            continue
        study = data[key]["study"]
        runid = data[key]["runid"]
        insert_list.append((key, study, runid, "init", "", now, "", ""))
    
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.executemany("insert into analysis values (?, ?, ?, ?, ?, ?, ?, ?)", insert_list)
    con.commit()
    con.close()

    # upload DB
    db = conf.get("db", "upload_db")
    
    insert_list = []
    for key in data:
        if __exists(key, "upload", db):
            continue
        for output in data[key]["upload"]:
            insert_list.append((key, output, data[key]["upload"][output]))
    
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
