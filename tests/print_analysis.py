import sqlite3
import otomo.CONFIG
import sqlite3
import otomo.CONFIG

conf = otomo.CONFIG.load_conf(otomo.CONFIG.DEFAULT_CONF)
db = conf.get("db", "analysis_db")

con = sqlite3.connect(db)
cur = con.cursor()
cur.execute("select * from analysis limit 30")

data = []
header = []
for h in otomo.CONFIG.ANALYSIS_COLUMUNS:
    header.append(h.split(" ")[0])
data.append("\t".join(header))

for row in cur.fetchall():
    text = []
    for i in row:
        text.append(str(i))
    data.append("\t".join(text))

con.close()
print("\n".join(data))
