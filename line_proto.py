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

    with open('./data.json') as f:
        json_data = json.load(f)
    
        if messe == "グー":
            if num == 0:
                messagelist.append(TextSendMessage(text="DRAW"))
            elif num == 1:
                messagelist.append(TextSendMessage(text="YOUR WIN"))
                messagelist.append(TextSendMessage(text=random.choice(json_data["person"])))
                messagelist.append(TextSendMessage(text=random.choice(json_data["part"])))
                messagelist.append(TextSendMessage(text="まポリン様、勝利回数は"+ str(json_data["syouri"][0])))
                json_data["syouri"][0] =+ 1
            else:
                messagelist.append(TextSendMessage(text="YOUR LOSE"))
                json_data["syouri"][1] =+ 1
                messagelist.append(TextSendMessage(text="まポリン様、敗北回数は"+ str(json_data["syouri"][1])))
        
        elif messe == "チョキ":
            if num == 0:
                messagelist.append(TextSendMessage(text="YOUR LOSE"))
                json_data["syouri"][1] =+ 1
                messagelist.append(TextSendMessage(text="まポリン様、敗北回数は"+ str(json_data["syouri"][1])))
            elif num == 1:
                messagelist.append(TextSendMessage(text="DRAW"))
            else:
                messagelist.append(TextSendMessage(text="YOUR WIN"))
                messagelist.append(TextSendMessage(text=random.choice(json_data["person"])))
                messagelist.append(TextSendMessage(text=random.choice(json_data["part"])))
                json_data["syouri"][0] =+ 1
                messagelist.append(TextSendMessage(text="まポリン様、勝利回数は"+ str(json_data["syouri"][0])))

        elif messe == "パー":
            if num == 0:
                messagelist.append(TextSendMessage(text="YOUR WIN"))
                json_data["syouri"][0] =+ 1
                messagelist.append(TextSendMessage(text=random.choice(json_data["person"])))
                messagelist.append(TextSendMessage(text=random.choice(json_data["part"])))
                messagelist.append(TextSendMessage(text="まポリン様、勝利回数は"+ str(json_data["syouri"][0])))
            elif num == 1:
                messagelist.append(TextSendMessage(text="YOUR LOSE"))
                json_data["syouri"][1] =+ 1
                messagelist.append(TextSendMessage(text="まポリン様、敗北回数は"+ str(json_data["syouri"][1])))
            else:
                messagelist.append(TextSendMessage(text="DRAW"))
        
        else:
            messagelist.append("hanashi ni narimasen")

        line_bot_api.reply_message(event.reply_token, messagelist)

        f.write(json.dumps(json_data))
        f.close




if __name__ == '__main__':

    app.run()
     