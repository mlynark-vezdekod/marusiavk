from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
from helpers import *
from handler import *

origins = ["*"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

test_results = {}

@app.post('/webhook')
async def webhook(info: Request):
    try:
        data = await info.json()

        command = data['request']['command']
        original = data['request']['original_utterance']
        original_ = original.lower()
        userid = data['session']['user']['user_id']

        res = {}
        res['session'] = data['session']
        res['version'] = data['version']
        res['response'] = {"end_session": False}

        print(inListNameOfTeam(original_.split()))

        if userid in test_results.keys():
            if test_results[userid] != None:
                _res = testHandler(data, test_results)
                test_results[userid] = _res['user']
                return _res['res']

        if 'console.log(326)' and ('вездекод' in original_ or 'вездеход' in original_):
            ans = 'Привет вездекодерам!'
            res['response']['text'] = ans
            res['response']['tts'] = ans
            return res

        elif isFirstInSpeech(original_):
            ans = 'Привет вездекодерам!'
            res['response']['text'] = ans
            res['response']['tts'] = ans
            return res

        elif command == 'пройти тест':

            ans_s = '''
            <speaker audio=marusia-sounds/game-powerup-1>  Привет! Отвечай на мои вопросы - говори варианты А, БЭ, ВЭ или ГЭ .  В конце я скажу тебе результат.
            Итак, первый вопрос: Какие способы получения событий чат-ботов ты знаешь?
            '''
            ans = '''
            1. Какие способы получения событий чат-ботов ты знаешь?
А) ShortRes, PoolQueue
Б) Longpoll и CallBack
В) FastConnect и OpenQuest
Г) WebConnect и VK Connect
            '''
            test_results[userid] = dict(
                step=1,
                vkma=0,
                mobile=0,
                marusya=0,
                chatbots=0,
                php=0,
                java=0,
                gamedev=0,
                backend=0
            )
            res['response']['text'] = ans
            res['response']['tts'] = ans_s
            return res

        elif original_ == 'финал теста':
            res['response']['text'] = f'''
            Отлично!
            Я думаю, вам стоит обратить внимание на категорию «ИБАНИЕ БАРАН»
                    '''
            res['response']['tts'] = f'<speaker audio=marusia-sounds/game-win-1>  Отлично! Я думаю, вам стоит обратить внимание на категорию ИБАНИЕ БАРАН, ждём вас на Вездекоде!'
            return res

        ans = f'Не понимаю, что значит ваше {original_}'
        res['response']['text'] = ans
        res['response']['tts'] = ans
        return res
    except Exception as err:
        print(err)
        res = {}
        res['session'] = data['session']
        res['version'] = data['version']
        res['response'] = {"end_session": False}
        ans = f'Произошли технические шоколадочки {str(err)}'
        res['response']['text'] = ans
        res['response']['tts'] = ans
        return res
