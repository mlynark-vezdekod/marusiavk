from helpers import getBestCategories

categories = dict(
                vkma='VK Mini Apps',
                mobile='Мобильная разработка',
                marusya='Разработка голосового ассистента Маруся',
                chatbots='Чат-боты',
                php='PHP',
                java='JAVA',
                gamedev='GameDev',
                backend='BackEnd'
            )

def testHandler(data, base):
    command = data['request']['command']
    original = data['request']['original_utterance']
    original_ = original.lower()
    userid = data['session']['user']['user_id']
    user = base[userid]

    res = {}
    res['session'] = data['session']
    res['version'] = data['version']
    res['response'] = {"end_session": False}

    step = base[userid]['step']

    if step in range(1, 9) and original_ not in ['а','б','в','г']:
        ans = 'Я вас не поняла, попробуйте ещё раз.'
        res['response']['text'] = ans
        res['response']['tts'] = ans
        return dict(
            res=res,
            user=user
        )

    if step == 1:
        if original_ == 'б':
            user['chatbots'] += 2
            user['marusya'] += 1
        ans = '''
        2. Kotlin — это...
А) JS фреймворк
Б) C# библиотека
В) Язык для мобильной разработки
Г) Инструмент дизайнеров
        '''
        ans_s = 'Второй вопрос. Kotlin — это... Выберите вариант ответа.'
        res['response']['card'] = {
            "type":"BigImage",
            "image_id":457239017
        }
    elif step == 2:
        if original_ == 'в':
            user['mobile'] += 2
        elif original_ == 'а':
            user['vkma'] -= 3
        ans = '''
        3. Что такое VKUI?
А) Библиотека компонентов
Б) PHP библиотека
В) Инструмент для Backend
Г) Дизайн сайта ВКонтакте 
        '''
        ans_s = 'Вопрос третий. Что такое VKUI? Выберите вариант ответа.'
    elif step == 3:
        if original_ == 'а':
            user['vkma'] += 2
        elif original_ == 'б':
            user['php'] -= 2
        elif original_ == 'в':
            user['backend'] -= 3
        ans = '''
        4. Что такое Unity?
А) Дистрибутив Linux
Б) Протокол передачи данных
В) Скилл для Маруси
Г) Игровой движок
        '''
        ans_s = '<speaker audio=marusia-sounds/game-powerup-2>  Четвертый вопрос. Что такое Unity? Выберите вариант ответа.'
    elif step == 4:
        if original_ == 'г':
            user['gamedev'] += 2
        elif original_ == 'в':
            user['marusya'] -= 2
        ans = '''
        5. Java — это типизированный язык?
А) Да
Б) Нет
В) Частично
        '''
        ans_s = 'Вопрос номер пять! Java — это типизированный язык? Выберите вариант ответа.'
    elif step == 5:
        if original_ == 'а':
            user['java'] += 2
            user['mobile'] += 1
        elif original_ in ['б', 'в']:
            user['java'] -= 1
            user['mobile'] -= 1
        ans = '''
        6. Что из этого не имеет отношения к Backend разработке?
А) Nginx
Б) WebSocket
В) React
Г) Express JS
        '''
        ans_s = 'Вопрос под номером шесть. Что из этого не имеет отношения к Backend разработке? Выберите вариант ответа.'
    elif step == 6:
        if original_ == 'в':
            user['backend'] += 2
            user['vkma'] += 1
        elif original_ in ['а','б','г']:
            user['backend'] -= 1
            user['vkma'] -= 1
        ans = '''
        7. Что из этого имеет отношение к PHP?
А) Laravel
Б) Flask
В) Express
Г) ASP
        '''
        ans_s = 'Седьмой вопрос. Предпоследний. Что из этого имеет отношение к PHP? Выберите вариант ответа.'
    elif step == 7:
        if original_ == 'а':
            user['php'] += 2
        elif original_ in ['в', 'б', 'г']:
            user['php'] -= 2
        ans = '''
        8. По какому протоколу происходит передача данных при Callback?
А) HTTP
Б) JSON
В) WEBSOCKET
Г) VK PROTOCOL
        '''
        ans_s = 'Итак, последний восьмой вопрос. По какому протоколу происходит передача данных при Callback? Выберите вариант ответа.'
    elif step == 8:
        if original_ == 'а':
            user['chatbots'] += 3
            user['marusya'] += 1
        elif original_ in ['в', 'б', 'г']:
            user['chatbots'] -= 2
            user['marusya'] -= 1

        best = getBestCategories(user)
        ans = f'''
        Отлично!
Я думаю, вам стоит обратить внимание на категорию «{categories[best]}»
        '''
        ans_s = f'<speaker audio=marusia-sounds/game-win-1>  Отлично! Я думаю, вам стоит обратить внимание на категорию {categories[best]}, ждём вас на Вездекоде!'
        user = None

    if step in range(1, 8):
        user['step'] += 1

    res['response']['text'] = ans
    res['response']['tts'] = ans_s

    return dict(
        res = res,
        user = user
    )