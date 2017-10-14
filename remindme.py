# Telegram imports
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, Job

# utils imports
import random
from termcolor import colored
import logging
logging.basicConfig(format='%(levelname)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

print colored('RUN: PyLetsGO bot support running ..', 'blue')


# static variables
tips = [
    [
        'La tua gestione del tempo non va bene Maurizio!',
        'Maurizio e\' il momento di uscire',
        'Maurizio stai prendendo il computer?',
        'Davvero ti porterai a casa il computer Maurizio?',
        'Quante volte lavori DAVVERO a casa?',
        'Maurizio sei concentrato?',
        'Fai lo Schemetto',
    ],
    [
        'Potenzialmente siete nelle condizioni di poter fare qualcosa di positivo non solo in stage ma anche in prospettiva futura... *DIPENDE DA VOI*.\nCredete in voi stessi e date il meglio!',
        'Pensa a quello che vuoi essere!',
        'Pensa a quello che fai! Tanto oramai sei un Senior',
        'Non permettere mai a nessuno di dirti che non sai fare qualcosa!',
        'Esercitare liberamente il proprio ingegno, ecco la vera felicita\'.',
        'Essere irragionevoli e\' un diritto umano',
        'Quando sai cosa stai facendo, allora puoi fare quello che vuoi',
        'E\' solo quando avrai smesso di rincorrere le cose sbagliate che darai una possibilita\' alle cose giuste di raggiungerti.',
        'Se davanti a te vedi tutto grigio sposta l\'elefante.',
    ]
]
short_time = '10'
long_time = '3600'


def start(bot, update):
    # TODO: improve logic of start
    keyboard = [[KeyboardButton("/set {}".format(short_time)),
                 KeyboardButton("/set {}".format(long_time))],

                [KeyboardButton("/unset")]]

    reply_markup = ReplyKeyboardMarkup(keyboard)

    update.message.reply_text('Hello Mauri, welcome to code support during hard web development sessions: \n\nPlease make a choice..', reply_markup=reply_markup)


def alarm(bot, job):
    """Function to send the alarm message"""
    first_random = tips[random.randint(0,1)] # will be a list of texts
    second_random = first_random[random.randint(0, len(first_random)-1)] # will be the output text
    bot.send_message(job.context, text=second_random)
    print colored('INFO: ' + second_random, 'green')


def set(bot, update, args, job_queue, chat_data):
    """Adds a job to the queue"""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Sorry we can\'t go back!')
            return

        # Add job to queue
        # job = job_queue.run_once(alarm, due, context=chat_id)
        job = job_queue.run_repeating(alarm, interval=due, first=due, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def unset(bot, update, chat_data):
    """Removes the job if the user changed their mind"""

    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Timer successfully unset!')


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater("YOUR TOKEN HERE")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("set", set,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()