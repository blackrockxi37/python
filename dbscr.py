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

def GetGymByDate(userid, date):
    string = ''
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM Gyms WHERE user_id = ? AND date = ?', (userid, str(date), ))
    gymid = cursor.fetchall()
    print('date: ', date)
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
    for i in range(len(exnames)):
        string += f'{exnames[i]}:\n'
        for j in setlist[i]:
            string += f'{j[2]} {j[3]}\n'
    print("<->", string)
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
    print('gymid: ', gymid)
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

def AddExsize(userid, gymid, name):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM Exsizes')
    total_ex = cursor.fetchone()[0]
    print('total_ex : ', total_ex)
    cursor.execute('INSERT INTO Exsizes (id, user_id, gym_id, name) VALUES (?,?,?,?)', (total_ex + 1, userid, gymid, name))
    connection.commit()
    connection.close()

def RemoveExsize(userid, gymid, name):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT id FROM Exsizes WHERE user_id = ? AND name = ? AND gym_id = ?', (userid, name, gymid, ))
        num = cursor.fetchone()[0]
        cursor.execute('DELETE FROM Exsizes WHERE user_id = ? AND name = ? AND gym_id = ?', (userid, name, gymid, ))
        cursor.execute('UPDATE Exsizes SET id = id - 1 WHERE id > ?', (num, ))
    except Exception as er:
        print('exception ' + str(er))
    connection.commit()
    connection.close()
    

def GetExsize(userid): # Для списка всех пользователльский упражнений
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute(f'SELECT name FROM Exsizes WHERE user_id = ?', (userid, ))
    ex = cursor.fetchall()
    ex = list(map(list, ex))
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

def AddSet(exid, setrep):
    connection = sqlite3.connect(dbUserpath)
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM Reps')
    total_sets = cursor.fetchone()[0]
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