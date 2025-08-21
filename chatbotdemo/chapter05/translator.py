template = """
당신은 번역 함수이며, 반환 값은 반드시 Json 형식이어야 합니다.
STEP벼ㄹ로 작업을 수행하면서 그 결과를 아래의 출력 결과 json포맷에 작성하세요.
STEP - 1. 아래 세 개의 백틱으로 구분된 텍스트를 원문 그대로 읽어올 것
STEP - 2. 입력받은 텍스트가 영어가 아니라면 false를 표기하고 STEP - 3를 진행하지 말 것
STEP - 3. 다음의 말투로 번역할 것. ["지구의 나이는 45억 살이야.","세종대왕은 조선의 위대한 국왕이야"]
```{text}```
---
출력 결과 : {{"STEP" : <입력테스트>,"STEP-2":<true/false>,"STEP-3: <번역결과>}}
"""

text="William Shakespeare was an English playwrigter, poet and actor. He is widely regarded as the greatest writer in the English language and the world's pre-eninent dramatist."
template = tamplate.format(text=text)

context = [{"role":"user","content":template}]
response = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = context,
    temperature = 0,
    top_p=0,
    seed=1234,
).model_dump()
pprint(json.loads(response['choices'][0]['message']['content']))