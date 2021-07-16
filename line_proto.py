from linebot import LineBotApi, WebhookHandler 
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, ImageSendMessage  ,TextSendMessage
import pya3rt 

from flask import Flask, request, abort
#from flask_ngrok import run_with_ngrok

import cv2

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

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
    
    messe = event.message.text
    
    if messe == "ちんぽ":
        cap = cv2.VideoCapture(0)
       
        ret, frame = cap.read()
        #frame = cv2.resize(frame, dsize=(10, 10))

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, frame_otsu = cv2.threshold(frame_gray, 0, 255, cv2.THRESH_OTSU)
        #cv2.imshow("test",frame_otsu)
        #cv2.waitKey(20)
        #cv2.destroyAllWindows()
        cap.release()
        
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()

        drive = GoogleDrive(gauth)
        
        if ret == True:
            cv2.imwrite('gazo.jpg', frame_otsu)
        
        f = drive.CreateFile({'title': 'gazo.jpg', 'mimeType': 'image/jpeg'})
        f.SetContentFile('gazo.jpg')
        f.Upload()
        url = 'https://drive.google.com/uc?export=view&id=' + f['id']
        #url = 'https://drive.google.com/file/d/1C3y2Dz316dXSSc5fmTDxZNVkB9mpRViJ/view?usp=sharing'    
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=url, preview_image_url=url))

if __name__ == '__main__':

    app.run()
     
