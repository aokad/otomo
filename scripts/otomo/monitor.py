import datetime
import sqlite3
import otomo.CONFIG

def get(table, conf_file=otomo.CONFIG.DEFAULT_CONF):
    """
    Get all the contents of a specified table from the monitor DB.
    
    Parameters
    ----------
    table : str
        Table name
    
    conf_file : str, default otomo.CONFIG.DEFAULT_CONF
        Path to otomo.cfg
    
    Returns
    -------
    h : list
        [(timestamp, value), (timestamp, value), ...]
    """
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "monitor_db")

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select *from %s order by timestamp" % (table))
    h = cur.fetchall()
    con.close()
    return h

def insert(table, data, conf_file=otomo.CONFIG.DEFAULT_CONF):
    """
    Insert data to a specified table in the monitor DB.
    
    Parameters
    ----------
    table : str
        Table name
    
    data : list
        Insert data [(timestamp, value), (timestamp, value), ...]
        An error occurs if the same timestamp is already registered.

    conf_file : str, default otomo.CONFIG.DEFAULT_CONF
        Path to otomo.cfg
    """
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "monitor_db")

    con = sqlite3.connect(db, isolation_level='EXCLUSIVE')
    cur = con.cursor()
    cur.executemany("insert into %s values (?, ?)" % (table), data)
    con.commit()
    con.close()

if __name__ == "__main__":
    pass

