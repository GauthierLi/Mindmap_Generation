class LLMApi(object):
    def __init__(self, llm_api):
        self.llm = llm_api
    
    def __call__(self, prompt: str, temperature=0.9):
        result = '<ERROR>'
        count = 0
        while result == '<ERROR>':
            result = self.llm(prompt, temperature)
            count += 1
            if count > 10:
                raise AssertionError('Over 10 times of error ！！')
        return result