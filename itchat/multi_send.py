import itchat,time


itchat.auto_login(True)

SINCERE_WISH = 'Happy New Year'

friendList = itchat.get_friends(update=True)[11:]
for friend in friendList:
    print(SINCERE_WISH % (friend['DisplayName'] or friend['NickName']),friend['UserName'])
    time.sleep(.5)


