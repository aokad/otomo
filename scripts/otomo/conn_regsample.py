import sqlite3
import otomo.CONFIG

def insert_samples(samples_file):
    conf = otomo.CONFIG.load_conf()
    db = conf.get("db", "sample_db")
    
    sample_list = []
    for row in open(samples_file).read().split("\n"):
        if row == "":
            continue
        (study, runid) = row.split("_")
        sample_list.append((row, runid, study, "init", ""))
    
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.executemany("insert into sample values (?, ?, ?, ?, ?)", sample_list)
    con.commit()
    con.close()

def main(args):    
    insert_samples(args.samples)

if __name__ == "__main__":
    pass
