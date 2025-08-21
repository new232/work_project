from characters import system_role, instruction

# jjinchin 인스턴스 생성 -> 나중에 바꿔주기
jjinchin = Chatbot(
    model = model.basic,
    system_role = system_role,
    instruction = instruction
)

@application.route('/chat-api', methods=['POST'])
def chat_api():
    request_message = request.json['request_message']
    print #이어서 p187