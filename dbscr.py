import sqlite3
from datetime import date

dbUserpath = './db/users.db'
def Buttons():
    dbpath = './db/database.db'
    connection = sqlite3.connect(dbpath)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Buttons')
    buttons = cursor.fetchall()
    connection.close()

    buttons = [str(i[0]) for i in buttons]
    print(buttons)
    return buttons

def UsersConnectDB():
    dbUserpath = './db/users.db'
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            userid INTEGER,
            username TEXT NOT NULL,
            userbase TEXT,
            userpremsg INTEGER,
            userkbmsg INTEGER
    );
    CREATE TABLE IF NOT EXISTS Gyms (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            username TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(id)
    );
    CREATE TABLE IF NOT EXISTS Exsizes (
            id INTEGER PRIMARY KEY,
            gym_id INTEGER,
            user_id INTEGER,
            name TEXT NOT NULL,
            original INTEGER,
            FOREIGN KEY (gym_id) REFERENCES Gyms(id),
            FOREIGN KEY (user_id) REFERENCES Users(id)
    );
    CREATE TABLE IF NOT EXISTS Reps (
            id INTEGER PRIMARY KEY,
            exsize_id INTEGER,
            sets INTEGER,
            reps INTEGER,
            FOREIGN KEY (exsize_id) REFERENCES Exsizes(id)
    );
    CREATE TABLE IF NOT EXISTS OnDelete (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            message_id INTEGER
    )
    """)
    connection.commit()
    connection.close()

def AddUser(userid, username):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    for u in users:
        if u[1] == userid:
            print(u[2])
            if u[2] != username:
                cursor.execute('UPDATE Users SET username = ? WHERE userid = ?', (username, userid))
                connection.commit()
            return
        

    cursor.execute('SELECT COUNT(*) FROM Users')
    total_users = cursor.fetchone()[0]
    cursor.execute('INSERT INTO Users (id, userid, username, userbase, userpremsg, userkbmsg) VALUES (?,?,?,?,?,?)', (total_users + 1, f'{userid}', f'{username}', '', 0, 0))
    
    connection.commit()
    connection.close()


def AddGym(userid, username):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM Gyms WHERE user_id = ? AND date = ?', (userid, str(date.today()), ))
    total_gyms = cursor.fetchone()[0]
    print('tG: ', total_gyms)
    if total_gyms == 0: 
        cursor.execute('SELECT COUNT(*) FROM Gyms')
        total_gyms = cursor.fetchone()[0]
        cursor.execute('INSERT INTO Gyms (id, user_id, username, date) VALUES (?,?,?,?)', (total_gyms + 1, userid, username, str(date.today())))
        connection.commit()
        connection.close()
    else:
        connection.commit()
        connection.close()
def GetGymIdByDate(userid, date):
    connection = sqlite3.connect(dbUserpath)
    cursore = connection.cursor()
    cursore.execute('SELECT id FROM Gyms WHERE date = ? AND user_id = ?', (str(date), userid, ))
    gymid = cursore.fetchone()
    gymid = gymid[0]
    connection.close()
    print (gymid)
    return gymid

def GetGymDateById(userid, gymid):
    connection = sqlite3.connect(dbUserpath)
    cursore = connection.cursor()
    cursore.execute('SELECT date FROM Gyms WHERE id = ? AND user_id = ?', (gymid, userid, ))
    gymid = cursore.fetchone()
    gymid = gymid[0]
    connection.close()
    print (gymid)
    return gymid

def GetGymByDate(userid, date):
    string = ''
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM Gyms WHERE user_id = ? AND date = ?', (userid, str(date), ))
    gymid = cursor.fetchall()
    gymid = gymid[0][0]
    cursor.execute('SELECT id FROM Exsizes WHERE gym_id = ? ', (gymid, ))
    exids = cursor.fetchall()
    exids = list(map(list, exids))
    exids = [w[0] for w in exids]
    setlist = []
    for e in exids:
        cursor.execute('SELECT * FROM Reps WHERE exsize_id = ? ', (e, ))
        setlist.append(cursor.fetchall())
    cursor.execute('SELECT name FROM Exsizes WHERE gym_id = ? ', (gymid, ))
    exnames = cursor.fetchall()
    exnames = list(map(list, exnames))
    exnames =  [w[0] for w in exnames]
    print ('exnames before: ', exnames)
    temp = []
    for i in exnames:
        if i not in temp:
            temp.append(i)
    exnames = temp
    print ('exnames2: ', exnames)
    for i in range(len(exnames)):
        string += f'{exnames[i]}:\n'
        for j in setlist[i]:
            string += f'{j[2]} {j[3]}\n'
    return string
def GetGymById(userid, gymid):
    string = ''
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM Exsizes WHERE gym_id = ? ', (gymid, ))
    exids = cursor.fetchall()
    exids = list(map(list, exids))
    exids = [w[0] for w in exids]
    setlist = []
    for e in exids:
        cursor.execute('SELECT * FROM Reps WHERE exsize_id = ? ', (e, ))
        setlist.append(cursor.fetchall())
    cursor.execute('SELECT name FROM Exsizes WHERE gym_id = ? ', (gymid, ))
    exnames = cursor.fetchall()
    exnames = list(map(list, exnames))
    exnames =  [w[0] for w in exnames]
    for i in range(len(exnames)):
        string += f'{exnames[i]}:\n'
        for j in setlist[i]:
            string += f'{j[2]} {j[3]}\n'
    return string

def GetGymWithoutExsize(userid, date):
    string = ''
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM Gyms WHERE user_id = ? AND date = ?', (userid, str(date), ))
    gymid = cursor.fetchall()
    gymid = gymid[0][0]
    cursor.execute('SELECT name FROM Exsizes WHERE gym_id = ? ', (gymid, ))
    exnames = cursor.fetchall()
    exnames = list(map(list, exnames))
    exnames =  [w[0] for w in exnames]
    return exnames

def GetLastUserGym(userid):
    string = ''
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM Gyms WHERE user_id = ? ', (userid, ))
    gymid = cursor.fetchone()[0]
    cursor.execute('SELECT id FROM Exsizes WHERE gym_id = ? ', (gymid, ))
    exids = cursor.fetchall()
    exids = list(map(list, exids))
    exids = [w[0] for w in exids]
    setlist = []
    for e in exids:
        cursor.execute('SELECT * FROM Reps WHERE exsize_id = ? ', (e, ))
        setlist.append(cursor.fetchall())
    cursor.execute('SELECT name FROM Exsizes WHERE gym_id = ? ', (gymid, ))
    exnames = cursor.fetchall()
    exnames = list(map(list, exnames))
    exnames =  [w[0] for w in exnames]
    for i in range(len(exnames)):
        string += f'{exnames[i]}:\n'
        for j in setlist[i]:
            string += f'{j[2]} {j[3]}\n'

    return string


def GetGymsDates(userid):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute(f'SELECT date FROM Gyms WHERE user_id = ?', (userid, ))
    ex = cursor.fetchall()
    ex = list(map(list, ex))
    return ex

def GetLastGymId(userid):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM Gyms WHERE user_id = ?', (userid, ))
    gymids = cursor.fetchall()
    gymids = list(map(list, gymids))
    try:
        total = gymids[-1][0]
    except:
        AddGym(userid, username='NULL')
        cursor.execute('SELECT id FROM Gyms WHERE user_id = ?', (userid, ))
        gymids = cursor.fetchall()
        gymids = list(map(list, gymids))
        total = gymids[-1][0]
    print('last Gym id: ', total)
    connection.commit()
    connection.close()
    return total
def GetExNamesByGymId(userid, gymid):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT name FROM Exsizes WHERE gym_id = ? AND user_id = ?', (gymid, userid, ))
    exnames = cursor.fetchall()
    exnames = list(map(list, exnames))
    exnames = [e[0] for e in exnames]
    connection.close()
    return exnames

def AddExsize(userid, gymid, name, original):
    print("userid, gymid, name, original",userid, gymid, name, original)
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM Exsizes')
    total_ex = cursor.fetchone()[0]
    print('total_ex : ', total_ex)
    cursor.execute('INSERT INTO Exsizes (id, user_id, gym_id, name, original) VALUES (?,?,?,?,?)', (total_ex + 1, userid, gymid, name, original))
    connection.commit()
    connection.close()
def GetOrigId(userid, exname):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM Exsizes WHERE user_id = ? AND name = ? AND original = 0', (userid, exname))
    value = cursor.fetchone()[0]
    if value is None:
        return 0
    return value

def RemoveExsize(userid, gymid, name):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT id FROM Exsizes WHERE user_id = ? AND name = ? AND gym_id = ?', (userid, name, gymid, ))
        exid = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM Reps WHERE exsize_id = ? ', (exid, ))
        num = cursor.fetchone()[0]
        cursor.execute('SELECT id FROM Reps WHERE exsize_id = ?', (exid, ))
        id = cursor.fetchall()[-1][0]
        print('id : ', id)
        cursor.execute('DELETE FROM Reps WHERE exsize_id = ?', (exid, ))
        cursor.execute('UPDATE Reps SET id = id - ? WHERE id > ?', (num, id, ))
        cursor.execute('UPDATE Exsizes SET gym_id = 0 WHERE id = ?', (exid, ))
        
    except Exception as er:
        try:
            cursor.execute('UPDATE Exsizes SET gym_id = 0 WHERE id = ?', (exid, ))
        except:
            print('second exception')
        print('exception ' + str(er))
    connection.commit()
    connection.close()
    

def GetExsize(userid): # Для списка всех пользователльский упражнений
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute(f'SELECT name FROM Exsizes WHERE user_id = ?', (userid, ))
    ex = cursor.fetchall()
    ex = list(map(list, ex))
    temp = []
    for e in ex:
        if e not in temp:
            temp.append(e)
    ex = temp
    return ex

def GetExIdByName(exname, userid):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute(f'SELECT id FROM Exsizes WHERE name = ? AND user_id = ?', (exname, userid))
    ex = cursor.fetchall()
    ex = list(map(list, ex))[0][0]
    connection.commit()
    connection.close()
    return ex

def GetExIdByNameAndGym(exname, gymid, userid):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute(f'SELECT id FROM Exsizes WHERE name = ? AND user_id = ? AND gym_id = ?', (exname, userid, gymid, ))
    ex = cursor.fetchall()
    ex = list(map(list, ex))[0][0]
    connection.commit()
    connection.close()
    return ex

def AddSet(exid, setrep):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM Reps')
    total_sets = cursor.fetchone()[0]
    try:
        int(setrep[0])
        int(setrep[1])
    except:
        setrep[0] = 0
        setrep[1] = 0
    cursor.execute('INSERT INTO Reps (id, exsize_id, sets, reps) VALUES (?,?,?,?)', (total_sets + 1, exid, int(setrep[0]), int(setrep[1])))
    connection.commit()
    connection.close()

def GetUserBase(userid):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute(f'SELECT userbase FROM Users WHERE userid = ?', (userid, ))
    ex = cursor.fetchall()
    ex = list(map(list, ex))[0][0]
    connection.commit()
    connection.close()
    return ex
def SetUserBase(userbase, userid):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET userbase = ? WHERE userid = ?', (userbase, userid))
    connection.commit()
    connection.close()
    
def GetUserPremsg(userid):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute(f'SELECT userpremsg FROM Users WHERE userid = ?', (userid, ))
    ex = cursor.fetchall()
    ex = list(map(list, ex))[0][0]
    connection.commit()
    connection.close()
    return ex
def SetUserPremsg(userpremsg, userid):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET userpremsg = ? WHERE userid = ?', (userpremsg, userid))
    connection.commit()
    connection.close()

def GetUserKbmsg(userid):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute(f'SELECT userkbmsg FROM Users WHERE userid = ?', (userid, ))
    ex = cursor.fetchall()
    ex = list(map(list, ex))[0][0]
    connection.commit()
    connection.close()
    return ex
def SetUserKbmsg(userkbmsg, userid):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET userkbmsg = ? WHERE userid = ?', (userkbmsg, userid))
    connection.commit()
    connection.close()

def GetLastExRetsById(userid, exname):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    exIdByName = GetExIdByName(exname, userid)
    cursor.execute('SELECT sets, reps FROM Reps WHERE exsize_id = ? ', (exIdByName, ))
    reps = cursor.fetchall()
    reps = list(map(list, reps))
    print(reps)
    connection.commit()
    connection.close()
    return reps
    



def WatchAllUsers():
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    for user in users:
        print(user)
    connection.close()

def WatchAllGyms():
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Gyms')
    gyms = cursor.fetchall()
    for gym in gyms:
        print(gym)
    connection.close()

def DeleteAllGymsByUserId(userid, flag = False):
    if flag:
        connection = sqlite3.connect(dbUserpath)
        cursor = connection.cursor()
        cursor.execute('DELETE FROM Gyms WHERE user_id = ?', (userid,))
        connection.commit()
        connection.close()

def DeleteAllEx():
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Exsizes WHERE user_id = ?', (316009566,))
    connection.commit()
    connection.close()

def DeleteLastEx():
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Exsizes WHERE user_id = ? AND id = (SELECT MAX(id) FROM Exsizes)', (316009566,))
    connection.commit()
    connection.close()

def WatchEx():
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Exsizes')
    exs = cursor.fetchall()
    for ex in exs:
        print(ex)
    connection.close()

def SetNullBases():
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET userbase = ?', ("", ))
    connection.commit()
    connection.close()

def GetOnDelete(userid):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT message_id FROM OnDelete WHERE user_id = ?', (userid, ))
    reps = cursor.fetchall()
    reps = list(map(list, reps))
    reps = [r[0] for r in reps]
    connection.close()
    return reps

def AddOnDelete(userid, mid):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM OnDelete')
    total_ids = cursor.fetchone()[0]
    print((total_ids + 1, userid, mid, ))
    cursor.execute('INSERT OR REPLACE INTO OnDelete (id, user_id, message_id) VALUES (?,?,?)', (total_ids + 1, userid, mid, ))
    connection.commit()
    connection.close()
    

def DeleteOnDelete(userid):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('DELETE FROM OnDelete WHERE user_id = ?', (userid, ))
    connection.commit()
    connection.close()