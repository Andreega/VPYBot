from typing import Any

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters, \
    CallbackQueryHandler

from handlers.base_handler import BaseHandler

ONE, TWO, THREE, FOUR = range(4)


class SecondConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('begining', cls.begin)],
            states={
                ONE: [MessageHandler(filters.Regex('^(1|2)$'), cls.one)],
                TWO: [MessageHandler(filters.Regex('^(1|2)$'), cls.two)],
                THREE: [MessageHandler(filters.Regex('^(1|2)$'), cls.three)],
                FOUR: [MessageHandler(filters.Regex('^(1|2)$'), cls.four)],
            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def begin(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton('1'), KeyboardButton('2')],
        ]

        reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await update.message.reply_text(f"""
        Головний герой, Майк, опиняється в таємничому місці, де нічого не пам'ятає.
Вибір: Він може розпочати пошуки вихідного шляху або залишитися на місці та чекати допомоги.
        """,
                                        reply_markup=reply_text)

        return ONE

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Вихід з квесту')

        return ConversationHandler.END

    @staticmethod
    async def one(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == '1':
            keyboard = [
                [KeyboardButton('1'), KeyboardButton('2')],
            ]

            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
            f"""
            Якщо Майк розпочинає пошуки вихіду:
Він знаходить схованку і виявляється в забрудненому підземеллі.
Він натрапляє на розбійників, які атакують його.
            """, reply_markup=reply_text)
            return TWO
        elif answer == '2':
            await update.message.reply_text("""
            Якщо Майк чекає допомоги:
Допомога так і не приходить, і він продовжує чекати.
Він падає жертвою голоду та виснаження.""")
            return ConversationHandler.END

    @staticmethod
    async def two(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == '1':
            keyboard = [
                [KeyboardButton('1'), KeyboardButton('2')],
            ]

            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
                f"""
            Якщо Майк бореться з розбійниками:
Він використовує свої навички та зброю, що знайшов, і перемагає ворогів.
В розбійників є перевага, і вони завдають смертельні поранення Майку.
            """, reply_markup=reply_text)
            return THREE

        elif answer == '2':
            await update.message.reply_text("""
            Якщо Майк обирає втекти від розбійників:
Він виявляється в лабіринті підземелля, де загублюється.
Він втрачає розбійників з поля зору, але потрапляє в пастку, яку вони підготували.
            """)
            return ConversationHandler.END

    @staticmethod
    async def three(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int | Any:
        answer = update.message.text
        if answer == '1':
            keyboard = [
                [KeyboardButton('1'), KeyboardButton('2')],
            ]
            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            await update.message.reply_text(
                f"""
            Якщо Майк вирішує далі досліджувати лабіринт:
Він знаходить вихід і виходить на поверхню.
Він виявляється в западеному місці, де немає можливості виходу.
            """, reply_markup=reply_text)
            return FOUR

        elif answer == '2':
            await update.message.reply_text(
                """
                Якщо Майк спробує знайти вихід самостійно:
Він відкриває нові тунелі, які ведуть його ще глибше в підземелля.
Він падає в пастку і трапляється у павутинній мережі тунелів, де потрапляє під керівництво загадкового монстра.""")
            return ConversationHandler.END

    @staticmethod
    async def four(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == '1':
            await update.message.reply_text(
                f"""
            Якщо Майк знаходить вихід на поверхню:
Він повертається додому, врятувавши себе.
Він виходить на поверхню, але знаходиться в іншому світі, де йому доведеться боротися за виживання.
            """)
            return ConversationHandler.END
        elif answer == '2':
            await update.message.reply_text(
               """
               Якщо Майк потрапляє під керівництво монстра:
Він стає його рабом, виконуючи всі його накази.
Він вирішує вступити в боротьбу з монстром, але виявляється надто слабким, і його з'їдає монстр.""")
            return ConversationHandler.END
        