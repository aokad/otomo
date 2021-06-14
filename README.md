[![Build Status](https://api.travis-ci.com/aokad/otomo.svg?branch=master)](https://travis-ci.com/github/aokad/otomo)
![Python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue.svg)

# otomo

## 1. Dependency

 - awscli
 - boto3
 - sqlite3
 - requests
 - qacct (Sun Grid Engine)
 - parallel (Linux command)

## 2. Install

```Bash
git clone https://github.com/aokad/otomo.git
cd otomo
python setup.py build install
```

Set aws account (If you want to upload output files to aws S3)
```
aws configure
...
```

## 3. QuickStart

### 1) setup

Create SQLiteDB
```
$ otomo setup --wdir ${gcat_workflow_work_dir}
```

vi config file (option)
```
$ vi ~/.otomo.cfg

[notify]
slack_url = 
channel = 
label = 

[upload]
endpoint_url = 
profile = 
```

Add samples
```
$ otomo regsample --samples ${samples.json}
```

```
$ cat ${samples.json}
{
    "ERP001942_ERR205022" :
    {
        "study": "ERP001942",
        "runid": "ERR205022",
        "upload": 
        {
            "expression/ERP001942_ERR205022/ERP001942_ERR205022.txt.fpkm":                 s3://BUCKET/sra/expression/ERP001942_ERR205022/ERP001942_ERR205022.txt.fpkm,
            "expression/ERP001942_ERR205022/ERP001942_ERR205022.txt.gz":                   s3://BUCKET/sra/expression/ERP001942_ERR205022/ERP001942_ERR205022.txt.gz,
            "expression/ERP001942_ERR205022/ERP001942_ERR205022.txt.summary":              s3://BUCKET/sra/expression/ERP001942_ERR205022/ERP001942_ERR205022.txt.summary,
            "ir_count/ERP001942_ERR205022/ERP001942_ERR205022.ir_simple_count.txt.gz":     s3://BUCKET/sra/ir_count/ERP001942_ERR205022/ERP001942_ERR205022.ir_simple_count.txt.gz,
            "ir_count/ERP001942_ERR205022/ERP001942_ERR205022.ir_simple_count.txt.gz.tbi": s3://BUCKET/sra/ir_count/ERP001942_ERR205022/ERP001942_ERR205022.ir_simple_count.txt.gz.tbi,
            "iravnet/ERP001942_ERR205022/ERP001942_ERR205022.iravnet.filt.bam":            s3://BUCKET/sra/iravnet/ERP001942_ERR205022/ERP001942_ERR205022.iravnet.filt.bam,
            "iravnet/ERP001942_ERR205022/ERP001942_ERR205022.iravnet.filt.bam.bai":        s3://BUCKET/sra/iravnet/ERP001942_ERR205022/ERP001942_ERR205022.iravnet.filt.bam.bai,
            "iravnet/ERP001942_ERR205022/ERP001942_ERR205022.iravnet.filt.vcf":            s3://BUCKET/sra/iravnet/ERP001942_ERR205022/ERP001942_ERR205022.iravnet.filt.vcf,
            "iravnet/ERP001942_ERR205022/ERP001942_ERR205022.iravnet.vcf":                 s3://BUCKET/sra/iravnet/ERP001942_ERR205022/ERP001942_ERR205022.iravnet.vcf,
            "juncmut/ERP001942_ERR205022/ERP001942_ERR205022.juncmut.filt.bam":            s3://BUCKET/sra/juncmut/ERP001942_ERR205022/ERP001942_ERR205022.juncmut.filt.bam,
            "juncmut/ERP001942_ERR205022/ERP001942_ERR205022.juncmut.filt.bam.bai":        s3://BUCKET/sra/juncmut/ERP001942_ERR205022/ERP001942_ERR205022.juncmut.filt.bam.bai,
            "juncmut/ERP001942_ERR205022/ERP001942_ERR205022.juncmut.txt":                 s3://BUCKET/sra/juncmut/ERP001942_ERR205022/ERP001942_ERR205022.juncmut.txt,
            "star/ERP001942_ERR205022/ERP001942_ERR205022.Log.final.out":                  s3://BUCKET/sra/star/ERP001942_ERR205022/ERP001942_ERR205022.Log.final.out,
            "star/ERP001942_ERR205022/ERP001942_ERR205022.Log.out":                        s3://BUCKET/sra/star/ERP001942_ERR205022/ERP001942_ERR205022.Log.out,
            "star/ERP001942_ERR205022/ERP001942_ERR205022.Log.progress.out":               s3://BUCKET/sra/star/ERP001942_ERR205022/ERP001942_ERR205022.Log.progress.out,
            "star/ERP001942_ERR205022/ERP001942_ERR205022.SJ.out.tab.gz":                  s3://BUCKET/sra/star/ERP001942_ERR205022/ERP001942_ERR205022.SJ.out.tab.gz,
        },
    },
...
}
```

### 2) Running Job

Set Sample Status
```
$ otomo sample ${sample} ${status} ${description}
```

 - status ...
    init/run/analysis_failure/stop/success/finish/upload_failure/remove_failure

 - decsription [OPTION]

Set Job Status
```
$ qacct -j "*" -o USER -d 1 > ./qacct.txt
$ otomo regjob --qacct ./qacct.txt
```

### 3) Job Report

```
$ otomo qreport ${option}
```

Options
 - -f: failure only
 - -b begin_time: jobs started after
 - --max NUMBER: limited display jobs

## 4. License 

See document [LICENSE](./LICENSE).
