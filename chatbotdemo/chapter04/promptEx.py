prompt = """
내일 다음 주제로 미래 교육 포럼에서 발표할 발제문을 작성해야 합니다.
발제문의 주요 내용을 불릿 기호로 간단히 정리해 주세요
주제 : {agenda}
""".format(agenda = "인공지능 시대의 교육의 역할과 의미")

response = client.chat.completions.create
            model = "gpt-3.5-turbo"
            messages = [{"role":"user", "content":"prompt"}],
        )   