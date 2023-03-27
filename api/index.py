from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


from pathlib import Path

from sanic import Sanic
from sanic_template import template as Template

app = Sanic("api")
template = Template(path=Path(__file__).parent.joinpath("templates"))
print('外面')




################################################################
import openai, os
	
openai.api_key = os.getenv("OPENAI_API_KEY")
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET")) 


	
conversation = []

class ChatGPT:  
    

    def __init__(self):
        
        self.messages = conversation
        self.model = os.getenv("OPENAI_MODEL", default = "gpt-3.5-turbo")



    def get_response(self, user_input):
        conversation.append({"role": "user", "content": user_input})
        

        response = openai.ChatCompletion.create(
	            model=self.model,
                messages = self.messages

                )

        conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        
        print("AI回答內容：")        
        print(response['choices'][0]['message']['content'].strip())


        
        return response['choices'][0]['message']['content'].strip()
	



chatgpt = ChatGPT()

from sanic import Sanic, Request, response, HTTPResponse
#from sanic.response import json

 
 

@app.route("/")
async def html(request):
    print(f'template: {template.path}')
    vars = {'title': 'hello world', 'name': 'Tom'}
    return await template.render_template("test.html", **vars)


@app.post("/callback")
async def callback(request: Request) -> HTTPResponse:
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        pass
    return response.text("OK")

@handler.add(MessageEvent, message=TextMessage)
def handling_message(event):

    
    if isinstance(event.message, TextMessage):

        
        user_message = event.message.text


        reply_msg = chatgpt.get_response(user_message)
        
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_msg))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)
