import telebot as TB
from telebot import types
from dbscr import *
from kbscr import *
import prsrc

bot = TB.TeleBot('6659217278:AAEOXOerD_7_IQt_dih3HdYSqRRYy8snFAA')

buttons = Buttons()
UsersConnectDB()


@bot.message_handler(commands=["start"])
def start(message, res=False):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        teleitem1 = types.KeyboardButton(buttons[0])
        teleitem2 = types.KeyboardButton(buttons[1])
        markup.add(teleitem1)
        markup.add(teleitem2)
        AddUser(message.chat.id, message.from_user.username)
        premsg = bot.send_message(message.chat.id, f'Нажми: \n{buttons[0]} для добавления тренировки\n{buttons[1]} — для просмотра тренировок ',  reply_markup=markup).message_id
        SetUserPremsg(premsg, message.chat.id)
        SetUserBase('', message.chat.id)
        
        

@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        functions(message.text.strip(), message)
    except Exception as er:
      bot.send_message(message.chat.id, f"exceprion: {type(er).__name__}, {str(er)}")



def functions(button, message):
  base = GetUserBase(message.chat.id)
  if button == buttons[1]:
      OnDelete(message.chat.id)
      premsg = bot.send_message(message.chat.id, 'Страница 1', reply_markup=kbgymsdateslist(0, message.chat.id)).message_id
      SetUserKbmsg(premsg, message.chat.id)
      return
  if button == buttons[0]: # добавить тренировку
    OnDelete(message.chat.id)
    premsg = bot.send_message(message.chat.id, 'Страница 1', reply_markup=kbexlist(0, message.chat.id)).message_id
    SetUserPremsg(premsg, message.chat.id)
    SetUserBase('', message.chat.id)
    AddGym(message.chat.id, message.from_user.username)
    return
  
  if 'Создание упражнения 2' in GetUserBase(message.chat.id):
      gymid = base.split('&')[1]
      AddExsize(message.chat.id, gymid, button, 0)
      premsg = GetUserPremsg(message.chat.id)
      AddOnDelete(message.chat.id, premsg)
      AddOnDelete(message.chat.id, message.id)
      OnDelete(message.chat.id)
      SetUserBase('', message.chat.id)
      bot.edit_message_reply_markup(chat_id= message.chat.id, message_id=GetUserKbmsg(message.chat.id), reply_markup=kbaddexsize(0, message.chat.id, gymid))

  if GetUserBase(message.chat.id) == 'Создание упражнения':
      AddExsize(message.chat.id, GetLastGymId(message.chat.id), button, 0)
      premsg = GetUserPremsg(message.chat.id)
      AddOnDelete(message.chat.id, premsg)
      AddOnDelete(message.chat.id, message.id)
      OnDelete(message.chat.id)
      SetUserBase("",message.chat.id)
      bot.edit_message_reply_markup(chat_id= message.chat.id, message_id=GetUserKbmsg(message.chat.id), reply_markup=kbexlist(0, message.chat.id))

  if 'Добавление подходов1' in GetUserBase(message.chat.id):
      exname = GetUserBase(message.chat.id).split('&')[1]
      SetUserBase("", message.chat.id)
      premsg = GetUserPremsg(message.chat.id)
      AddOnDelete(message.chat.id, premsg)
      AddOnDelete(message.chat.id, message.id)
      OnDelete(message.chat.id)
      msg = prsrc.Parse(button)
      exid = GetExIdByName(exname, message.chat.id)
      for i in msg:
        try:
            int(i[0])
            int(i[1])
        except:
            premsg = bot.send_message(chat_id=message.chat.id, text= 'Пожалуйста, используйте целые числа, умоляю!').message_id
            AddOnDelete(message.chat.id, premsg)
            SetUserBase(f"Добавление подходов1&{exname}")
            return
        AddSet(exid, i)
      responce = GetLastUserGym(message.chat.id)
      print('Первая версия')
      premsg = bot.send_message(chat_id=message.chat.id, text= 'Ваша тренировка:\n' + responce).message_id
      AddOnDelete(message.chat.id, premsg)
      SetUserPremsg(premsg, message.chat.id)

  if 'Добавление подходов2' in GetUserBase(message.chat.id):
      print('Вторая версия')
      exname = GetUserBase(message.chat.id).split('&')[1]
      gymid = GetUserBase(message.chat.id).split('&')[2]
      print('exname: ', exname, 'gymid: ', gymid)
      SetUserBase("", message.chat.id)
      premsg = GetUserPremsg(message.chat.id)
      AddOnDelete(message.chat.id, premsg)
      AddOnDelete(message.chat.id, message.id)
      OnDelete(message.chat.id)
      msg = prsrc.Parse(button)
      exid = GetExIdByNameAndGym(exname,gymid, message.chat.id)
      for i in msg:
        try:
            int(i[0])
            int(i[1])
        except:
            premsg = bot.send_message(chat_id=message.chat.id, text= 'Пожалуйста, используйте целые числа, умоляю!').message_id
            AddOnDelete(message.chat.id, premsg)
            SetUserBase(f"Добавление подходов2&{exname}&{gymid}")
            return
        AddSet(exid, i)
      responce = GetGymById(message.chat.id, gymid)

      gymdate = GetGymDateById(message.chat.id, gymid)
      premsg = bot.send_message(chat_id=message.chat.id, text= 'Ваша тренировка:\n' + responce, reply_markup=kbrmbtn(gymdate, gymid)).message_id
      AddOnDelete(message.chat.id, premsg)
      SetUserPremsg(premsg, message.chat.id)
      


  

@bot.callback_query_handler(func=lambda call: True)
def buttonhandler(call):
    kbmsg = call.message.id
    SetUserKbmsg(kbmsg,call.from_user.id)
    if call.data == '&exsize=Создать упражнение':
        premsg = bot.send_message(call.from_user.id, 'Введите название упражнения').message_id
        AddOnDelete(call.from_user.id, premsg)
        SetUserPremsg(premsg, call.from_user.id)
        SetUserBase("Создание упражнения", call.from_user.id)
    if call.data == '&fback=Далее >>':
        page = int(call.message.text.split()[1])
        bot.edit_message_text(chat_id= call.from_user.id, message_id=kbmsg, text = 'Страница '+ str(page+1), reply_markup=kbexlist(page, call.from_user.id))
    if call.data == '&fback=<< Назад':
        page=  int(call.message.text.split()[1])
        bot.edit_message_text(chat_id= call.from_user.id, message_id=kbmsg, text = 'Страница '+ str(page-1), reply_markup=kbexlist(page-2, call.from_user.id))

    if '&exsize=' in call.data and call.data != '&exsize=Создать упражнение': #Добавление в упражнение подходов и повторений
        msg = call.data.replace('&exsize=', '')
        premsg = bot.send_message(chat_id= call.from_user.id, text = 'Введите вес и повторения\nНа предыдущей тренировке:\nВес  /  Повторы\n' + prsrc.antiParse(GetLastExRetsById(call.from_user.id, msg))).message_id
        AddOnDelete(call.from_user.id, premsg)
        SetUserPremsg(premsg, call.from_user.id)
        SetUserBase(f"Добавление подходов1&{msg}", call.from_user.id)
    
    if call.data == '&fbackgyms=Далее >>':
        page = int(call.message.text.split()[1])
        bot.edit_message_text(chat_id= call.from_user.id, message_id=kbmsg, text = 'Страница '+ str(page+1), reply_markup=kbgymsdateslist(page, call.from_user.id))

    if call.data == '&fbackgyms=<< Назад':
        page=  int(call.message.text.split()[1])
        bot.edit_message_text(chat_id= call.from_user.id, message_id=kbmsg, text = 'Страница '+ str(page-1), reply_markup=kbgymsdateslist(page-2, call.from_user.id))

    if '&gyms=' in call.data: 
        msg = call.data.replace('&gyms=', '')
        gymstring = GetGymByDate(call.from_user.id, msg)
        gymid = GetGymIdByDate(call.from_user.id, msg)
        OnDelete(call.from_user.id)
        premsg = bot.send_message(chat_id= call.from_user.id, text = f'Ваша тренировка {msg}:\n{gymstring}', reply_markup=kbrmbtn(msg, gymid)).message_id
        AddOnDelete(call.from_user.id, premsg)
        SetUserPremsg(premsg, call.from_user.id)

    if '&deleteoradd=' in call.data:
        OnDelete(call.from_user.id)
        msg = call.data.replace('&deleteoradd=', '').split('&')
        data = msg[1].replace(' ', '')
        gymid = msg[2]
        msg = msg[0]
        if msg == 'Удалить упражнение':
            premsg = bot.send_message(chat_id=call.from_user.id, text='Выберете упражнение для удаления', reply_markup=kbrmexsize(call.from_user.id, data, gymid)).message_id
        elif msg == 'Добавить упражнение':
            print(len(data.encode('utf-8')))
            premsg = bot.send_message(chat_id=call.from_user.id, text='Страница 1', reply_markup=kbaddexsize(0, call.from_user.id, data)).message_id
        AddOnDelete(call.from_user.id, premsg)

    if call.data == '&fbackadd=Далее >>':
        page = int(call.message.text.split()[1])
        bot.edit_message_text(chat_id= call.from_user.id, message_id=kbmsg, text = 'Страница '+ str(page+1), reply_markup=kbaddexsize(page, call.from_user.id))

    if call.data == '&fbackadd=<< Назад':
        page=  int(call.message.text.split()[1])
        bot.edit_message_text(chat_id= call.from_user.id, message_id=kbmsg, text = 'Страница '+ str(page-1), reply_markup=kbaddexsize(page-2, call.from_user.id))
    if call.data == '&fbackadd= |<< ':
        AddOnDelete(call.from_user.id, kbmsg)
        OnDelete(call.from_user.id)

    if '&exsizeadd=' in call.data and '&exsizeadd=Создать упражнение' not in call.data:
        msg = call.data.replace('&exsizeadd=', '').split('&')
        gymdate = msg[1]
        msg = msg[0]
        gymid = GetGymIdByDate(call.from_user.id, gymdate)
        premsg = bot.send_message(chat_id= call.from_user.id, text = 'Введите вес и повторения\nНа предыдущей тренировке:\nВес  /  Повторы\n' + prsrc.antiParse(GetLastExRetsById(call.from_user.id, msg))).message_id
        AddOnDelete(call.from_user.id, premsg)
        exnames = GetExNamesByGymId(call.from_user.id, gymid)
        if msg not in exnames:
            AddExsize(call.from_user.id, gymid, msg, GetOrigId(call.from_user.id, msg))
        SetUserBase(f'Добавление подходов2&{msg}&{gymid}', call.from_user.id)

    if '&exsizeadd=Создать упражнение' in call.data:
        msg = call.data.replace('&exsizeadd=', '').split('&')
        gymdate = msg[1]
        msg = msg[0]
        gymid = GetGymIdByDate(call.from_user.id, gymdate)
        premsg = bot.send_message(call.from_user.id, 'Введите название упражнения').message_id
        AddOnDelete(call.from_user.id, premsg)
        SetUserPremsg(premsg, call.from_user.id)
        SetUserBase(f'Создание упражнения 2&{gymid}', call.from_user.id)
    if '&exdelete' in call.data:
        OnDelete(call.from_user.id)
        msg = call.data.replace('&exdelete=', '').split('&')
        edata = msg[1]
        msg = msg[0]
        if msg != '<< Назад':
            RemoveExsize(userid = call.from_user.id, gymid=edata, name=msg)
        if msg == '<< Назад':
            OnDelete(call.from_user.id)
        
        

            
        


def OnDelete(userid):
    try:
      msgs = GetOnDelete(userid)
      bot.delete_messages(chat_id=userid, message_ids=msgs)
      DeleteOnDelete(userid)
    except Exception as er:
        print('delete error: ', {er})
        return f"exceprion: {er}"

bot.polling(none_stop=True, interval=0)


