from openai import OpenAI
client = OpenAI()


chat = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "당신은 한국어 전문가입니다."},
        {"role": "user", "content": "머신러닝과 딥러닝의 차이점을 설명해주세요."}
    ],
    temperature=0.7,
)
print(chat.choices[0].message.content)