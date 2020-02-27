
#dar doce py telegram vot bejaye telegram.message masaln bayad update.message ro dar nazar begirim
#bot.bot hamoon telegram.bote

import logging
import sqlite3
from  sqlite3 import Error
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)

        print(sqlite3.version)
        return  conn
    except Error as e:
        print(e)
    return conn

import telegram.bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater,Handler, commandhandler, messagehandler, filters, CommandHandler, MessageHandler, Filters, \
    CallbackQueryHandler, ConversationHandler

NAME,NAME2,PHONE,KART,ADMIN,ADMIN2 =range(6)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
def create_user(id,name=None,photo="AgACAgQAAxkBAAIEm15WxFQJaxkprOLkJTmLPK4Nf2fxAAKRsTEbwXW5UhGNhNSJqsz9_f4hGwAEAQADAgADeQAD_yEFAAEYBA",warn_number=0,is_allowed=0,is_admin=0):
    conn = create_connection("bot2.db")

    cursor = conn.cursor()

    sql = ''' INSERT INTO user(name,id,photo,warn_number,is_allowed,is_admin)
                      VALUES(?,?,?,?,?,?) '''
    user = ( name,id,photo,warn_number,is_allowed,is_admin)
    cursor.execute(sql, user)
    conn.commit()
def search_by_user_id_s(userid,username="None"):
    print(userid)
    print("______")
    users=get_all_users()
    for user in users:
        print(user['id'])
        if user['id']==str(userid):
            print(user)
            return user

    create_user(id=userid,name=username)
    users = get_all_users()
    for user in users:
        if user['id'] == str(userid):
            print(user)
            return user


    #user=None #mire too db user rp ba id peyda mikone va kole usero barmigardoone
    # age nabood None ro return kone
def get_all_users():
    conn = create_connection("bot2.db")

    cursor = conn.cursor()
    e=cursor.execute('SELECT * FROM user')
    users = [{'name': row[0], 'id': row[1],'phone':row[2],'student_number':row[3],'photo':row[4],'warn_number':row[5],'is_allowed':row[6],'is_admin':row[7],'ehraz':row[8]} for row in cursor.fetchall()]
    #print(users)
    #print("_____________")
   # print(e)
    return users

def save_name_s(name2,id):
    conn = create_connection("bot2.db")

    cursor = conn.cursor()
    print(name2)


    sql = '''  UPDATE user
                  SET name = ? 
                  WHERE id = ? '''
    user=(name2,id)
    cursor.execute(sql,user)
    conn.commit()


def save_phone_s(phone,id):
    conn = create_connection("bot2.db")

    cursor = conn.cursor()
    print(phone)
    sql = ''' UPDATE user
                  SET phone = ? 
                  WHERE id = ?'''
    user=(phone,id)
    cursor.execute(sql,user)
    conn.commit()

def save_image_s(file,id):
    print(file)
    conn = create_connection("bot2.db")

    cursor = conn.cursor()

    #with open(file, 'rb') as file:
    #blobData = file.read()
    sql = ''' UPDATE user
                  SET photo = ? 
                  WHERE id = ?'''
    user = (file, id)
    cursor.execute(sql, user)
    conn.commit()




def warn(update, context):
   # print(get_all_users())
    warned_user=update.message.reply_to_message.from_user
    user=search_by_user_id_s(warned_user.id,update.effective_user.username)
    print (warned_user)
    print(user)
    update.message.reply_text(warned_user.first_name+ " اخطار!!!!! اخطار های شما:   "+str(user['warn_number']+1))
    conn = create_connection("bot2.db")
    cursor = conn.cursor()
    sql = ''' UPDATE user
                     SET warn_number = ? 
                     WHERE id = ?'''
    w=user['warn_number']+1

    cursor.execute(sql, (w, warned_user.id))
    conn.commit()
    if user['warn_number']>2:
        context.bot.kick_chat_member(update.message.chat.id, user['id'])


def kick(update,bot):
    admins=bot.bot.get_chat_administrators(update.message.chat.id)
    print(admins.count(admins))
    print(admins[1])
    for admin in admins:
        if update.effective_user.id ==admin.user.id:
         bot.bot.kick_chat_member(update.message.chat.id, update.message.reply_to_message.from_user.id)
         print("alan kick mishe")

def register(update,context):
    print(update)
    users=get_all_users()
    user=search_by_user_id_s(update.effective_user.id,update.effective_user.username)
    print(user)
    if ( user['is_allowed']==0 ) and user['ehraz']==0:
        if user['id']=="985520245":
            return

        update.message.reply_text(
            "{username} شما باید احراز هویت کنید".format(username=update.effective_user.first_name))
        conn = create_connection("bot2.db")
        cursor = conn.cursor()
        sql = ''' UPDATE user
                             SET ehraz = ? 
                             WHERE id = ?'''
        w = user['ehraz'] + 1

        cursor.execute(sql, (w, update.effective_user.id))
        conn.commit()
        update.message.delete()
    elif user['is_allowed']==0 and  user['ehraz']>0:
        update.message.delete()


def start(update,context):
    reply_keyboard = [['ثبت نام', 'ادمین'],
                      ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('انتخاب کنید:', reply_markup=markup)
    return NAME
def zero_state(update,context):
    update.message.reply_text(
        "لطفا نام و نام خانوادگی خود را وارد نمایید:")
    return name

def name(update, context):
    update.message.reply_text(
        "لطفا نام و نام خانوادگی خود را وارد نمایید:")

    #entekhabe user

    print(update.message)
    #context.user_data['choice'] = text
    print(context.user_data)

    return NAME2


def name2(update,context):
    name = update.message.text
    save_name_s(name,update.message.chat.id)
    reply_keyboard = [['بازگشت']
                      ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "لطفا شماره همراه خود را وارد نمایید:",reply_markup=markup)

    return PHONE


def phone(update,context):
    reply_keyboard = [['بازگشت']
                      ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "لطفا عکس از کارت دانشجویی خود بفرستید: ",reply_markup=markup)

    phone1 = update.message.text  # entekhabe user
    save_phone_s(phone1,update.message.chat.id)
    print(context.user_data)
    # context.user_data['choice'] = text
    print(context.user_data)

    return KART

def kart(update,context):
    reply_keyboard = [['بازگشت'],['اتمام']
                      ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "ثبت نام شما انجام شد",reply_markup=markup)
    file=context.bot.getFile(update.message.photo[-1].file_id)
    file.download('photo.jpg')
    print(file)

    save_image_s(update.message.photo[-1].file_id,update.message.chat.id)
    #phone = update.message.  # entekhabe user
    print(context.user_data)
    # context.user_data['choice'] = text
    print(context.user_data)

    return ConversationHandler.END

def admin(update,context):
    print(update)
    user=search_by_user_id_s(update.message.chat.id)
    if user['is_admin']==1:
        reply_keyboard = [['تایید کاربران',],['بازگشت'],
                          ]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text('انتخاب کنید:', reply_markup=markup)
        return ADMIN
    else:
        update.message.reply_text("شما ادمین نیستید")
        return  ConversationHandler.END

def taeed(update,context):
    users=get_all_users()
    i=0

    for user in users:
        i += 1
        if user['is_allowed']==0:
            keyboard = [[InlineKeyboardButton("تایید", callback_data=user["id"])]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text("user number= "+str(i)+"||||| user name= @"+str(user['name']),reply_markup=reply_markup)
            #update.message.reply_text(user['photo'])
            context.bot.send_photo(update.message.chat.id,user['photo'])

    reply_keyboard = [['تایید','عدم تایید'],['بازگشت'],
                      ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('برای تایید هر کاربر شماره ی انرا که در بالا نمایش داده شده بفرستید و یا اینکه بر روی دکمه تایید زیر ان کلیلک کنید:', reply_markup=markup)
    return ADMIN2
def taeed2(update,context):
    choice=update.message.text
    choice2=update.callback_query
    users=get_all_users()
    user=users[int(choice)-1]
    conn = create_connection("bot2.db")
    cursor = conn.cursor()
    sql = ''' UPDATE user
                                 SET is_allowed = ? 
                                 WHERE id = ?'''
    cursor.execute(sql, (1, user['id']))
    conn.commit()
    #for user in users:
       # if user['is_allowed']==0 and user['photo'] !="":
           # cursor.execute(sql, (1, user['id']))
           # conn.commit()


    update.message.reply_text('با موفقیت انجام شد')
    return ADMIN2
def taeed3(update,context):
    choice = update.callback_query.data
    print("++++++++++++++++++")
    print(update)
    print(choice)



    conn = create_connection("bot2.db")
    cursor = conn.cursor()
    sql = ''' UPDATE user
                                     SET is_allowed = ? 
                                     WHERE id = ?'''
    cursor.execute(sql, (1, choice))
    conn.commit()
    # for user in users:
    # if user['is_allowed']==0 and user['photo'] !="":
    # cursor.execute(sql, (1, user['id']))
    # conn.commit()

    update.callback_query.edit_message_text('با موفقیت انجام شد')
    return ADMIN2

def done(update, context):

    update.message.reply_text("ثبت نام موفقیت امیز بود")

    return ConversationHandler.END


def delete_sticker( update,bot):
    #telegram.ext.callbackcontext.CallbackContext

    #print(json.dumps(update.message, indent=4, sort_keys=True))
    print(update)
    print("________________________")

    print((bot.bot.get_chat_administrators(update.message.chat.id)[1]))
    #bot.bot.delete_message(update.message.chat.id,update.message.message_id)
    #bot.bot.restrict_chat_member(update.message.chat.id,736077809,can_send_messages=False)

    if update.effective_user.id==1056410709:

        update.message.reply_text("{username} شما اید احراز هویت کنید".format(username=update.effective_user.first_name))
        update.message.delete()
    if update.effective_message.sticker and update.effective_user.id==1056410709:
        update.message.delete()
        print("sticker delet shod")
    else:
        print("not deleted")



def add_group(update, context):
    print(update.message.supergroup_chat_created)
    update.message.supergroup_chat_created=True
    print(update.message.supergroup_chat_created)
    print(update.message)
    for member in update.message.new_chat_members:
        update.message.reply_text("{username} add group".format(username=member.username))
def trap(update,context):
    pass


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1070197544:AAHsr1Iepf2O5UYgP3lFvOQMektxkrO1RQ8", use_context=True)

    print("connected to database")
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    #add_group_handle = MessageHandler(Filters.text, add_group)
    #gphandler=MessageHandler(Filters.group,gp)
    #dp.add_handler(gphandler)
    #dp.add_handler(add_group_handle)
    kick_handler=CommandHandler('k',kick)
    warn_handler=CommandHandler('w',warn)
    dp.add_handler(warn_handler)
    dp.add_handler(kick_handler)
    dp.add_handler(MessageHandler(Filters.group, register))


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={  # mese state haye nazarias


            NAME: [MessageHandler(Filters.regex('^ثبت نام$'),
                                      name),
                   MessageHandler(Filters.regex('^ادمین$'),
                                  admin),
                   MessageHandler(Filters.regex('^بازگشت$'),
                                  start),

                       ],  # age in state oomad 2ta karo anjam bede ?
            ADMIN:[MessageHandler(Filters.regex('^تایید کاربران$'),
                                  taeed),
                   MessageHandler(Filters.regex('^بازگشت$'),
                                  start),
                   ],
            ADMIN2:[MessageHandler(Filters.regex('^[-+]?[0-9]+$'),
                                  taeed2),
                    CallbackQueryHandler(taeed3),
                    MessageHandler(Filters.regex('^بازگشت$'),
                                   admin),
                   ],
            NAME2: [MessageHandler(Filters.regex("^(?!.*(بازگشت))"),
                                  name2),
                    MessageHandler(Filters.regex('^بازگشت$'),
                                   start),

                   ],

            PHONE: [MessageHandler(Filters.regex("^(?!.*(بازگشت))"),
                                           phone),
                    MessageHandler(Filters.regex('^بازگشت$'),
                                   start),
                            ],

            KART: [MessageHandler(Filters.photo,
                                          kart),
                   MessageHandler(Filters.regex('^بازگشت$'),
                                  name2),
                   MessageHandler(Filters.regex('^اتمام$'),
                                  done),
                           ],

        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )
    dp.add_handler(conv_handler)

    # log all errors

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()