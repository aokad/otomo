import shutil
import os
import otomo.CONFIG
import otomo.analysis_status

def __remove(sample, stages, wdir):
    error = ""
    try:
        for stage in stages:
            shutil.rmtree("%s/%s/%s" % (wdir, stage, sample))
            os.makedirs("%s/%s/%s" % (wdir, stage, sample))
        return error

    except Exception as e:
        error = str(e)
    return error

def main(args):
    conf = otomo.CONFIG.load_conf(args.conf)
    stages = conf.get("upload", "remove_dirs").split(",")
    wdir = conf.get("work", "dir")

    samples = otomo.analysis_status.get_sample_w_status("analysis_failure")
    for sample in samples:
        error_remove = __remove(sample, stages, wdir)
        if error_remove != "":
            otomo.analysis_status.set_status_w_sample(sample, "reduction_failure", error=error_remove)

if __name__ == "__main__":
    pass

