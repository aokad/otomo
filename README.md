[![Build Status](https://travis-ci.org/aokad/otomo.svg?branch=master)](https://travis-ci.org/aokad/otomo)
![Python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue.svg)

# otomo

## 1. Dependency

 - sqlite3
 - qacct (Sun Grid Engine)
 - parallel (Linux command)

## 2. Install

```Bash
git clone https://github.com/aokad/otomo.git
cd otomo
python setup.py build install
```

## 3. QuickStart

### 1) setup

create SQLiteDB
```
$ otomo setup --samples ${samples} --wdir ${gcat_workflow_work_dir}
```

### 2) Running Job

Set Sample Status
```
$ otomo sample ${sample} ${status} ${description}
```

 - status ...
    RUN/ERROR/STOP/SUCCESS/UPLOADED

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

options
 - -f: failure only
 - -b begin_time: jobs started after
 - --max NUMBER: limited display jobs

### 3) View Job Status

## 4. License 

See document [LICENSE](./LICENSE).
