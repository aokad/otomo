import sqlite3
import otomo.CONFIG

def view_analysis(args):
    conf = otomo.CONFIG.load_conf(args.conf)
    db = conf.get("db", "analysis_db")

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select * from analysis %s" % args.option)

    data = []
    header = []
    for h in otomo.CONFIG.ANALYSIS_COLUMNS:
        header.append(h.split(" ")[0])
    data.append("\t".join(header))

    for row in cur.fetchall():
        text = []
        for i in row:
            text.append(str(i))
        data.append("\t".join(text))

    con.close()
    print("\n".join(data))

def view_upload(args):
    conf = otomo.CONFIG.load_conf(args.conf)
    db = conf.get("db", "upload_db")

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select * from upload %s" % args.option)

    data = []
    header = []
    for h in otomo.CONFIG.UPLOAD_COLUMNS:
        header.append(h.split(" ")[0])
    data.append("\t".join(header))

    for row in cur.fetchall():
        text = []
        for i in row:
            text.append(str(i))
        data.append("\t".join(text))

    con.close()
    print("\n".join(data))

def view_sample_stage(args):
    conf = otomo.CONFIG.load_conf(args.conf)
    db = conf.get("db", "sample_stage_db")

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select * from sample_stage %s" % args.option)

    data = []
    header = []
    for h in otomo.CONFIG.SAMPLE_STAGE_COLUMNS:
        header.append(h.split(" ")[0])
    data.append("\t".join(header))

    for row in cur.fetchall():
        text = []
        for i in row:
            text.append(str(i))
        data.append("\t".join(text))

    con.close()
    print("\n".join(data))

def view_job(args):
    conf = otomo.CONFIG.load_conf(args.conf)
    db = conf.get("db", "job_db")

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select * from job %s" % args.option)

    data = []
    header = []
    for h in otomo.CONFIG.JOB_COLUMNS:
        header.append(h.split(" ")[0])
    data.append("\t".join(header))

    for row in cur.fetchall():
        text = []
        for i in row:
            text.append(str(i))
        data.append("\t".join(text))

    con.close()
    print("\n".join(data))

def view_monitor(args):
    conf = otomo.CONFIG.load_conf(args.conf)
    db = conf.get("db", "monitor_db")

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select * from %s %s" % (args.table, args.option))

    data = []
    header = []
    for h in otomo.CONFIG.MONITOR_COLUMNS_INT:
        header.append(h.split(" ")[0])
    data.append("\t".join(header))

    for row in cur.fetchall():
        text = []
        for i in row:
            text.append(str(i))
        data.append("\t".join(text))

    con.close()
    print("\n".join(data))

def main(args):
    if args.table == "analysis":
        view_analysis(args)

    elif args.table == "upload":
        view_upload(args)

    elif args.table == "sample_stage":
        view_sample_stage(args)

    elif args.table == "job":
        view_job(args)

    elif args.table in ["success", "error", "stop", "job_count", "hdd_usage"]:
        view_monitor(args)

if __name__ == "__main__":
    pass

