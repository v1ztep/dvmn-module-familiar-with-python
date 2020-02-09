import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

email_from = 'b10Sss@yandex.ru'
email_to = 'noahbread@gmail.com'

message = '''\
From: {0}
To: {1}
Subject: Важно!
Content-Type: text/plain; charset="UTF-8";

Привет, %friend_name%! %my_name% приглашает тебя на сайт %website%!

%website% — это новая версия онлайн-курса по программированию. 
Изучаем Python и не только. Решаем задачи. Получаем ревью от преподавателя. 

Как будет проходить ваше обучение на %website%? 

→ Попрактикуешься на реальных кейсах. 
Задачи от тимлидов со стажем от 10 лет в программировании.
→ Будешь учиться без стресса и бессонных ночей. 
Задачи не «сгорят» и не уйдут к другому. Занимайся в удобное время и ровно столько, сколько можешь.
→ Подготовишь крепкое резюме.
Все проекты — они же решение наших задачек — можно разместить на твоём GitHub. Работодатели такое оценят. 

Регистрируйся → %website%  
На модули, которые еще не вышли, можно подписаться и получить уведомление о релизе сразу на имейл.'''.format(email_from, email_to)

transformed_message = message.replace('%website%', 'dvmn.org')
transformed_message = transformed_message.replace('%friend_name%', 'Вадим')
transformed_message = transformed_message.replace('%my_name%', 'Владимир')
transformed_message = transformed_message.encode("UTF-8")

login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")

server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
server.login(login, password)
server.sendmail(email_from, email_to, transformed_message)
server.quit()


print('Письмо отправлено')

