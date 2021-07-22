from linebot import LineBotApi, WebhookHandler 
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, ImageSendMessage  ,TextSendMessage

import random

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

janken : list = ["グー", "チョキ", "パー"]
message : list = []

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print('OK')
    messe = event.message.text

    num : int = random.randint(0,2)
    line_hand = janken[num]
    message.append(line_hand)

    if messe == "グー":
        if int == 0:
            message.append("DRAW")
        elif int == 1:
            message.append("YOUR WIN")
        else:
            message.append("YOUR LOSE")
    
    elif messe == "チョキ":
        if int == 0:
            message.append("YOUR LOSE")
        elif int == 1:
            message.append("DRAW")
        else:
            message.append("YOUR WIN")

    elif messe == "パー":
        if int == 0:
            message.append("YOUR WIN")
        elif int == 1:
            message.append("YOUR LOSE")
        else:
            message.append("DRAW")
    
    else:
        message.append("hanashi ni narimasen")

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message[1]))



if __name__ == '__main__':

    app.run()
     