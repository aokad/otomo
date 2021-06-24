import datetime
import sqlite3
import otomo.CONFIG

def get(table, conf_file=otomo.CONFIG.DEFAULT_CONF):
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "monitor_db")

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select *from %s order by timestamp" % (table))
    h = cur.fetchall()
    con.close()
    return h

def insert(table, data, conf_file=otomo.CONFIG.DEFAULT_CONF):
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "monitor_db")

    con = sqlite3.connect(db, isolation_level='EXCLUSIVE')
    cur = con.cursor()
    cur.executemany("insert into %s values (?, ?)" % (table), data)
    con.commit()
    con.close()

if __name__ == "__main__":
    _main('./qacct.txt')

