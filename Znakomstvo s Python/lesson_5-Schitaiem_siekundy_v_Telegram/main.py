import ptbot
import os
from pytimeparse import parse
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("MY_TG_BOT_TOKEN")
CHAT_ID = '219730051'

bot = ptbot.Bot(TOKEN)
bot.send_message(CHAT_ID, "Бот запущен")


def main():
    bot.send_message(CHAT_ID, "На сколько запустить таймер?")
    bot.reply_on_message(timer)
    

def timer(text_time):
    timer_seconds = parse(text_time)
    message_id = bot.send_message(CHAT_ID, "Таймер запущен на {0} секунд(ы)\n{1}".format(timer_seconds, render_progressbar(timer_seconds, timer_seconds)))
    
    bot.create_countdown(timer_seconds, notify_progress, message_id=message_id, timer_seconds=timer_seconds)
    bot.create_timer(timer_seconds, notify)


def notify():
    bot.send_message(CHAT_ID, "Время вышло")


def notify_progress(secs_left, message_id, timer_seconds):
    bot.update_message(CHAT_ID, message_id, "Осталось {0} секунд(ы)\n{1}".format(secs_left, render_progressbar(timer_seconds, secs_left)))


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


if __name__ == '__main__':
    main()

bot.run_bot()
