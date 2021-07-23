from linebot import LineBotApi, WebhookHandler 
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, ImageSendMessage  ,TextSendMessage, TemplateSendMessage,ButtonsTemplate,URIAction

import random
import json

from flask import Flask, request, abort
#from flask_ngrok import run_with_ngrok


app = Flask(__name__)
#run_with_ngrok(app)

line_bot_api = LineBotApi("y4HvuUcycFtqu9sKvTDcIVqNlqFA+LFC/eIBWZJ2vG/0V6BDRFlYCCw/tnf2jguNiWauaVLfJs6TBSrxF57b+jhYiIGoGmE+iy8wBtc2sUGAKsAWy33CYkqztkK9+6i4EB+1f8bsDMjwMruN01WnUgdB04t89/1O/w1cDnyilFU=")

handler = WebhookHandler("cc2a636c27b60f6cc54e758793b46e81")

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

    messe = event.message.text

    num : int = random.randint(0,2)
    messagelist : list = []
    messagelist.append(TextSendMessage(text=janken[num]))


    with open('data.json') as f:
        json_data = json.load(f)
        win_messe = TextSendMessage(text=random.choice(json_data["場所"])+random.choice(json_data["kigen"])+random.choice(json_data["person"])+"に"+random.choice(json_data["part"])+"を"+random.choice(json_data["time"])+"揉んでいただく権利をまぽりんさんは手にしました")

        message_template_win = TemplateSendMessage(
        alt_text="にゃーん",
        template=ButtonsTemplate(
            text=win_messe,
            title="WIN",
            image_size="cover",
            thumbnail_image_url="https://任意の画像URL.jpg",
            actions=[
                URIAction(
                    uri="https://任意のページURL",
                    label="URIアクションのLABEL"
                )
            ]
        )
    )
        message_template_lose = TemplateSendMessage(
        alt_text="にゃーん",
        template=ButtonsTemplate(
            text=win_messe,
            title="L O S E",
            image_size="cover",
            thumbnail_image_url="https://任意の画像URL.jpg",
            actions=[
                URIAction(
                    uri="https://任意のページURL",
                    label="URIアクションのLABEL"
                )
            ]
        )
    )
    
        if messe == "グー":
            if num == 0:
                messagelist.append(TextSendMessage(text="DRAW"))
            elif num == 1:
                messagelist.append(TextSendMessage(text="YOUR WIN !!!!!!!!!"))
                messagelist.append(win_messe)
                messagelist.append(message_template_win)
            else:
                messagelist.append(TextSendMessage(text="YOUR LOSE"))
                messagelist.append(message_template_lose)
        
        elif messe == "チョキ":
            if num == 0:
                messagelist.append(TextSendMessage(text="L O S E"))
                messagelist.append(message_template_lose)
            elif num == 1:
                messagelist.append(TextSendMessage(text="DRAW"))
            else:
                messagelist.append(TextSendMessage(text="YOUR WIN !!!!!!!!"))
                messagelist.append(win_messe)
                messagelist.append(message_template_win)

        elif messe == "パー":
            if num == 0:
                messagelist.append(TextSendMessage(text="おめでとうございます !!!!!!!!"))
                messagelist.append(win_messe)
                messagelist.append(message_template_win)
            elif num == 1:
                messagelist.append(TextSendMessage(text="まぽりんさんは敗北しました。"))
                messagelist.append(message_template_lose)
            else:
                messagelist.append(TextSendMessage(text="DRAW"))
        
        else:
            messagelist.append("hanashi ni narimasen")

        line_bot_api.reply_message(event.reply_token, messagelist)

        f.write(json.dumps(json_data))
        f.close

if __name__ == '__main__':

    app.run()
     