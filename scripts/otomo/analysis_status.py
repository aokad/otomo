import sqlite3
import datetime
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

def set_status_w_sample(sample, status, description = "", error = "", stop_reason = "", conf_file=otomo.CONFIG.DEFAULT_CONF):
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "analysis_db")

    now = otomo.CONFIG.date_to_text(datetime.datetime.now())
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("update analysis set last_status=:status, last_update=:now where sample=:sample", 
        {"status": status, "sample": sample, "now": now}
    )

    if description != "":
        cur.execute("update analysis set status_describe=:descript where sample=:sample",
            {"descript": description, "sample": sample}
        )
    if error != "":
        cur.execute("update analysis set error_describe=:error where sample=:sample",
            {"error": error, "sample": sample}
        )
    if stop_reason != "":
        cur.execute("update analysis set stop_reason=:stop_reason where sample=:sample",
            {"stop_reason": stop_reason, "sample": sample}
        )

    con.commit()
    con.close()

def get_run_count_w_sample(sample, conf_file=otomo.CONFIG.DEFAULT_CONF):
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "analysis_db")

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select run_count from analysis where sample='%s'" % (sample))

    count = 0
    for f in cur.fetchall():
        count = f[0]

    con.close()
    return count

def countup(args):
    conf = otomo.CONFIG.load_conf(args.conf)
    db = conf.get("db", "analysis_db")
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select run_count from analysis where sample='%s'" % (args.sample))

    run_count = 0
    for f in cur.fetchall():
        run_count = f[0]
    con.close()

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("update analysis set run_count=:count where sample=:sample",
        {"count": run_count+1, "sample": args.sample}
    )

    con.commit()
    con.close()

def main(args):
    set_status_w_sample(args.sample, args.status, description = args.description, error = args.error_message, stop_reason = args.stop_reason)

if __name__ == "__main__":
    #select("DRP000425", "init")
    set_status_w_sample("DRP000425_DRR001174", "run", description ="test")
    get_sample_w_status("run")

