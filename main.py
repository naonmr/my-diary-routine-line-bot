
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import requests
import datetime



import schedule
import time


app = Flask(__name__)



#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

YOUR_USERID = os.environ["YOUR_USERID"]

YOUR_TIMETREE_TOEN  = os.environ["YOUR_TIMETREE_TOEN"]
YOUR_ROOM_ID  = os.environ["YOUR_ROOM_ID"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

line_bot_api.push_message(
    YOUR_USERID,
    TextSendMessage(text='ぷっしゅめっせーじです。やあ!'))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if event.type == "message":
        if event.message.text in "帰るよー！" or (event.message.text == "帰るよ！") or (event.message.text == "帰る！") or (event.message.text == "帰るよ"):
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text='お疲れ様です'+ chr(0x10002D)),
                ]
            )
            
    if event.type == "message":
        if event.reply_token:

            dt_now = datetime.datetime.now()
            year = dt_now.year
            month = dt_now.month
            day = dt_now.day

            if month < 10:
                month = f"0{month}"
            if day < 10:
                day = f"0{day}"

            print(year, month, day, "⏰")


            timetree_url= f"https://timetreeapis.com/calendars/{YOUR_ROOM_ID}/events"

            headers = {
                'Authorization': f'Bearer {YOUR_TIMETREE_TOEN}',
                "Accept": "application/vnd.timetree.v1+json",
                "Content-Type": "application/json"
            }
            request_body = {
                "data": {
                "attributes": {
                    "category": "schedule",
                    "title": event.message.text,
                    "all_day": True,
                    "start_at": f"{year}-{month}-{day}T00:00:00.000Z",
                    "start_timezone": "UTC",
                    "end_at": f"{year}-{month}-{day}T00:00:00.000Z",
                    "end_timezone": "UTC"
                },
                "relationships": {
                    "label": {
                    "data": {
                        "id": f"{YOUR_ROOM_ID},1",
                        "type": "label"
                    }
                    }
                }
                }
            }
    
            res = requests.post(timetree_url, headers=headers, json=request_body)
            
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=f"「{event.message.text}」をTimeTreeに登録しました！{chr(0x10008A)}"),
                ]
            )




    line_bot_api.push_message(
        YOUR_USERID,
        TextSendMessage(text='ぷっしゅめっせーじです。やあ!'))


    # schedule.every(1).minutes.do(
    #     line_bot_api.push_message(
    #     YOUR_USERID,
    #     TextSendMessage(text='ぷっしゅめっせーじです。やあ!')))

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)





if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

