template = """
    Q: 서버실에는 컴퓨터 9대 있었습니다. 
    월요일부터 목요일까지 매일 5대의 컴퓨터가 추가로 설치되었고 
    어제 한 대를 반출했습니다.
    이제 서버실에는 몇 대의 컴퓨터가 있을까요?
    A :
"""

context = [{"role" : "user", "content" : template}]
response = client.chat.completions.create(
    model = "gpt-3.5-turbo-0613",
    messages=context
    temperature = 0,
    top_p = 0
).model_dump()

pprint(response['choices'][0]['message']['content'])