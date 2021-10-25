import requests
import json
import otomo.CONFIG

def main(args):
    """
    command line I/F : Notify message to slack
    """
    message = open(args.message_file).read()
    if message != "":
        conf = otomo.CONFIG.load_conf(args.conf)
        channel = conf.get("notify", "channel")
        
        payload_dic = {
            "text": message,
            "channel": channel
        }
        requests.post(slack_url, data=json.dumps(payload_dic))

if __name__ == "__main__":
    pass
