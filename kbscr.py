from keyboa import Keyboa
import telebot as TB
from telebot import types
import dbscr
from datetime import date

def kbexlist (listnumber, chatid):
    allExsizes = dbscr.GetExsize(chatid)
    allExsizes = [w[0] for w in allExsizes]
    allExsizes = allExsizes[::-1]
    allExsizes.insert(0, 'Создать упражнение')
    
    controlls = []
    eight = []
    if listnumber == 0:
        controlls = [' |<< ', 'Далее >>']
    if listnumber > 0 and (listnumber+1) * 9 < len(allExsizes):
        controlls = ['<< Назад', 'Далее >>']
    if (listnumber+1) * 9 >= len(allExsizes):
        controlls = ['<< Назад', ' >>| ']
    if (listnumber+1) * 9 >= len(allExsizes) and listnumber == 0:
        controlls = [' |<< ', ' >>| '] 
    

    if not listnumber * 9 >= len(allExsizes):
        eight = allExsizes[listnumber * 9 : listnumber * 9 + 8]
    else:
        eight = allExsizes[(listnumber-1) * 9 : ]
        print(eight)
    k_eight = Keyboa(items=eight, items_in_row= 2, front_marker="&exsize=", back_marker='').keyboard
    k_controlls = Keyboa(items=controlls, items_in_row=2, front_marker="&fback=", back_marker='').keyboard
    keyboard = Keyboa.combine(keyboards = (k_eight, k_controlls))
    return keyboard

def kbrmbtn(date, gymid):
    Keyboard = Keyboa(items = ['Удалить упражнение', 'Добавить упражнение'], items_in_row=2, front_marker='&deleteoradd=', back_marker= '&' + str(date) + f'&{gymid}').keyboard
    return Keyboard

def kbaddexsize(listnumber, chatid, edata):
    print(f'1:{listnumber}, 2: {chatid}, 3: {edata}')
    allExsizes = dbscr.GetExsize(chatid)
    allExsizes = [w[0] for w in allExsizes]
    allExsizes = allExsizes[::-1]
    allExsizes.insert(0, 'Создать упражнение')
    
    controlls = []
    eight = []
    if listnumber == 0:
        controlls = [' |<< ', 'Далее >>']
    if listnumber > 0 and (listnumber+1) * 9 < len(allExsizes):
        controlls = ['<< Назад', 'Далее >>']
    if (listnumber+1) * 9 >= len(allExsizes):
        controlls = ['<< Назад', ' >>| ']
    if (listnumber+1) * 9 >= len(allExsizes) and listnumber == 0:
        controlls = [' |<< ', ' >>| '] 
    

    if not listnumber * 9 >= len(allExsizes):
        eight = allExsizes[listnumber * 9 : listnumber * 9 + 8]
    else:
        eight = allExsizes[(listnumber-1) * 9 : ]
    print(edata)
    k_eight = Keyboa(items=eight, items_in_row= 2, front_marker="&exsizeadd=", back_marker=edata).keyboard
    k_controlls = Keyboa(items=controlls, items_in_row=2, front_marker="&fbackadd=", back_marker=f'').keyboard
    keyboard = Keyboa.combine(keyboards = (k_eight, k_controlls))
    return keyboard

def kbrmexsize(userid, date, edata):
    exlist = dbscr.GetGymWithoutExsize(userid, date)
    print('exlist: ', exlist)
    exlist.append('<< Назад')
    Keyboard = Keyboa(items = exlist, front_marker='&exdelete=', back_marker=f'&{edata}').keyboard
    return Keyboard
    

def kbgymsdateslist (listnumber, chatid):
    allExsizes = dbscr.GetGymsDates(chatid)
    allExsizes = [w[0] for w in allExsizes]
    allExsizes = allExsizes[::-1]
    
    controlls = []
    eight = []
    if listnumber == 0:
        controlls = [' |<< ', 'Далее >>']
    if listnumber > 0 and (listnumber+1) * 9 < len(allExsizes):
        controlls = ['<< Назад', 'Далее >>']
    if (listnumber+1) * 9 >= len(allExsizes):
        controlls = ['<< Назад', ' >>| ']
    if (listnumber+1) * 9 >= len(allExsizes) and listnumber == 0:
        controlls = [' |<< ', ' >>| '] 
    

    if not listnumber * 9 >= len(allExsizes):
        eight = allExsizes[listnumber * 9 : listnumber * 9 + 8]
    else:
        eight = allExsizes[(listnumber-1) * 9 : ]
    k_eight = Keyboa(items=eight, items_in_row= 2, front_marker="&gyms=", back_marker='').keyboard
    k_controlls = Keyboa(items=controlls, items_in_row=2, front_marker="&fbackgyms=", back_marker='').keyboard
    keyboard = Keyboa.combine(keyboards = (k_eight, k_controlls))
    return keyboard