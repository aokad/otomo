# build pydoc

## check NumDoc

NumPyスタイルのdocstringをチェックしてくれるLintを作りました。  
https://qiita.com/simonritchie/items/84c4d4b2528309c30359

install
```
pip install numdoclint
```

check_numdoc.py
```
import numdoclint
lint_info_list = numdoclint.check_python_module_recursively("../scripts/otomo/")
lint_info_list
```

main関数と private 関数は良しとする。
```
python check_numdoc.py | egrep -v __ | egrep -v main | grep :: | sort | uniq
```

## build
```
pydoc -w otomo otomo.CONFIG otomo.analysis_status otomo.monitor otomo.qreport  otomo.regist_sample otomo.setup
```

otomo.html の<table width="100%" summary="list">タグ以降を以下内容で更新

```
<table width="100%" summary="list">
<tr><td width="100%" valign=top>
<a href="otomo.CONFIG.html">CONFIG</a><br>
<a href="otomo.analysis_status.html">analysis_status</a><br>
<a href="otomo.monitor.html">monitor</a><br>
<a href="otomo.qreport.html">qreport</a><br>
<a href="otomo.regist_sample.html">regist_sample</a><br>
<a href="otomo.setup.html">setup</a><br>
</td></tr></table></td></tr></table>
</body></html>
```
