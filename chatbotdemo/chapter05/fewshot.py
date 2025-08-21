# zero-shot Prompting으로 구현하기
# 샘플 없이 사전 학습 데이터로 답변 생성

template = """
긍정 또는 부정으로 답변하세요.
Q : 매력적인 이성과 사랑에 빠졌어
"""

context = [{"role":"user", "content": template}]

res