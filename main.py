
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

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

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
        if event.message.text in "習慣登録":

            timetree_url= f"https://timetreeapis.com/calendars/{YOUR_ROOM_ID}/events"
            headers = {
                "Content_Type": "application/json",
                "Accept": "application/vnd.timetree.v1+json",
                "Authorization": f"Bearer, {YOUR_TIMETREE_TOEN}"
            }
            request_body = {
                "data": {
                "attributes": {
                    "category": "schedule",
                    "title": "Lineから登録",
                    "all_day": True,
                    "start_at": "2022-03-01T00:00:00.000Z",
                    "start_timezone": "UTC",
                    "end_at": "2022-03-01T00:00:00.000Z",
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
            print("🥺🥺")
            print(res)
            print("🥺🥺")

            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=res+ chr(0x10002D)),
                ]
            )

            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text='お疲れ様です'+ chr(0x10002D)),
                ]
            )
            


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

