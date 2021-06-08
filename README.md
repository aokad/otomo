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
$ otomo setup ${gcat_workflow_work_dir} ${samples}
```

### 2) Running Job

Set Job Status
```
$ otomo sample ${sample} ${status} ${description}
```

 - status ...
    RUN/ERROR/STOP/SUCCESS/UPLOADED

 - decsription [OPTION]

### 3) Job Report

```
$ otomo qreport ${option}
```

-f: failure only
-b begin_time: jobs started after


### 3) View Job Status

## 4. License 

See document [LICENSE](./LICENSE).
