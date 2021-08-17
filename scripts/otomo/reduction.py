import shutil
import os
import glob
import otomo.CONFIG
import otomo.analysis_status

STOP_REASON =  {
    "sra_fastq_dump": {
        "item not found": "item not found while constructing within virtual database module",
        "cmn_iter_open_db": "cmn_iter.c cmn_iter_open_db().VDBManagerOpenDBRead",
        "removed": "object has been removed from distribution ( 403 )",
        "wide_character": "Wide character in subroutine entry at /usr/bin/fasterq-dump line 764.",
        "malformed": "malformed UTF-8 character in JSON string, at character offset",
        "parser_error": "Entity: line 1: parser error :",
        "not_available_location": "The object is not available from your location. ( 406 )",
        "name_not_found": "name not found while resolving query within virtual file system module - failed to resolve accession",
        "cmn_read_String": "err: cmn_iter.c cmn_read_String",
        "permission_denied": "unknown while reading file within file system module - unknown system error 'Permission denied(13)'",
        "file_not_exist": "err: extract_acc2",
        "read_len_zero": "err: sorter.c producer_thread_func: rec.read.len = 0",
        "doesnt_exist": "no such file or directory",
        "invalid_accession": "err: invalid accession",
    },
    "star_alignment": {
        "short_read": "EXITING because of FATAL ERROR in reads input: short read sequence line: ",
        "not_consistent": "EXITING because of FATAL ERROR: Read1 and Read2 are not consistent, reached the end of the one before the other one",
        "not_equal": "EXITING because of FATAL ERROR in reads input: quality string length is not equal to sequence length",
        "SJ_output_is_too_small": "EXITING because of fatal error: buffer size for SJ output is too small",
        "unknown_file_format": "EXITING because of FATAL ERROR in input reads: unknown file format: the read ID should start with",
    },
    "expression": {
        "zero_division": "ZeroDivisionError: float division by zero"
    }
}

def __stop(sample, wdir):
    
    log_files = sorted(glob.glob("%s/log/%s/*.e*" % (wdir, sample)), key=lambda f: os.stat(f).st_mtime, reverse=True)
    if len(log_files) == 0:
        return ""
    
    last_log_file = log_files[0]
    stage = last_log_file.split("/")[-1].split(".")[0]
    
    f = open(last_log_file)
    log = f.read()
    f.close()

    if not stage in STOP_REASON:
        return ""
    
    for key in STOP_REASON[stage]:
        if STOP_REASON[stage][key] in log:
            return "%s:%s" % (stage, key)
    
    return ""

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
    """
    command line I/F : ステータスが "failure" のサンプルについて、
    1) ログファイルを元に解析不可能か判断し、解析不可能であればステータスを "stop" に更新する。
       解析不可能でなければステータスを "analysis_error" に更新する。
    2) ローカルの出力ファイルを削除する。ローカルの出力ファイル削除に失敗した場合、ステータスを "remove_error" に更新する
    ※ "remove_error" > ("analysis_error", "stop")
    """
    conf = otomo.CONFIG.load_conf(args.conf)
    stages = conf.get("upload", "remove_dirs").split(",")
    wdir = conf.get("work", "dir")

    samples = otomo.analysis_status.get_sample_w_status("failure")
    for sample in samples:
        try:
            stop_reason = __stop(sample, wdir)
            if stop_reason != "":
                otomo.analysis_status.set_status_request(sample, "stop", stop_reason=stop_reason)
        except Exception as e:
            stop_reason = str(e)
            otomo.analysis_status.set_status_request(sample, "stop_error", error_text=stop_reason)

        error_remove = __remove(sample, stages, wdir)
        if error_remove != "":
            otomo.analysis_status.set_status_request(sample, "remove_error", error_text=error_remove)

        if stop_reason == "" and error_remove == "":
            otomo.analysis_status.set_status_request(sample, "analysis_error")

    otomo.analysis_status.set_status_commit()
if __name__ == "__main__":
    pass
