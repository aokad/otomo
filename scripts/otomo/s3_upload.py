import shutil
import sqlite3
import boto3
import otomo.CONFIG
import otomo.analysis_status

def __path(db, sample):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("select output,uri from upload where sample='%s'" % sample)

    pathes = []
    for f in cur.fetchall():
        pathes.append((f[0], f[1]))

    con.close()
    return pathes

def __upload(wdir, pathes, endpoint_url, profile):
    if endpoint_url == "":
        endpoint_url = None
    if profile == "":
        profile = None

    error = ""
    try:
        session = boto3.session.Session(profile_name=profile)
        client = session.client("s3", endpoint_url=endpoint_url)

        for path in pathes:
            path1 = path[1].replace("s3://", "")
            path1_bucket = path1.split("/")[0]
            path1_key = path1.replace(path1_bucket + "/", "", 1)
            client.upload_file("%s/%s" % (wdir, path[0]), path1_bucket, path1_key)
        return error

    except Exception as e:
        error = str(e)
    return error

def __remove(sample, stages, wdir):
    error = ""
    try:
        for stage in stages:
            shutil.rmtree("%s/%s/%s" % (wdir, stage, sample))
        return error

    except Exception as e:
        error = str(e)
    return error

def main(args):

    conf = otomo.CONFIG.load_conf(args.conf)
    upload_db = conf.get("db", "upload_db")
    endpoint_url = conf.get("upload", "endpoint_url")
    profile = conf.get("upload", "profile")
    stages = conf.get("upload", "remove_dirs").split(",")
    wdir = conf.get("work", "dir")

    samples = otomo.analysis_status.get_sample_w_status("success", limit=args.max)
    for sample in samples:
        pathes = __path(upload_db, sample)
        error_upload = __upload(wdir, pathes, endpoint_url, profile)
        if error_upload == "":
            error_remove = __remove(sample, stages, wdir)
            if error_remove == "":
                otomo.analysis_status.set_status_request(sample, "finish")
            else:
                otomo.analysis_status.set_status_request(sample, "remove_error", error_text=error_remove)
        else:
            otomo.analysis_status.set_status_request(sample, "upload_error", error_text=error_upload)

    otomo.analysis_status.set_status_commit()

if __name__ == "__main__":
    pass

