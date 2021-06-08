import datetime
import sqlite3
import otomo.CONFIG

def __select(b_time, fail, max):
    conf = otomo.CONFIG.load_conf()
    db = conf.get("db", "job_db")

    sql = "select * from job"

    where = ""
    if b_time != "":
        where = "where start_time>=" + b_time
    if fail:
        if where != "":
            where += " and failed=1"
        else:
            where = "where failed=1"
    if where != "":
        sql += " " + where

    if max > 0:
        sql += " limit %d" % (max)

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(sql)
    
    ret = cur.fetchall()
    con.close()
    return ret

def __text_to_date(text):
    dt = datetime.datetime.strptime(text, '%Y%m%d%H%M')
    return dt.strftime('%Y/%m/%d %H:%M:%S')

def select(b_time = "", fail = False, max = 0):
    return __select(b_time, fail, max)

def main(args):
    data = __select(args.begin, args.failed, args.max)
    print ("\t".join(otomo.CONFIG.JOB_COLMUNS))
    for row in data:
        item = []
        for i in row:
            item.append(str(i))
        print("\t".join(item))

if __name__ == "__main__":
    pass
