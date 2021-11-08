import os
import datetime
import glob
import json
import sqlite3
import otomo.CONFIG

def __exists(taskname, db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select count(taskname) from ecsub where taskname=:taskname",
        {"taskname": taskname}
    )
    
    ret = True
    if cur.fetchall()[0][0] == 0:
        ret = False
    con.close()
    return ret

def __text_to_date(text):
    return datetime.datetime.strptime(text, '%m/%d/%Y %H:%M:%S.%f')

def __insert(data, db):
    item = []
    for col in otomo.CONFIG.ECSUB_COLUMNS:
        key = col.split(" ")[0]
        if key in data:
            item.append(data[key])
        else:
            item.append("")

    con = sqlite3.connect(db, isolation_level='EXCLUSIVE')
    cur = con.cursor()
    cur.execute("insert into ecsub values (" + ",".join(["?"] * len(item)) + ")", item)
    con.commit()
    con.close()

def __update(data, db):
    item = []
    for key in data:
        if key in ["taskname", "taskid"]:
            continue
        item.append("%s=:%s" % (key, key))
    
    con = sqlite3.connect(db, isolation_level='EXCLUSIVE')
    cur = con.cursor()
    cur.execute("update ecsub set %s where taskname=:taskname and taskid=:taskid" % (",".join(item)), data)
    con.commit()
    con.close()

def __get_max_metrics(file_path):
    values = []
    header = True
    for row in open(file_path).read().split("\n"):
        if row == "": continue
        if header:
            header = False
            continue
        values.append(int(row.split("\t")[2]))
    return max(values)

def upsert_job(taskname, conf_file):

    conf = otomo.CONFIG.load_conf(conf_file)
    ecsub_dir = conf.get("work", "ecsub_dir")
    task_dir = "%s/%s" % (ecsub_dir, taskname)
    if not os.path.exists(task_dir):
        return

    db = conf.get("db", "ecsub_db")

    task_definition = json.load(open(task_dir + "/conf/task_definition.json"))
    for overrides_json in sorted(glob.glob(task_dir + "/conf/containerOverrides.*.json")):
        taskid = overrides_json.split(".")[-2]
        data = {
            "taskname": taskname,
            "taskid": taskid,
            "image": task_definition["containerDefinitions"][0]["image"],
            "goofys": task_definition["containerDefinitions"][0]["privileged"],
            "status": "run"
        }
        exit_code = -1
        overrides = json.load(open(overrides_json))
        data["cpu"] = overrides["containerOverrides"][0]["cpu"]
        data["memory"] = overrides["containerOverrides"][0]["memory"]

        specification = json.load(open(overrides_json.replace("containerOverrides", "specification_file")))
        data["disk_size"] = specification["BlockDeviceMappings"][0]["Ebs"]["VolumeSize"]
        data["instance_type"] = specification["InstanceType"]
        data["region"] = specification["Placement"]["AvailabilityZone"]
        
        data["spot"] = len(glob.glob(task_dir + "/log/request-spot-instances.%s.*.log" % (taskid))) > 0

        start_task = sorted(glob.glob(task_dir + "/log/start-task.%s.*.log" % (taskid)))
        if len(start_task) > 0:
            dt1 = datetime.datetime.fromtimestamp(os.stat(start_task[-1]).st_mtime)
            data["start_time"] = otomo.CONFIG.date_to_text(dt1)

            describe_task = sorted(glob.glob(task_dir + "/log/describe-tasks.%s.*.log" % (taskid)))
            if len(describe_task) > 0:
                task = json.load(open(describe_task[-1]))
                if task["tasks"][0]["lastStatus"] == "STOPPED":
                    dt2 = datetime.datetime.fromtimestamp(os.stat(describe_task[-1]).st_mtime)
                    data["end_time"] = otomo.CONFIG.date_to_text(dt2)
                    data["run_time_h"] = "%.2f" % ((dt2-dt1).total_seconds() / 3600)
                    exit_code = task["tasks"][0]["containers"][0]["exitCode"]

        metrics_count = 0
        path = task_dir + "/metrics/%d-CPUUtilization.txt" % (int(taskid))
        if os.path.exists(path):
            data["max_pct_cpu_util"] = __get_max_metrics(path)
            metrics_count += 1

        path = task_dir + "/metrics/%d-MemoryUtilization.txt" % (int(taskid))
        if os.path.exists(path):
            data["max_pct_memory_util"] = __get_max_metrics(path)
            metrics_count += 1

        path = task_dir + "/metrics/%d-DataStorageUtilization.txt" % (int(taskid))
        if os.path.exists(path):
            data["max_pct_disk_util"] = __get_max_metrics(path)
            metrics_count += 1

        if metrics_count == 3:
            if exit_code == 0:
                data["status"] = "success"
            else:
                data["status"] = "failure" 

        if __exists(taskname, db):
            __update(data, db)
        else:
            __insert(data, db)

def main(args):
    upsert_job(args.taskname, args.conf)

if __name__ == "__main__":
    upsert_job("task_acc_1_10-0rxLA", otomo.CONFIG.DEFAULT_CONF)

