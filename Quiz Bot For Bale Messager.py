from urllib.request import urlopen, Request
import json
from time import sleep
import random
import os

class Bot():
    def __init__(self, token: str):
        self.token = token
        self.get_url = "https://tapi.bale.ai/bot{}/getUpdates".format(token)
        self.send_url = "https://tapi.bale.ai/bot{}/sendMessage".format(token)

    def get_updates(self):
        with urlopen(self.get_url) as resp:
            return json.loads(resp.read())

    def send_message(self, data):
        req = Request(self.send_url, method='POST')
        req.add_header('Content-Type', 'application/json')
        with urlopen(req, data=data) as resp:
            return json.loads(resp.read())

# Initialize Bot instance
bot = Bot("1556200068:hmUx6SotFjkDvsQCEuDOmV8IMM5yqTtpMdnbAXdz")

questions = [
    {'question': 'پایتخت کشور سوئیس کجاست؟',
        'choices': ['زوریخ', 'برن', 'وین'],
        'answer': 1},
    {'question': 'کدام کشور بیشترین تولید پسته را در جهان دارد؟',
        'choices': ['آمریکا', 'ترکیه', 'ایران'],
        'answer': 0},
    {'question': 'بهترین فوتبالیست دنیا کیست؟',
        'choices': ['مسی', 'رونالدو','نیمار'],
        'answer': 0},
    {'question': 'پایتخت ایران کجاست؟',
        'choices': ['مشهد','تهران', 'اصفهان'],
        'answer': 1}
]

count = 0
ids = set()
info = dict()

# Check if data.json exists and create if it doesn't
if not os.path.exists("data.json"):
    with open("data.json", "w") as file:
        data = {"count": count, "info": info, 'ids': list(ids)}
        json.dump(data, file)

while True:
    s = bot.get_updates()
    length = len(s["result"])

    # Read data from the file
    with open("data.json", "r") as file:
        d = json.load(file)

    count = d['count']
    info = d["info"]
    ids = set(d['ids'])

    if count == length:
        pass
    elif count < length:
        diff = length - count
        for i in range(diff):
            idx = count
            a = s["result"][idx]
            z = str(a["message"]["from"]["id"])
            r = a["message"]["text"]
            if not z in ids:
                ids.add(z)
                info[z] = {"score": 0, "shown_q": [], "last_answered": True}

            if r == "/start":
                # Reset the user's progress
                info[z] = {"score": 0, "shown_q": [], "last_answered": True}
            
            if r == "/start" or (r.isdigit() and r in ["1", "2", "3"]):
                remain_index = [i for i in range(len(questions)) if i not in info[z]["shown_q"]]
                
                if len(remain_index) < 1:
                    data = {
                        "chat_id": z,
                        "text": "all shown!"
                    }
                    data = json.dumps(data)
                    data = data.encode()
                    bot.send_message(data)
                else:
                    if r.isdigit() and int(r)-1 == questions[info[z]['shown_q'][-1]]['answer']:
                        info[z]["score"] += 1
                        data = {
                            "chat_id": z,
                            "text": "correct! your score is: " + str(info[z]["score"])
                        }
                        data = json.dumps(data)
                        data = data.encode()
                        bot.send_message(data)
                    elif r.isdigit():
                        data = {
                            "chat_id": z,
                            "text": "wrong!"
                        }
                        data = json.dumps(data)
                        data = data.encode()
                        bot.send_message(data)
                    
                    q_index = random.choice(remain_index)
                    data = {
                        "chat_id": z,
                        "text": questions[q_index]["question"] + "\n" + ("1. " + questions[q_index]["choices"][0]) + "\n" + ("2. " + questions[q_index]["choices"][1]) + "\n" + ("3. " + questions[q_index]["choices"][2])
                    }
                    data = json.dumps(data)
                    data = data.encode()
                    bot.send_message(data)
                    info[z]['shown_q'].append(q_index)
                    info[z]["last_answered"] = False

            elif r == "scoreboard":
                scoreboard = []
                for k, v in info.items():
                    scoreboard.append((k, v["score"]))
                scoreboard.sort(key=lambda x: x[1], reverse=True)
                output = ""
                for x in scoreboard:
                    output += x[0] + ": " + str(x[1]) + "\n"
                data = {
                    "chat_id": z,
                    "text": output
                }
                data = json.dumps(data)
                data = data.encode()
                bot.send_message(data)
            else:
                data = {
                    "chat_id": z,
                    "text": "متوجه نشدم"
                }
                data = json.dumps(data)
                data = data.encode()
                bot.send_message(data)
            count = count + 1

    # Write updated data to the file
    with open("data.json", "w") as file:
        data = {"count": count, "info": info, 'ids': list(ids)}
        json.dump(data, file)

    sleep(5)
