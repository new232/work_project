class Chatbot:

    def __init__(self, model, system_role, instruction):
        self.context = [{"role":"system", "content": system_role}]
        self.model = model

#중략

    def _send_request(self):
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=self_context,
                temperature=0.5,
                top_p=1,
                max_tokens = 256,
                frequency_penalty = 0,
                presence_penalty =0
            ).model_dump()
        except Exception as e:
            print(f"Exception 오류({type(e)}) 발생:{e}")
        return response
    
    def send_request(self):
        self.context[-1]['content'] += self.instruction
        return self._send_request()
    
    def clean_context(self):
        for idx in reversed(range(len(self.context))):
            if self.context[idx]["role"] == "user":
                self.context[idx]["content"] = self.context[idx]["content"].
split("instruction:\n")[0].strip()
                break
