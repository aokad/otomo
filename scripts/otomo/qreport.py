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
    if b_time != None:
        where = "where start_time>='%s'" % (otomo.CONFIG.date_to_text(b_time))
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

def main(args):
    """
    command line I/F : Print the result of qreport
    """
    b_time = None
    if args.begin != "":
        b_time = datetime.datetime.strptime(args.begin, '%Y%m%d%H%M')
    data = __select(b_time, args.failed, args.max, args.conf)
    header = []
    for h in otomo.CONFIG.JOB_COLUMNS:
        header.append(h.split(" ")[0])
    print ("\t".join(header))
    for row in data:
        item = []
        for i in row:
            item.append(str(i))
        print("\t".join(item))

def __slice_jobcount(slice_time, conf_file):
    sql = "select count(jobname) from job where start_time<='{slice}' and end_time>='{slice}'".format(slice = otomo.CONFIG.date_to_text(slice_time))
    jobs = __query(sql, conf_file)
    return jobs[0][0]

def slice_jobcount_all(first_time = None, end_time = None, conf_file=otomo.CONFIG.DEFAULT_CONF):
    """
    指定時間に起動していたジョブ数をカウントする
    
    Parameters
    ----------
    first_time : datetime.datetime, default None
        カウント開始時間（なければデータの最初の時間）
    
    end_time : datetime.datetime, default None
        カウント終了時間（なければデータの最後の時間）
    
    conf_file : str, default otomo.CONFIG.DEFAULT_CONF
        Path to otomo.cfg
    
    Returns
    -------
    jobcounts : list
        [[sile_time1, job_count], [sile_time1, job_count], ...]
    """
    jobcounts = []
    if first_time == None:
        sql = "select start_time from job order by start_time limit 1"
        result = __query(sql, conf_file)
        first_time = datetime.datetime.strptime(result[0][0], '%Y/%m/%d %H:%M:%S')
    
    if end_time == None:
        end_time = datetime.datetime.now()
    
    passed_time = (end_time - first_time).total_seconds()
    for i in range(0, int(passed_time/60), 10):
        slice_time = first_time + datetime.timedelta(minutes=i)
        jobcounts.append([slice_time, __slice_jobcount(slice_time, conf_file)])
    
    #print(jobcounts)
    return jobcounts

if __name__ == "__main__":
    pass
