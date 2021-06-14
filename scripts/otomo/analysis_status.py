import sqlite3
import otomo.CONFIG

def get_sample_w_status(status, max = 0, conf_file=otomo.CONFIG.DEFAULT_CONF):
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "analysis_db")

    limit = ""
    if max > 0:
        limit = "limit %d" % (max)
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select sample from analysis where last_status='%s' %s" % (status, limit))

    samples = []
    for f in cur.fetchall():
        samples.append(f[0])

    con.close()
    return samples

def get_sample_count_g_status(conf_file=otomo.CONFIG.DEFAULT_CONF):
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "analysis_db")

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select last_status,count(sample) from analysis group by last_status")

    status = {}
    for f in cur.fetchall():
        status[f[0]] = f[1]

    con.close()
    return status

def set_status_w_sample(sample, status, description = "", conf_file=otomo.CONFIG.DEFAULT_CONF):
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "analysis_db")

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("update analysis set last_status=:status,status_describe=:descript where sample=:sample",
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

