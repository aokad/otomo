import requests
import json
import otomo.CONFIG

def main(args):
    data = open(args.quota).read().split("\n")
    val = 0.0
    for row in data:
        name = ""
        for d in row.strip().split(" "):
            if d == "":
                continue
            if name == "":
                name = d
                continue
            val += float(d)/1024/1024/1024
            break
    
    if val > 0:
        conf = otomo.CONFIG.load_conf(args.conf)
        slack_url = conf.get("notify", "slack_url")
        label = conf.get("notify", "label")
        channel = conf.get("notify", "channel")
        message = "[%s] disk usage is %.1f (Tbyte)" % (label, val)
        
        payload_dic = {
            "text": message,
            "channel": channel
        }
        requests.post(slack_url, data=json.dumps(payload_dic))

if __name__ == "__main__":
    pass
