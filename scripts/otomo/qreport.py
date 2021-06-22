import datetime
import sqlite3
import otomo.CONFIG

def __query(sql, conf_file):
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "job_db")
    
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(sql)
    
    ret = cur.fetchall()
    con.close()
    return ret

def __select(b_time, fail, max, conf_file):
    sql = "select * from job"
    
    where = ""
    if b_time != "":
        where = "where start_time>='%s'" % (__text_to_date(b_time))
    if fail:
        if where != "":
            where += " and failed=1"
        else:
            where = "where failed=1"
    if where != "":
        sql += " " + where
    
    if max > 0:
        sql += " limit %d" % (max)
    
    return __query(sql, conf_file)

def __text_to_date(text):
    dt = datetime.datetime.strptime(text, '%Y%m%d%H%M')
    return dt.strftime('%Y/%m/%d %H:%M:%S')

def select(b_time = "", fail = False, max = 0, conf=otomo.CONFIG.DEFAULT_CONF):
    return __select(b_time, fail, max, conf)

def main(args):
    data = __select(args.begin, args.failed, args.max, args.conf)
    header = []
    for h in otomo.CONFIG.JOB_COLUMNS:
        header.append(h.split(" ")[0])
    print ("\t".join(header))
    for row in data:
        item = []
        for i in row:
            item.append(str(i))
        print("\t".join(item))

def slice_jobcount(slice_time, conf=otomo.CONFIG.DEFAULT_CONF):
    sql = "select count(jobname) from job where start_time<='{slice}' and end_time>='{slice}'".format(slice = __text_to_date(slice_time))
    jobs = __query(sql, conf)
    return jobs[0][0]

def slice_jobcount_all(first_time = "", end_time = "", conf=otomo.CONFIG.DEFAULT_CONF):
    jobcounts = []
    if first_time == "":
        sql = "select start_time from job order by start_time limit 1"
        result = __query(sql, conf)
        first_time = datetime.datetime.strptime(result[0][0], '%Y/%m/%d %H:%M:%S')
    else:
        first_time = datetime.datetime.strptime(first_time, '%Y%m%d%H%M%S')
    
    if end_time == "":
        end_time = datetime.datetime.now()
    else:
        end_time = datetime.datetime.strptime(end_time, '%Y%m%d%H%M%S')

    passed_time = (end_time - first_time).total_seconds()
    for i in range(0, int(passed_time/60), 10):
        slice_time = first_time + datetime.timedelta(minutes=i)
        jobcounts.append([slice_time, slice_jobcount(slice_time.strftime('%Y%m%d%H%M'), conf)])

#    print(jobcounts)
    return jobcounts

if __name__ == "__main__":
    pass
