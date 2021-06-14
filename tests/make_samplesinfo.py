"""
サンプルシート作成手順
必要なもの
 - サンプルシート作成時に出力したサンプルリスト.txt (Study_RunID)

python ./make_sampleinfo.py samples.txt s3://UPLOAD-BUCKET/subdir

出力されるもの
 - サンプルinfo.json

"""

import sys
SAMPLE = sys.argv[1]
S3_PREFIX = sys.argv[2]

uploads = {}
for sample in open(SAMPLE).read().split("\n"):
    if sample == "":
        continue

    expected_files = [
        "expression/%s/%s.txt.fpkm" % (sample, sample),
        "expression/%s/%s.txt.gz" % (sample, sample),
        "expression/%s/%s.txt.summary" % (sample, sample),
        "ir_count/%s/%s.ir_simple_count.txt.gz" % (sample, sample),
        "ir_count/%s/%s.ir_simple_count.txt.gz.tbi" % (sample, sample),
        "iravnet/%s/%s.iravnet.filt.bam" % (sample, sample),
        "iravnet/%s/%s.iravnet.filt.bam.bai" % (sample, sample),
        "iravnet/%s/%s.iravnet.filt.vcf.gz" % (sample, sample),
        "iravnet/%s/%s.iravnet.vcf" % (sample, sample),
        "iravnet/%s/%s.iravnet.vcf.gz.tbi" % (sample, sample),
        "juncmut/%s/%s.juncmut.filt.bam" % (sample, sample),
        "juncmut/%s/%s.juncmut.filt.bam.bai" % (sample, sample),
        "juncmut/%s/%s.juncmut.txt" % (sample, sample),
        "star/%s/%s.Log.final.out" % (sample, sample),
        "star/%s/%s.Log.out" % (sample, sample),
        "star/%s/%s.Log.progress.out" % (sample, sample),
        "star/%s/%s.SJ.out.tab.gz" % (sample, sample),
    ]
    
    upload_files = {}
    for key in expected_files:
        upload_files[key] = "%s/%s" % (S3_PREFIX.rstrip("/"), key)
    
    (study, runid) = sample.split("_")
    uploads[sample] = {
        "study": study,
        "runid": runid,
        "upload": upload_files
    }

import json
fw = open(SAMPLE.replace(".txt", ".json"), "w")
json.dump(uploads, fw, ensure_ascii=False, indent=4, separators=(',', ': '))
fw.close()
