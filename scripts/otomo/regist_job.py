import datetime
import sqlite3
import otomo.CONFIG

def __exists(jobnumber, taskid, db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select count(jobnumber) from job where jobnumber=:jobnumber and taskid=:taskid",
        {"jobnumber": jobnumber, "taskid": taskid}
    )
    
    ret = True
    if cur.fetchall()[0][0] == 0:
        ret = False
    con.close()
    return ret

def __text_to_date(text):
    return datetime.datetime.strptime(text, '%m/%d/%Y %H:%M:%S.%f')

def __insert(item, db):
    job = []
    for key in otomo.CONFIG.JOB_COLMUNS:
        job.append(item[key.split(" ")[0]])

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("insert into job values (" + ",".join(["?"] * len(job)) + ")", job)
    con.commit()
    con.close()

def __insert_job(item, db):
    if __exists(item["jobnumber"], item["taskid"], db):
        return

    submit = __text_to_date(item["qsub_time"])
    start = __text_to_date(item["start_time"])
    end = __text_to_date(item["end_time"])
    item["wait_time_h"] = "%.2f" % ((start-submit).total_seconds() / 3600)
    item["run_time_h"] = "%.2f" % ((end-start).total_seconds() / 3600)

    item["qsub_time"] = otomo.CONFIG.date_to_text(submit)
    item["start_time"] = otomo.CONFIG.date_to_text(start)
    item["end_time"] = otomo.CONFIG.date_to_text(end)
    
    if item["failed"] == "0" and item["exit_status"] == "0":
        item["failed"] = "0"
    else:
        item["failed"] = "1"

    try:
        cpu = float(item["cpu"])
    except Exception:
        cpu = 0.0

    try:
        wallclock = float(item["wallclock"])
    except Exception:
        wallclock = 0.0

    if wallclock > 0:
        item["use_cpu_rate"] = "%.2f" % (cpu / wallclock)
    else:
        item["use_cpu_rate"] = "NA"

    try:
        l_mem = float(item["l_mem_g"])
        slots = float(item["l_slots"])
        item["l_mem_g"] = "%.2f" % (l_mem * slots)
    except Exception:
        item["l_mem_g"] = item["l_mem_g"] + "*"
    
    __insert(item, db)

def __qreport(qacct_path):
    return open(qacct_path).read().split("\n")

def __init_item():
    dic = {}
    for key in otomo.CONFIG.JOB_COLMUNS:
        dic[key.split(" ")[0]] = ""

    dic["cpu"] = ""
    dic["wallclock"] = ""
    dic["exit_status"] = ""

    return dic

def _main(qacct_path, conf_file=otomo.CONFIG.DEFAULT_CONF):
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "job_db")

    qreport = __qreport(qacct_path)
    item = __init_item()

    for row in qreport:
        row = row.strip().rstrip()
        if row.startswith("jobnumber"):
            item["jobnumber"] = row.split(" ")[-1]
            continue
        if row.startswith("taskid"):
            item["taskid"] = row.split(" ")[-1]
            continue
        if row.startswith("slots"):
            item["l_slots"] = row.split(" ")[-1]
            continue
        if row.startswith("exit_status"):
            item["exit_status"] = row.split(" ")[-1]
            continue
        if row.startswith("failed"):
            item["failed"] = row.split(" ")[-1]
            continue
        if row.startswith("qname"):
            item["qname"] = row.split(" ")[-1]
            continue
        if row.startswith("hostname"):
            item["hostname"] = row.split(" ")[-1]
            continue
        if row.startswith("jobname"):
            item["jobname"] = row.split(" ")[-1]
            continue
        if row.startswith("qsub_time"):
            item["qsub_time"] = row.split(" ")[-2] + " " + row.split(" ")[-1]
            continue
        if row.startswith("start_time"):
            item["start_time"] = row.split(" ")[-2] + " " + row.split(" ")[-1]
            continue
        if row.startswith("end_time"):
            item["end_time"] = row.split(" ")[-2] + " " + row.split(" ")[-1]
            continue
        if row.startswith("maxvmem"):
            value = row.split(" ")[-1]
            if value.endswith("M"):
                value2 = float(value.replace("M", ""))/1024
                item["use_maxvmem_g"] = "%.2f" % (value2)
            elif value.endswith("K"):
                value2 = float(value.replace("K", ""))/1024/1024
                item["use_maxvmem_g"] = "%.2f" % (value2)
            else:
                item["use_maxvmem_g"] = value.replace("G", "")
            continue
        if row.startswith("cpu"):
            item["cpu"] = row.split(" ")[-1]
            continue
        if row.startswith("submit_cmd"):
            try:
                item["sample"] = row.split("/")[-2]
            except Exception:
                pass
            for c in row.split(" "):
                if c.startswith("mem_req="):
                    item["l_mem_g"] = c.split("=")[-1].replace("G", "")
            continue
        if row.startswith("ru_wallclock"):
            item["wallclock"] = row.split(" ")[-1]
            continue

        if row.startswith("===") and item["jobnumber"] != "" and item["jobname"] != "QLOGIN":
            __insert_job(item, db)
            item = __init_item()

    if item["jobnumber"] != "" and item["jobname"] != "QLOGIN":
        __insert_job(item, db)

def main(args):
    _main(args.qacct, args.conf)

if __name__ == "__main__":
    _main('./qacct.txt')

