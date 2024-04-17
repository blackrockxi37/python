from datetime import date

def Parse(text):
    try:
        a = text.split('\n')
        for i in range(len(a)):
            a[i] = a[i].split()
        return a
    except Exception as er:
        return f"exceprion: {type(er).__name__}"
def antiParse(l):
    a = ''
    try:
        for i in l:
            a += f'{i[0]}          {i[1]}\n'
        return a
        
    except Exception as er:
        return f"exceprion: {type(er).__name__}"

def msgParse(msg, n):
    arr = msg.split('&')
    return arr[n]

def dataParce(data):
    print(data)
    return int(data)

