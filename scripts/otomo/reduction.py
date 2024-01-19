import shutil
import os
import glob
import re
import otomo.CONFIG
import otomo.analysis_status

STOP_REASON =  {
    "sra_fastq_dump": {
        "item not found": ["str", "item not found while constructing within virtual database module"],
        "cmn_iter_open_db": ["str", "cmn_iter.c cmn_iter_open_db().VDBManagerOpenDBRead"],
        "removed": ["str", "object has been removed from distribution ( 403 )"],
        "wide_character": ["str", "Wide character in subroutine entry at /usr/bin/fasterq-dump line 764."],
        "malformed": ["str", "malformed UTF-8 character in JSON string, at character offset"],
        "parser_error": ["str", "Entity: line 1: parser error :"],
        "not_available_location": ["str", "The object is not available from your location. ( 406 )"],
        "name_not_found": ["str", "name not found while resolving query within virtual file system module - failed to resolve accession"],
        "cmn_read_String": ["str", "err: cmn_iter.c cmn_read_String"],
        "permission_denied": ["str", "unknown while reading file within file system module - unknown system error 'Permission denied(13)'"],
        "file_not_exist": ["str", "err: extract_acc2"],
        "read_len_zero": ["str", "err: sorter.c producer_thread_func: rec.read.len = 0"],
        "doesnt_exist": ["str", "no such file or directory"],
        "invalid_accession": ["str", "err: invalid accession"],
        "read_len_not_quality_len": ["re", r"err: row #.+ : READ\.len\([0-9]+\) != QUALITY\.len\([0-9]+\) \([A-Z]+\)"],
        "read_len_not_quality_len2": ["re", r"err: row #.+ : R\[[0-9]+\]\.len\([0-9]+\) != Q\[[0-9]+\]\.len\([0-9]+\)"],
        "read_len_not_quality_len3": ["re", r"err: row #.+ : Q\[[0-9]+\]\.len\([0-9]+\) \+ Q\[[0-9]+\]\.len\([0-9]+\) != Q\.len\([0-9]+\)"],
        "no_1_1fastq": ["str", "/1_1.fastq\n[E::stk_squeeze] failed to open the input file/stream."],
    },
    "star_alignment": {
        "short_read": ["str", "EXITING because of FATAL ERROR in reads input: short read sequence line: "],
        #"not_consistent": ["str", "EXITING because of FATAL ERROR: Read1 and Read2 are not consistent, reached the end of the one before the other one"],
        "not_consistent": ["str", "EXITING because of FATAL ERROR: read files are not consistent, reached the end of the one before the other one"],
        "not_equal": ["str", "EXITING because of FATAL ERROR in reads input: quality string length is not equal to sequence length"],
        "SJ_output_is_too_small": ["str", "EXITING because of fatal error: buffer size for SJ output is too small"],
        "unknown_file_format": ["str", "EXITING because of FATAL ERROR in input reads: unknown file format: the read ID should start with"],
    },
    "expression": {
        "zero_division": ["str", "ZeroDivisionError: float division by zero"],
    }
}

def __stop(sample, wdir):
    error = ""
    stop =""
    try:
        log_files = sorted(glob.glob("%s/log/%s/*.e*" % (wdir, sample)), key=lambda f: os.stat(f).st_mtime, reverse=True)
        if len(log_files) == 0:
            return (stop, error)
        
        last_log_file = log_files[0]
        stage = last_log_file.split("/")[-1].split(".")[0]
        
        f = open(last_log_file, encoding="utf-8", errors="replace")
        log = f.read()
        f.close()

        if not stage in STOP_REASON:
            return (stop, error)
        
        for key in STOP_REASON[stage]:
            stype = STOP_REASON[stage][key][0]
            text = STOP_REASON[stage][key][1]

            if stype == "re" and re.search(text, log, re.IGNORECASE):
                return ("%s:%s" % (stage, key), error)

            if stype == "str" and text in log:
                return ("%s:%s" % (stage, key), error)

    except Exception as e:
        error = str(e)
    return (stop, error)

def __remove(sample, stages, wdir, extend_dir=None):
    error = ""
    try:
        for stage in stages:
            shutil.rmtree("%s/%s/%s" % (wdir, stage, sample))
            os.makedirs("%s/%s/%s" % (wdir, stage, sample))
            if not extend is None:
                shutil.rmtree("%s/%s/%s" % (extend_dir, stage, sample))
        return error
    
    except Exception as e:
        error = str(e)
    return error

def main(args):
    """
    command line I/F : ステータスが "unresolv" のサンプルについて、
    1) ローカルの出力ファイルを削除する。ファイル削除失敗時、ステータスを "remove_error" に更新する
    2) ログファイルを元に解析不可能か判断し、解析不可能であればステータスを "stop" に更新する。
       判定失敗時、ステータスを "stop_error" に更新する。
       解析不可能でなければステータスを "analysis_error" に更新する。

    ※ "remove_error" > "stop_error" > "stop" > "analysis_error"
    """
    conf = otomo.CONFIG.load_conf(args.conf)
    stages = conf.get("reduction", "remove_dirs").split(",")
    wdir = conf.get("work", "dir")
    extend_dir = None
    if conf.has_option('work', 'extend_dir')
        extend_dir = conf.get("work", "extend_dir")

    samples = otomo.analysis_status.get_sample_w_status("failure")
    samples += otomo.analysis_status.get_sample_w_status("unresolv")
    for sample in samples:
        error_remove = ""
        if conf.getboolean("reduction", "enable"):
            error_remove = __remove(sample, stages, wdir, extend_dir)
        if error_remove != "":
            otomo.analysis_status.set_status_request(sample, "remove_error", error_text=error_remove)
        else:
            (stop_reason, error_stop) = __stop(sample, wdir)
            if error_stop != "":
                otomo.analysis_status.set_status_request(sample, "stop_error", error_text=error_stop)
            elif stop_reason != "":
                otomo.analysis_status.set_status_request(sample, "stop", stop_reason=stop_reason)
            else:
                otomo.analysis_status.set_status_request(sample, "analysis_error", error_text="")

    otomo.analysis_status.set_status_commit()

if __name__ == "__main__":
    pass
