import netsnmp
#from setroubleshoot.errcode import err

# from __main__ import port


class SnmpClass(object):
    #
    def __init__(self, version, destHost, community):
        try:
            self.session = netsnmp.Session(Version=version, DestHost=destHost, Community=community)
        except:
            if self.session.ErrorStr == '' or self.session.ErrorStr == 'Timeout':
                msg = "Error in SNMP handle"
            else:
                msg = "Unknown error in SNMP handle"
            raise Exception(msg)

    # query Switch MIB
    def query(self, oid):
        try:
            oid = netsnmp.Varbind(oid)
            oidList = netsnmp.VarList(oid)
            result = self.session.walk(oidList)
        except Exception, err:
            print err
            result = None
        return result

    # query Standard MIB
    def queryMIB(self, oid):
        try:
            pass
        except Exception, err:
            print err
            result = None
        return result

    #
    def update(self):
        try:
            # pass
            port = '4'
            index = '13'

            oid = netsnmp.Varbind('.1.3.6.1.4.1', '.2011.5.25.157.1.1.1.1.15.9', '2', 'INTEGER')
            # print netsnmp.snmpset(oid,Version=1,DestHost='10.15.9.253',Community='private@it')
            print netsnmp.snmpget('.1.3.6.1.4.1.2011.5.25.157.1.1.1.1.15.5', Version=1, DestHost='10.15.9.253',
                                  Community='private@it')
            print netsnmp.snmpgetnext('.1.3.6.1.4.1.2011.5.25.157.1.1.1.1.15.5', Version=1, DestHost='10.15.9.253',
                                      Community='private@it')
            print netsnmp.snmpwalk('.1.3.6.1.4.1.2011.5.25.157.1.1.1.1.15', Version=1, DestHost='10.15.9.253',
                                   Community='private@it')
        except Exception, err:
            print err


def getDevice():
    fileDevice = open("Device_Info.txt")
    dictDevice = {}
    try:
        for line in fileDevice.readlines():
            if line.isspace():
                continue
            elif line.startswith('#'):
                continue
            else:
                key = line.partition('#')[0].strip().partition('=')[0].strip()
                value = line.partition('#')[0].strip().partition('=')[2].strip()
                dictDevice[key] = value

        '''
        while True:
            lineDevice = ''.join(fileDevice.readline()).strip('\n')
            if not lineDevice:
                break
            if  lineDevice.startswith('#'):
                continue
            listDevice = lineDevice.split(":")
            dictDevice[listDevice[0]] = listDevice[1]
        '''
    except Exception, err:
        print err
    finally:
        fileDevice.close()
        return dictDevice


def getMIB():
    fileMIB = open("Huawei_S5700_MIB.txt")
    dictMIB = {}
    try:
        for line in fileMIB.readlines():
            if line.isspace():
                continue
            elif line.startswith('#'):
                continue
            else:
                key = line.partition('#')[0].strip().partition('=')[0].strip()
                value = line.partition('#')[0].strip().partition('=')[2].strip()
                dictMIB[key] = value

        '''
        while True:
            lineMIB = ''.join(fileMIB.readline()).strip('\n')
            if not lineMIB:
                break
            if  lineMIB.startswith('#'):
                continue
            listMIB = lineMIB.split("=")
            dictMIB[listMIB[0]] = listMIB[1]
        '''
    except Exception, err:
        print err
    finally:
        fileMIB.close()
        return dictMIB


def main():
    # read paramter files
    dictDevice = getDevice()
    dictMIB = getMIB()

    nbbl_Test = SnmpClass(destHost=dictDevice['NBBL_Test'],
                          version=int(dictDevice['Version']),
                          community=dictDevice['Community']
                          )

    print nbbl_Test.query(dictMIB['hwEthernetDeplex'])[0]
    # print nbbl_Test.query(dictMIB['hwEthernetDeplex'])[1]


if __name__ == '__main__':
    main()