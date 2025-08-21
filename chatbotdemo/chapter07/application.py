from flask import Flask, render_template, request
import sys
from chatbot import Chatbot
from common import model

#jjinchin 인스턴스 생성
jjinchin = Chatbot(model.basic)

#이건 flask 코드라서. 우리는 그거 말고 fastapi썼으니까 그걸로 바꿔줘야함. 
# url 주소도 물어봐야함. 

#flask 객체 생성
application = Flask(__name__)

#url주소와 함수 연결.
@application.route("/") #괄호안의 url로 접속했을때 일로 오라는 데코레이터. "/"는 기본 url임.
def hello():
    return "Hello."

#url 주소와 함수 연결 - route 수정.
@application.toute("/welcome")
def welcome():
    return "Hello. 수정 url!!!"

@application.route("/chat-api")
def chat_app():
    return render_template("chat.html")

#객체변수 chatbot을 jjinchin으로 해둠
@application.route('/chat-api', methods=['POST'])
def chat_api():
    request_message = request.json['request_message']
    print("request_message:", request_message)
    jjinchin.add_user_message(request_message)
    response = jjinchin.send_request()
    jjinchin.add_response(response)
    response_message = jjinchin.get_response_content()
    print("response_message:",response_message)
    return {"response_message": response_message}

# 서버 구동 - flask 객체를 담고 있는 application으로부터 run메소드 호출해서 서버 구동.
if __name__ == "__main__":
    application.run(host='0.0.0.0', port = int(sys.argv[1]))
