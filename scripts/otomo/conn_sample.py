import sqlite3
import otomo.CONFIG

def get_sample_w_status(status):
    conf = otomo.CONFIG.load_conf()
    db = conf.get("db", "sample_db")

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select sample from sample where last_status=:status", {"status": status})

    samples = []
    for f in cur.fetchall():
        samples.append(f[0])

    con.close()
    return samples

def set_status_w_sample(sample, status, description = ""):
    conf = otomo.CONFIG.load_conf()
    db = conf.get("db", "sample_db")

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("update sample set last_status=:status,status_describe=:descript where sample=:sample",
        {"status": status, "descript": description, "sample": sample}
    )

    con.commit()
    con.close()

def main(args):
    set_status_w_sample(args.sample, args.status, args.description)

if __name__ == "__main__":
    #select("DRP000425", "init")
    set_status_w_sample("DRP000425_DRR001174", "run", "test")
    get_sample_w_status("run")

