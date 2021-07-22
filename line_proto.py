from linebot import LineBotApi, WebhookHandler 
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, ImageSendMessage  ,TextSendMessage

import random
import json

from flask import Flask, request, abort
#from flask_ngrok import run_with_ngrok


app = Flask(__name__)
#run_with_ngrok(app)

line_bot_api = LineBotApi("5+03IhNq5ERf1hywUdvcgUgLb33nFRyCwT5cZ+TvEAKx8ymCnAHz/Mbbz\
pUQPr5y/TDD+0dQOGp+RJz6cE8cm6sfDUssEDG49aD0V6iHDbZDGcVI/qGrpKejMDBGSeHQ5loYaQicY5DL\
5eSDh7wVrwdB04t89/1O/w1cDnyilFU=")

handler = WebhookHandler("d033ce60910936f714c504a807b0aab5")

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    janken : list = ["グー", "チョキ", "パー"]
    messagelist : list = []

    messe = event.message.text

    num : int = random.randint(0,2)
    messagelist.append(TextSendMessage(text=janken[num]))

    with open('data.json') as f:
        json_data = json.load(f)
    
        if messe == "グー":
            if num == 0:
                messagelist.append(TextSendMessage(text="DRAW"))
            elif num == 1:
                messagelist.append(TextSendMessage(text="YOUR WIN !!!!!!!!!"))
                messagelist.append(TextSendMessage(text=random.choice(json_data["場所"])+random.choice(json_data["kigen"])+random.choice(json_data["person"])+"に"+random.choice(json_data["part"])+"を"+random.choice(json_data["time"])+"揉んでいただく権利をまぽりんさんは手にしました"))
            else:
                messagelist.append(TextSendMessage(text="YOUR LOSE"))
        
        elif messe == "チョキ":
            if num == 0:
                messagelist.append(TextSendMessage(text="L O S E"))
            elif num == 1:
                messagelist.append(TextSendMessage(text="DRAW"))
            else:
                messagelist.append(TextSendMessage(text="YOUR WIN !!!!!!!!"))
                messagelist.append(TextSendMessage(text=random.choice(json_data["場所"])+random.choice(json_data["kigen"])+random.choice(json_data["person"])+"に"+random.choice(json_data["part"])+"を"+random.choice(json_data["time"])+"揉んでいただく権利をまぽりんさんは手にしました"))

        elif messe == "パー":
            if num == 0:
                messagelist.append(TextSendMessage(text="おめでとうございます !!!!!!!!"))
                messagelist.append(TextSendMessage(text=random.choice(json_data["場所"])+random.choice(json_data["kigen"])+random.choice(json_data["person"])+"に"+random.choice(json_data["part"])+"を"+random.choice(json_data["time"])+"揉んでいただく権利をまぽりんさんは手にしました"))
            elif num == 1:
                messagelist.append(TextSendMessage(text="まぽりんさんは敗北しました。"))
            else:
                messagelist.append(TextSendMessage(text="DRAW"))
        
        else:
            messagelist.append("hanashi ni narimasen")

        line_bot_api.reply_message(event.reply_token, messagelist)

        f.write(json.dumps(json_data))
        f.close




if __name__ == '__main__':

    app.run()
     