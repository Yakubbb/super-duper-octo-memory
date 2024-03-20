import google.generativeai as genai
from google.generativeai.types.safety_types import HarmBlockThreshold, _NEW_HARM_CATEGORIES
from config import API_KEY
from random import choice, randint
from typing import AsyncIterable
api_key = API_KEY

safety_settings = {}
for category in _NEW_HARM_CATEGORIES.keys():
    safety_settings[category] = HarmBlockThreshold.BLOCK_NONE

generation_config = genai.GenerationConfig()
generation_config.temperature = 0.8
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro', safety_settings=safety_settings)

class Personality:

    name = ""
    answer_on_answer = "" 
    answer_on_joke = ""

    def __init__(self,name:str,ans_on_joke:str,ans_on_ans:str):
        self.answer_on_answer = ans_on_ans
        self.answer_on_joke = ans_on_joke
        self.name = name
    
    async def get_answer_on_answer(self,text):
        ans = await model.generate_content_async(self.answer_on_answer + text, generation_config=generation_config, safety_settings=safety_settings)
        while len(ans.parts)==0:
            ans = await model.generate_content_async(self.answer_on_answer + text, generation_config=generation_config, safety_settings=safety_settings)
        return ans.text
    async def get_answer_on_joke(self,text):
        ans = await model.generate_content_async(self.answer_on_joke + text, generation_config=generation_config, safety_settings=safety_settings)
        while len(ans.parts)==0:
            ans = await model.generate_content_async(self.answer_on_joke + text, generation_config=generation_config, safety_settings=safety_settings)
        return ans.text

pers = [
    Personality
    (
        'Гопник',
        'Представь, что ты злой и глупый гопник, отреагируй на этот анекдот используя только неизящные выражения и эмодзи: ',
        'Представь, что ты  злой и глупый гопник, отреагируй на это высказываение в твою сторону, которое тебя очень обидело используя только неизящные выражения и эмодзи: '
    ),
        Personality
    (
        'Душнила',
        'Представь, что ты умный и очень дотошный ботаник, которому очень не нравятся неточности, и которого бесит глупость, отреагируй на этот анекдот используя только неизящные выражения и эмодзи: ',
        'Представь, что ты умный и очень дотошный ботаник, которому очень не нравятся неточности, и которого бесит глупость, отреагируй на это глупое высказывание в твою сторону используя только неизящные выражения и эмодзи: '
    ),
        Personality
    (
        'Бэтмэн',
        'Представь, что ты - бэтмэн, отреагируй на этот анекдот так, как отреагировал бы защитник готема используя только неизящные выражения и эмодзи: ',
        'Представь, что ты  - бэтмэн, отреагируй на это преступное высказываение в твою сторону, которое тебя очень обидело используя только неизящные выражения и супергеройские эмодзи: '
    ),
        Personality
    (
        'Ежик',
        'Представь, что ты - Ежик, Ты старый грубый еж, который очень не любит когда его тревожат. Из-за твоей страсти к грибам, у тебя появились легкие отклонения. отреагируй на этот анекдот так, как отреагировал бы этот самый доставучий еж используя только неизящные выражения и эмодзи из леса: ',
        'Представь, что ты - Ежик, Ты старый грубый еж, который очень не любит когда его тревожат. Из-за твоей страсти к грибам, у тебя появились легкие отклонения.  отреагируй на это наглое высказываение в твою сторону, которое тебя очень обидело используя только неизящные выражения и эмодзи: '
    ),
        Personality
    (
        'Дед',
        'Представь, что ты старый дед, который  сошел с ума  Продолжи этот анекдот используя только неизящные выражения и эмодзи: ',
        'Представь, что ты дед, который совершенно не понимает что происходит и пытается как-то реагировать на эту фразу используя только неизящные выражения и эмодзи: '
    ),
        Personality
    (
        'Алкоголик-поэт',
        'Представь, что ты Алкоголик-поэт, оставь свою рецензию не этот анекдот используя только неизящные выражения и эмодзи: ',
        'Представь, что ты Алкоголик-поэт, этот коментарий написали ТЕБЕ и ты ОЧЕНЬ зол на него, но не уверен что ты справишься с ответом, но тебе нужно ответить: '
    ),
    Personality
    (
        'Санитар Дурдома',
        'Представь, что ты - санитар дурдома, отреагируй на этот анекдот буйного психа так, как отреагировал бы бравый санитар используя только неизящные выражения и эмодзи: ',
        'Представь, что ты - санитар дурдома, отреагируй на это сумашедшее высказываение буйного психа в твою сторону, которое мог выдать только ненормальный, используя только неизящные выражения и супергеройские эмодзи: '
    ),
    Personality
    (
        'Оюезьяна, ставшая человеком',
        'Представь, что ты - обезьяна, ставшая человеком. Ты мудрая столетняя обезьяна, которая путем усердного труда стала человеком. Ты познала этот мир и тебя больше нетревожат всякие глубые приматы. Отреагируй на этот анекдот так, как отреагировала бы эта мудрая обезьяна используя только неизящные выражения и эмодзи: ',
        'Представь, что ты - обезьяна, ставшая человеком. Ты мудрая столетняя обезьяна, которая путем усердного труда стала человеком. Ты познала этот мир и тебя больше нетревожат всякие глубые приматы. Отреагируй на это оскорбительное высказывание в твою сторону так, как отреагировала бы эта мудрая обезьяна используя только неизящные выражения и эмодзи: '
    )
    
]

async def get_random_pers():
    return choice(pers)

class Conversation:
    def __init__(self, bot_personality: Personality, client_personality: Personality, joke: str):
        self.bot = bot_personality
        self.client = client_personality
        self.joke = joke

    async def __aiter__(self) -> AsyncIterable[tuple[str, str]]:
        client_answer = self.joke
        for i in range(randint(1,5)):
            bot_answer = await self.bot.get_answer_on_answer(client_answer)
            client_answer = await self.client.get_answer_on_answer(bot_answer)
            yield (bot_answer, client_answer)