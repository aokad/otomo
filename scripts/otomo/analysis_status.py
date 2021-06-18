import sqlite3
import datetime
import json
import glob
import os
import otomo.CONFIG

def get_sample_w_status(status, where = None, limit = 0, conf_file=otomo.CONFIG.DEFAULT_CONF):
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "analysis_db")

    sql_limit = ""
    if limit > 0:
        sql_limit = "limit %d" % (limit)

    data = {"status": status}
    sql_where = ""
    if where != None:
        """
        where = {
            "sql": "description=:desc and run_count>:count",
            "value": {"desc": "join", "count": 2}
        }
        """
        sql_where = "and (%s)" % (where["sql"])
        data.update(where["value"])

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select sample from analysis where status=:status %s %s" % (sql_where, sql_limit), data)
    
    samples = []
    for f in cur.fetchall():
        samples.append(f[0])

    con.close()
    return samples

def get_sample_count_g_status(where = None, conf_file=otomo.CONFIG.DEFAULT_CONF):
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "analysis_db")

    data = {}
    sql_where = ""
    if where != None:
        """
        where = {
            "sql": "description=:desc and run_count>:count",
            "value": {"desc": "join", "count": 2}
        }
        """
        sql_where = "where " + where["sql"]
        data.update(where["value"])

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select status,count(sample) from analysis %s group by status" % (sql_where), data)
    
    status = {}
    for f in cur.fetchall():
        status[f[0]] = f[1]

    con.close()
    return status

def get_run_count_w_sample(sample, conf_file=otomo.CONFIG.DEFAULT_CONF):
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "analysis_db")

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select run_count from analysis where sample=:sample", {"sample": sample})

    count = 0
    for f in cur.fetchall():
        count = f[0]

    con.close()
    return count

def set_status_request(sample, status, countup = False, description = "", error_text = "", stop_reason = "", conf_file=otomo.CONFIG.DEFAULT_CONF):

    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "analysis_db")

    now = datetime.datetime.now()
    write_data = {
        "sample": sample,
        "status": status,
        "last_update": otomo.CONFIG.date_to_text(now)
    }
    if countup:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute("select run_count from analysis where sample='%s'" % (sample))

        run_count = 0
        for f in cur.fetchall():
            run_count = f[0]
        con.close()
        write_data["run_count"] = run_count + 1

    if description != "":
        write_data["description"] = description

    if error_text != "":
        write_data["error_text"] = error_text

    if stop_reason != "":
        write_data["stop_reason"] = stop_reason

    temp_name = "%s/%s_%s.json" % (conf.get("db", "request_dir"), now.strftime('%Y%m%d_%H%M%S%f'), sample)
    fw = open(temp_name, "w")
    json.dump(write_data, fw)
    fw.close()

def set_status_commit(conf_file=otomo.CONFIG.DEFAULT_CONF):

    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "analysis_db")
    requests = sorted(glob.glob("%s/*.json" % (conf.get("db", "request_dir"))))
    sqls = []
    commited_requests = []
    for i,request in enumerate(requests):
        if i >= 1000:
            break
        f = open(request)
        data = json.load(f)
        f.close()
        items = []
        for key in data:
            if key == "sample":
                continue
            items.append("%s=:%s" % (key, key))
        sqls.append(("update analysis set %s where sample=:sample" % (",".join(items)), data))
        commited_requests.append(request)

    error = None
    try:
        con = sqlite3.connect(db, isolation_level='EXCLUSIVE')
        cur = con.cursor()
        for sql in sqls:
            #print(sql)
            cur.execute(sql[0], sql[1])
        con.commit()

    except Exception as e:
        error = e

    finally:
        if con:
            con.close()

    if error != None:
        raise error

    for request in commited_requests:
        os.remove(request)

def main(args):
    if args.commit == False:
        set_status_request(
            args.sample, 
            args.status, 
            countup = args.countup, 
            description = args.description, 
            error_text = args.error_text, 
            stop_reason = args.stop_reason, 
            conf_file=args.conf
        )
    else:
        set_status_commit(args.conf)

if __name__ == "__main__":
    pass
