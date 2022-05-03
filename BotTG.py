import telebot, wikipedia, re, cmath, os
from telebot import types
import numpy as np
import matplotlib.pyplot as plt
# Создаем экземпляр бота
bot = telebot.TeleBot('5399071818:AAGZ8KxdodxM0_iBk4PKg8xKq-jYuucWQVQ')
# Устанавливаем русский язык в Wikipedia
wikipedia.set_lang("ru")
# Чистим текст статьи в Wikipedia и ограничиваем его тысячей символов
global D
###
def sqr(s):
    a = float(s.split(" ")[1])
    b = float(s.split(" ")[2])
    c = float(s.split(" ")[3])
    D = (b*b)-(4*a*c)
    if D>=0:
        x1 = ((-b)-(D**0.5))/(2*a)
        x2 = ((-b)+(D**0.5))/(2*a)   
        y = lambda x: a*x*x+b*x+c
        x0 = -b/(2*a);
        y0 = a*x0*x0+b*x0+c
        # создаём рисунок с координатную плоскость
        fig = plt.subplots()
        # создаём область, в которой будет
        # - отображаться график
        x = np.linspace(x0-10, x0+10,100)
        # значения x, которые будут отображены
        # количество элементов в созданном массиве
        # - качество прорисовки графика 
        # рисуем график
        ax = plt.gca()

        plt.scatter(x0, y0,  color = 'deeppink')
        plt.scatter(x1, 0,  color = 'deeppink')
        plt.scatter(x2, 0,  color = 'deeppink')
        plt.text(x0, y0, "x = " + str(round(x0,2))+"\ny = "+str(round(y0,2)))
        plt.text(x1-3, 0, "x = " + str(round(x1,2))+"\ny = 0")
        plt.text(x2+1, 0, "x = " + str(round(x2,2))+"\ny = 0")
        O = "O ("+str(x0)+";"+str(y0)+")"
        plt.plot(x, y(x))

        if a>0:
        
            if y0>0:
                plt.ylim(y0-2, y0+5)
            else:
                plt.ylim(y0-2, 5)
        else:
        
            if y0>0:
                plt.ylim(-5, y0+5)
            else:
                plt.ylim(y0-5, y0+2)
        plt.grid()
        plt.savefig('saved_figure.png')
    
        return "Корнями уравнения являются числа "+str(round(x1,2))+" и "+str(round(x2,2)) + "\n" + O
    else:
        return "Дискриминант <0"

        
    
def getwiki(s):

    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext=ny.content[:1000]
        # Разделяем по точкам
        wikimas=wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом'
# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
        # Добавляем две кнопки
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(m.chat.id, 'Перед вами предстал всемогущий праведник, напиши же /help чтобы познать мою мощь',  reply_markup=a)
@bot.message_handler(commands=["help"])
def help(m, res=False):
    bot.send_message(m.chat.id, 'Википедия: ищет статью по введенному названию, \nвики + [слово] (пример вики бот)\n'
                    '\nКвадратные уравнения: находит корни квадратного уравнения, \nкв + [коэффициенты уравнения] (пример кв 1 -2 -24)\n')
# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.lower().split(" ")[0] == 'вики' :
        bot.send_message(message.chat.id, getwiki(message.text.lower().strip('вики')))
    if message.text.lower().split(" ")[0] == 'кв':
        
        if D<=0:
             bot.send_message(message.chat.id, 'Дискриминант меньше нуля')
        else:
           bot.send_message(message.chat.id, sqr(message.text.lower().strip('кв')))
           bot.send_photo(message.chat.id, open('saved_figure.png', 'rb'));
           os.remove('saved_figure.png')
    

########### Запускаем бота ###########
bot.polling(none_stop=True, interval=0)