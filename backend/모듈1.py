from openai import OpenAI
client = OpenAI()


chat = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "����� �ѱ��� �������Դϴ�."},
        {"role": "user", "content": "�ӽŷ��װ� �������� �������� �������ּ���."}
    ],
    temperature=0.7,
)
print(chat.choices[0].message.content)