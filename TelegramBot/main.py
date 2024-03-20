import logging
import random
import clientApp
from telegram import Update, InlineQueryResultArticle,InputTextMessageContent,Message
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler,filters,InlineQueryHandler
from uuid import uuid4
from config import*
import bardApp


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def get_joke_by_id(id):
    msg = await clientApp.get_message_by_id(id)
    if id ==0 or msg == None or msg.text == "" or msg.text == None:
        return "Шутки под таким номером не существует"
    else:
        return "Анекдот номер: {}\n".format(msg.id) +msg.text
    
async def get_random_joke():
    msg = await clientApp.get_random_message()
    while msg == None or msg.text == "" or msg.text == None:
        msg = await clientApp.get_random_message()
    return "Анекдот номер: {}\n".format(msg.id) +msg.text

async def inlinequery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        await context.bot.answer_inline_query(update.inline_query.id,[
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Случайная шутка",
            description="Отправь чтобы узнать шутку",
            input_message_content=InputTextMessageContent(await get_random_joke()) #await get_random_joke()
        )],cache_time=0)
        return
    if not query.isnumeric():
        await context.bot.answer_inline_query(update.inline_query.id, [])
        return
    msg = await get_joke_by_id(int(query))
    await context.bot.answer_inline_query(update.inline_query.id, [
        InlineQueryResultArticle(
            id=query.upper(),
            title='Шутка №{}'.format(query),
            description=msg,
            input_message_content=InputTextMessageContent(msg)
        )])

async def comment_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if(update.message.forward_origin != None):
        print("Aboba")
        if(update.message.forward_origin.chat.id==CHANNEL_ID):
            print("Aboba")
            await clientApp.get_messages_async()
            await update.message.reply_text("Анекдот номер: {}".format(update.message.forward_origin.message_id))
            await start_conversation(update)

async def send_joke_by_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0 or not context.args[0].isnumeric():
        if update.message.from_user.id in IDIOTS_ANSWERS:
            await update.message.chat.send_message(IDIOTS_ANSWERS[update.message.from_user.id])
        else:
            await update.message.chat.send_message("Введенный номер не является числом")
    else:
        await update.message.chat.send_message(await get_joke_by_id(int(context.args[0])))

async def send_random_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_message(await get_random_joke())

async def simulate_self_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        if update.message.from_user.id in IDIOTS_ANSWERS:
            await update.message.chat.send_message(IDIOTS_ANSWERS[update.message.from_user.id])
        else:
            await update.message.chat.send_message("Обсуждать нечего")
        return
    mes = await update.message.chat.send_message(text="ответ может занять время...")
    if context.args[0].isnumeric():
        joke = await get_joke_by_id(int(context.args[0]))
        await mes.edit_text(await start_self_conversation(joke))
        return

    await mes.edit_text(await start_self_conversation(update.message.text))


async def start_conversation(update:Update):
    pers1 = await bardApp.get_random_pers()
    pers2 = await bardApp.get_random_pers()

    comment = await pers1.get_answer_on_joke(update.message.text)
    await update.message.reply_text(comment)

    client_ans = await pers2.get_answer_on_answer(comment)
    await clientApp.send_message(client_ans,update.message.id)

    for i in range(random.randint(0,4)):
        bot_answer =await  pers1.get_answer_on_answer(client_ans)
        client_ans = await pers2.get_answer_on_answer(bot_answer)

        await update.message.reply_text(bot_answer)
        await clientApp.send_message(client_ans,update.message.id)

async def start_self_conversation(text):
    ANSWER = ""

    pers1 = await bardApp.get_random_pers()
    pers2 = await bardApp.get_random_pers()

    comment = await pers1.get_answer_on_joke(text)
    ANSWER += pers1.name + " Flex Operator: "+comment + "\n\n\n"
    client_ans = await pers2.get_answer_on_answer(comment)
    ANSWER += pers2.name + " Adats: "+client_ans + "\n\n\n"
    for i in range(random.randint(0,4)):
        bot_answer =await  pers1.get_answer_on_answer(client_ans)
        ANSWER += pers1.name + " Flex Operator: "+bot_answer + "\n\n\n"
        client_ans = await pers2.get_answer_on_answer(bot_answer)
        ANSWER += pers2.name + " Adats: "+client_ans + "\n\n\n"
    
    return ANSWER


    

    



if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(InlineQueryHandler(inlinequery))
    application.add_handler( MessageHandler(filters=filters.Chat(CHAT_ID),callback=comment_joke))
    application.add_handler( CommandHandler(command="joke",callback=send_joke_by_id))
    application.add_handler( CommandHandler(command="conv",callback=simulate_self_conversation))
    application.add_handler(CommandHandler("rand",callback=send_random_joke))

    with clientApp.client:
        clientApp.get_messages()
        application.run_polling()
