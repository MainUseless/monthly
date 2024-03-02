from datetime import datetime
import gkeepapi
import time
import os

#https://accounts.google.com/b/0/DisplayUnlockCaptcha

startDate = "25"
monthIncome = "3000"


keep = gkeepapi.Keep()
success = keep.login(os.environ['email'], os.environ['password'])
today = datetime.today()


def get_date(x):
    if today.strftime("%d") < startDate:
        month = datetime.now().month - 1
    else:
        month = datetime.now().month

    if month < 1:
        month = 1
        year = datetime.now().year - 1
    else:
        year = datetime.now().year

    return startDate + "/" + str(month - x) + "/" + str(year)


# 0 is the initial value of x as it will search in the current month
# if it doesn't find the note it then reduces the month by 1 then
# calculates the final sum of that month , archives the note and
# create a new note for the ongoing month
def do_some_magic(x):
    allNotes = keep.all()
    dDate = get_date(x)

    if x == 1:
        for note in allNotes:
            if note.title == dDate:
                sum_note(note)
                note.archived = True
        note = keep.createNote(get_date(0), monthIncome + '\n-1')
        note.color = gkeepapi.node.ColorValue.Purple
        return

    for note in allNotes:
        if note.title == dDate:
            sum_note(note)
            return

    do_some_magic(1)


def sum_note(note):
    temp = 0
    arr = []
    optional, _H = "", ""
    arr = note.text.split()
    for i in range(1, len(arr)):
        if arr[i] == '-1': break
        if arr[i].isdigit():
            temp += int(arr[i])

    if arr[0] > '0': optional = " (R : " + str(int(arr[0]) - temp) + ")"

    #delete the last line of the note as it will be updated
    Note = note.text.splitlines(True)
    del Note[len(Note) - 1]

    #write the original content + the calculated sum
    H = datetime.now().hour + 2
    if H >= 24:
        H -= 24
        _H = "0" + str(H)
    else:
        _H = str(H)
    note.text = ("".join(str(x) for x in Note) +
                 today.strftime("%d/%m/%Y : (" + _H + ":%M)") + ' : ' +
                 str(temp) + optional)


if __name__ == '__main__':
    while True:
        do_some_magic(0)
        keep.sync()
        time.sleep(60*60*24*7)  # 1 week
