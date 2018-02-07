#coding=gbk
__author__ = 'ertuil'
__version__ = '0.0.1'

########################################################################
########## import ######################################################
########################################################################

import itchat
import time
import re
import requests
import threading
import shutil  
import os

########################################################################
########## Config ######################################################
########################################################################

'''
����ģ�飬�������ó��ñ���
'''

robot_on = True    # �������ܻ�����
group_on = True    # ������Ⱥ�Ŀ���
retrieve_on = True # ������Ϣ��¼          
api_url = 'http://www.tuling123.com/openapi/api'
apikey = '3163c880d11144f78fd8549c5f269f93'
robot_name = 'R'     # ����������
self_name = 'dazi'      # �Լ�������
call_name = 'Dear'         # �Կͳƺ�
max_list = 3            # ���š����׵���Ŀ��

event_time = 3600        # ѭ�����ͽ�����Ϣ��   



self_local = 'NB'       # ��ѯ�����ĵص�
ask_list = ['������'] # ����ÿ�չ��ĵ�Ⱥ�б�
ask_time = 6 # ����ÿ�����������ŵ�ʱ��
 
known_names = []
is_on = True

########################################################################
########## utils #######################################################
########################################################################

def self_command(cmds):
    '''
    ����������ͨ��΢�Ÿ��Լ�����ָ����ƻ����˵Ŀ��صȡ�
    '''
    flag = True
    global is_on
    global robot_on
    global group_on
    global retrieve_on
    if cmds == '�˳�':
        is_on = False
        quit_app()
        logs('���� �˳�')
    elif cmds == '����':
        robot_on = True
        logs('���� robot��\t'+str(robot_on))
    elif cmds == '�ر�':
        robot_on = False
        logs('���� robot��\t'+str(robot_on))
    elif cmds == 'Ⱥ������':
        group_on = True
        logs('���� group��\t'+str(group_on))
    elif cmds == 'Ⱥ�Ĺر�':
        group_on = False
        logs('���� group��\t'+str(group_on))
    elif cmds == '��¼����':
        retrieve_on = True
        logs('���� retrieve��\t'+str(retrieve_on))
    elif cmds == '��¼�ر�':
        retrieve_on = False
        logs('���� retrieve��\t'+str(retrieve_on))
    elif cmds == '������':
        clear_cache()
        logs('���� ������')
    elif cmds == '�ʺ�':
        sent_hello()
    else :
        flag = False
    return flag
    

def logs(obg):
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\t'+obg)

def clear_cache():
    '''
    ������ػ������Ƭ���ȡ�
    '''
    shutil.rmtree('./tmp')  
    os.mkdir('./tmp')  


def clear_list():
    logs('Clearing list')
    known_names.clear()



########################################################################
########## events ######################################################
########################################################################

'''
�¼���Ѷ����
'''

def events():
    '''
    �����¼�������¼�ѭ�����ƣ���ʱ��������б�ÿ�춨ʱ����������
    '''
    global timer
    global is_on
    clear_list()
    if int(time.strftime("%H", time.localtime())) == ask_time:
        sent_hello()
    if is_on:
        timer = threading.Timer(event_time, events)
        timer.start()

def quit_app():
    '''
    ���յ��˳��źţ��رն�ʱ����ע��΢��
    '''
    global timer
    timer.cancel()
    itchat.logout()

########################################################################
########## robot  ######################################################
########################################################################

'''
ͼ��������Ƚӿ�
'''

def get_response(msg, user_id,loc = ''):
    '''
    ����ͼ������ˡ�����������ķ��ص�json��
    ����:     msg:������ı�
             user_id: �û�id
             loc����ѡ��λ����Ϣ
             ���أ�һ�����жԻ����ݵ�list����
    '''

    data = {'key': apikey,
            'info': msg,
            'userid': user_id
            }
    if not loc == '':
        data['loc'] = loc
    logs(str(data))
    try:
        req = requests.post(api_url, data=data).json()
    except:
        return ''

    code = req.get('code')
    logs(str(req))

    text = re.sub('^��',call_name,req.get('text'))

    if code == 100000 :
        return (robot_name+"(С����):"+text,)
    elif code == 200000:
        return robot_name+"(С����):"+text , req.get('url')
    elif code == 302000:
        ans = [robot_name+"(С����):"+text,]
        news = req.get('list')
        idx = 0
        while idx < len(news) and idx < max_list:
            ans.append(news[idx]['article']+":"+news[idx]['detailurl'])
            idx += 1
        return ans
    elif code == 308000:
        ans = [robot_name+"(С����):"+text,]
        news = req.get('list')
        idx = 0
        while idx < len(news) and idx < max_list:
            ans.append(news[idx]['name']+"\t:"+news[idx]['info']+"\t���\t:"+news[idx]['detailurl'])
            idx += 1
        return ans
    elif code == 40004:
        return robot_name+"(С����):���������ˣ���Ϣ��Ϣ����"
    else :
        return robot_name+"(С����):�����˲�����״�Ĵ���"


def init_info(user_name,is_group = False):
    '''
    ����ǵ�һ�����������ˣ�����һ��С����
    '''

    if user_name not in known_names:
        if is_group == False and itchat.search_friends(userName=user_name)['NickName'] == self_name:
            itchat.send(robot_name+"(С����):���� "+self_name+" ��ר������С���� "+robot_name+" ���������ڲ����ߣ���������Ϊ���ṩ����",'filehelper')
        else:
            itchat.send(robot_name+"(С����):���� "+self_name+" ��ר������С���� "+robot_name+" ���������ڲ����ߣ���������Ϊ���ṩ����!",user_name)
            if is_group:
                itchat.send('��λ����@�ң������ҶԻ�Ŷ�����ҿ��Բ�ѯ���������š���',user_name)
        known_names.append(user_name)

########################################################################
########## retrieve ####################################################
########################################################################

'''
���ڼ�س�����Ϣ
'''

records = {}

def save_msg(user_name,msg):
    '''
    �������е��ı�����
    '''
    if user_name not in records:
        records[user_name] = [msg,]
    else:
        records[user_name].append(msg)

def retr_msg(user_name):
    '''
    ���ҳ��ص�����
    '''
    try:
        req = records[user_name].pop()
        return itchat.search_friends(userName=user_name)['NickName'] + '��������Ϣ:\t'+req['Content']
    except:
        pass

########################################################################
########## news ########################################################
########################################################################

def new_day():
    ans = []
    data = {'key': apikey,
        'info': self_local+'����',
        'userid': 'root'
    }

    req = requests.post(api_url, data=data).json()
    text = re.sub('^��',call_name,req.get('text'))
    ans.append(robot_name+"(С����):���������:"+text)

    data = {'key': apikey,
        'info': '����',
        'userid': 'root'
    }
    req = requests.post(api_url, data=data).json()
    news = req.get('list')
    idx = 0
    while idx < len(news) and idx < max_list:
        ans.append(news[idx]['article']+":"+news[idx]['detailurl'])
        idx += 1
    return ans

def sent_hello():
    infos = new_day()
    for chatroom in ask_list:
        for info in infos:
            itchat.send(info,itchat.search_chatrooms(name=chatroom)[0]['UserName'])


########################################################################
########## wechat register #############################################
########################################################################

'''
ע��΢����Ϣ������Ӧ��
'''

@itchat.msg_register(['Note'])
def auto_retreive(msg):
    if re.search("\[.*������һ����Ϣ\]", msg['Content']) and retrieve_on:
        reqs = retr_msg(msg['FromUserName'])
        itchat.send(reqs,'filehelper')

@itchat.msg_register(['Text', 'Map', 'Card', 'Sharing'])
def Tuling_robot(msg):
    if itchat.search_friends(userName=msg['FromUserName'])['NickName'] == self_name:
        if self_command(msg['Content']) :
            return 

    if retrieve_on:
        save_msg(msg['FromUserName'],msg)

    if robot_on:
        init_info(msg['FromUserName'])
        loc = ''
        if msg['Type'] == 'Map':
            try:
                loc = re.search('poiname=\"(.*)\"',msg['OriContent']).group(1)
                msg['Content'] = '������'
            except:
                loc = ''
        respones = get_response(msg['Content'], msg['FromUserName'],loc)
        
        if itchat.search_friends(userName=msg['FromUserName'])['NickName'] == self_name:
            for info in respones:
                itchat.send(info, toUserName='filehelper')
        else:
            for info in respones:
                itchat.send(info, msg['FromUserName'])

@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):
    filename = './tmp/'+msg['FileName']
    msg["Text"](filename)
    itchat.send(itchat.search_friends(userName=msg['FromUserName'])['NickName']+" ������һ��"+ msg['Type'],'filehelper')
    if msg['Type'] == 'Picture':
        itchat.send("@img@"+filename,'filehelper')
    elif msg['Type'] == 'Video':
        itchat.send("@vid@"+filename,'filehelper')
    else:
        itchat.send("@fil@"+filename,'filehelper')
        
    if robot_on:
        init_info(msg['FromUserName'])
        if itchat.search_friends(userName=msg['FromUserName'])['NickName'] == self_name:
            itchat.send(robot_name+"(С����):�����Ѿ��յ�������ļ���", 'filehelper')
        else:
            itchat.send(robot_name+"(С����):�����Ѿ��յ�������ļ���", msg['FromUserName'])

@itchat.msg_register(['Text', 'Map', 'Card', 'Sharing'], isGroupChat=True)
def group_reply(msg):
    if msg['isAt'] and group_on and robot_on:
        init_info(msg['FromUserName'],is_group = True)
        loc = ''
        if msg['Type'] == 'Map':
            try:
                loc = re.search('poiname=\"(.*)\"',msg['OriContent']).group(1)
                msg['Content'] = '�鿴����'
            except:
                loc = ''
        respones = get_response(msg['Content'], msg['FromUserName'],loc)

        itchat.send("@%s"%msg['ActualNickName'],msg['FromUserName'])

        for info in respones:
            itchat.send(info, msg['FromUserName'])

@itchat.msg_register(['Text', 'Map', 'Card', 'Sharing'],isMpChat =True)
def mp_robot(msg):
    if robot_on and group_on:
        init_info(msg['FromUserName'],True)
        loc = ''
        if msg['Type'] == 'Map':
            try:
                loc = re.search('poiname=\"(.*)\"',msg['OriContent']).group(1)
                msg['Content'] = '������'
            except:
                loc = ''
        respones = get_response(msg['Content'], msg['FromUserName'],loc)
        for info in respones:
            itchat.send(info, msg['FromUserName'])


########################################################################
########## itchat run ##################################################
########################################################################

if __name__ == '__main__':
    timer = threading.Timer( 1 , events)
    timer.start()
    # itchat.auto_login(hotReload=True,enableCmdQR=2)
    itchat.auto_login()
    itchat.run()
