import sqlite3
import datetime
import json
import glob
import os
import otomo.CONFIG

def get_sample_w_status(status, limit = 0, conf_file=otomo.CONFIG.DEFAULT_CONF):
    """
    指定されたステータスのサンプルを取得する
    
    Parameters
    ----------
    status : str
        ステータス
    
    limit : int, default 0
        最大値 (0の場合は無制限)
    
    conf_file : str, default otomo.CONFIG.DEFAULT_CONF
        Path to otomo.cfg
    
    Returns
    -------
    count : list
    """
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "analysis_db")

    sql_limit = ""
    if limit > 0:
        sql_limit = "limit %d" % (limit)

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select sample from analysis where status=:status %s" % (sql_limit), {"status": status})
    
    samples = []
    for f in cur.fetchall():
        samples.append(f[0])

    con.close()
    return samples

def get_sample_count_groupby_status_stage(conf_file=otomo.CONFIG.DEFAULT_CONF):
    """
    ステータスごとステージごとのサンプルをカウントする
    
    Parameters
    ----------
    conf_file : str, default otomo.CONFIG.DEFAULT_CONF
        Path to otomo.cfg
    
    Returns
    -------
    count : dic
        {STATUS1: {STAGE1: num, STAGE2: num}, STATUS2: {STAGE1: num, STAGE2: num}, ...}
    """
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "analysis_db")
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select status,stage,count(sample) from analysis group by status,stage")
    
    ret = {}
    for status,stage,count in cur.fetchall():
        if not status in ret:
            ret[status] = {}
        if not stage in ret[status]:
            ret[status][stage] = count
    
    con.close()
    return ret

def get_sample_count_groupby_stop_reason(conf_file=otomo.CONFIG.DEFAULT_CONF):
    """
    停止（解析不可）したサンプルについて、その理由ごとのサンプル数をカウントする
    
    Parameters
    ----------
    conf_file : str, default otomo.CONFIG.DEFAULT_CONF
        Path to otomo.cfg
    
    Returns
    -------
    count : dic
        {REASON1: num, REASON2: num, ...}
    """
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "analysis_db")
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select stop_reason,count(sample) from analysis group by stop_reason")

    ret = {}
    for stop_reason,count in cur.fetchall():
        if stop_reason == "": continue
        ret[stop_reason] = count
    con.close()
    return ret

def get_run_count_w_sample(sample, conf_file=otomo.CONFIG.DEFAULT_CONF):
    """
    指定されたサンプルの実行回数を取得する
    
    Parameters
    ----------
    sample : str
        サンプルID
    
    conf_file : str, default otomo.CONFIG.DEFAULT_CONF
        Path to otomo.cfg
    
    Returns
    -------
    count : {}
        {SAMPLE1: num, SAMPLE2: num, ...}
    """
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "sample_stage_db")

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select stage,count(*) from sample_stage where sample=:sample group by stage", {"sample": sample})

    count = {}
    for f in cur.fetchall():
        count[f[0]] = f[1]
    
    con.close()
    return count

def set_status_request(sample, status, stage = "", error_text = "", stop_reason = "", note = "", conf_file=otomo.CONFIG.DEFAULT_CONF):
    """
    analyis-DB への更新依頼を作成する
    
    Parameters
    ----------
    sample : str
        ステータス
    
    status : str
        ステータス
    
    stage : str, default ""
        解析ステージ ("" の場合はstageを更新しない)
    
    error_text :str, default ""
        エラー情報 ("" の場合はerror_textを更新しない)
    
    stop_reason : str, default ""
        解析不可能な理由 ("" の場合はstop_reasonを更新しない)
    
    
    conf_file : str, default otomo.CONFIG.DEFAULT_CONF
        Path to otomo.cfg
    """
    conf = otomo.CONFIG.load_conf(conf_file)
    
    now = datetime.datetime.now()
    label_time = now.strftime('%Y%m%d_%H%M%S%f')
    db_time = otomo.CONFIG.date_to_text(now)

    write_data = {
        "sample": sample,
        "last_update": db_time
    }
    if status != "":
        write_data["status"] = status

    def __set_sample_job_request():
        write_data = {
            "sample": sample,
            "stage": stage,
            "status": status,
            "start_time": db_time
        }
        temp_name = "%s/sample_stage_%s_%s.json" % (conf.get("db", "request_dir"), label_time, sample)
        fw = open(temp_name, "w")
        json.dump(write_data, fw)
        fw.close()

    if stage != "":
        write_data["stage"] = stage
        __set_sample_job_request()

    if error_text != "":
        write_data["error_text"] = error_text

    if stop_reason != "":
        write_data["stop_reason"] = stop_reason

    if note != "":
        write_data["note"] = note

    temp_name = "%s/analysis_%s_%s.json" % (conf.get("db", "request_dir"), label_time, sample)
    fw = open(temp_name, "w")
    json.dump(write_data, fw)
    fw.close()

def set_status_commit(conf_file=otomo.CONFIG.DEFAULT_CONF):
    """
    analyis-DB への更新依頼をコミットする
    
    Parameters
    ----------
    conf_file : str, default otomo.CONFIG.DEFAULT_CONF
        Path to otomo.cfg
    """
    # analysis db
    conf = otomo.CONFIG.load_conf(conf_file)
    db = conf.get("db", "analysis_db")
    requests = sorted(glob.glob("%s/analysis_*.json" % (conf.get("db", "request_dir"))))
    sqls = []
    commited_requests = []
    for i,request in enumerate(requests):
        #if i >= 1000:
        #    break
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

    if len(sqls) > 0:
        error = None
        try:
            con = sqlite3.connect(db, isolation_level='EXCLUSIVE')
            cur = con.cursor()
            for sql in sqls:
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

    # sample_stage db
    db = conf.get("db", "sample_stage_db")
    requests = sorted(glob.glob("%s/sample_stage_*.json" % (conf.get("db", "request_dir"))))
    insert_list = []
    commited_requests = []
    for i,request in enumerate(requests):
        #if i >= 1000:
        #    break
        f = open(request)
        data = json.load(f)
        f.close()
        insert_list.append((data["sample"], data["stage"], data["status"], data["start_time"]))
        commited_requests.append(request)

    if len(insert_list) > 0:
        error = None
        try:
            con = sqlite3.connect(db, isolation_level='EXCLUSIVE')
            cur = con.cursor()
            cur.executemany("insert into sample_stage values (?, ?, ?, ?)", insert_list)
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
    """
    command line I/F : analyis-DB のサンプル毎のステータスを更新する
    """
    if args.commit == False:
        set_status_request(
            args.sample, 
            args.status, 
            stage = args.stage, 
            error_text = args.error_text, 
            stop_reason = args.stop_reason, 
            note = args.note, 
            conf_file=args.conf
        )
    else:
        set_status_commit(args.conf)

if __name__ == "__main__":
    pass
