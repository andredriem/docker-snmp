from pysnmp.entity import engine, config
from pysnmp import debug
from pysnmp.entity.rfc3413 import cmdrsp, context, ntforg
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.smi import builder
from pysnmp.proto.api import v2c
from subprocess import check_output
import datetime

import threading
import collections
import time
from random import randint
from json import loads
from pprint import pprint

#can be useful
#debug.setLogger(debug.Debug('all'))

MibObject = collections.namedtuple('MibObject', ['mibName',
                                   'objectType', 'valueFunc'])
                                   
docker_list = []
                                   
def getDockerProcesses():
    out = check_output(['docker', 'ps'])
    lines = [line.split(r" ") for line in out.split('\n')]
    lines.pop(0)
    print lines
    return lines

class Mib(object):
    """Stores the data we want to serve. 
    """

    def __init__(self):
        self._lock = threading.RLock()
        self._test_count = 0

    def dockerDaemonUptime(self):
        "Calls system monitor to figure out for how much time Docker process is running"
        with self._lock:
            out = check_output(['ps', 'aux'])
            res = [line for line in  out.split('\n') if 'MacOS/Docker' in line][0].split()[1]
            if res == []:
                return 0
            out = check_output(['ps', '-o', 'etime=','-p',res])
            try:
                t=datetime.datetime.strptime(out,'%H:%M:%S\n')
            except:
                return 0
            return (((t.hour * 60) + t.minute) * 60 + t.second) * 100
            
    def dockerDaemonRestart(self):
        return randint(0,1)
        

def createVariable(SuperClass, getValue, *args):
    """This is going to create a instance variable that we can export. 
    getValue is a function to call to retreive the value of the scalar
    """
    class Var(SuperClass):
        def readGet(self, name, *args):
            return name, self.syntax.clone(getValue())
    return Var(*args)


class SNMPAgent(object):
    """Implements an Agent that serves the custom MIB and
    can send a trap.
    """

    def __init__(self, mibObjects):
        """
        mibObjects - a list of MibObject tuples that this agent
        will serve
        """

        #each SNMP-based application has an engine
        self._snmpEngine = engine.SnmpEngine()

        #open a UDP socket to listen for snmp requests
        config.addSocketTransport(self._snmpEngine, udp.domainName,
                                  udp.UdpTransport().openServerMode(('', 161)))

        #add a v2 user with the community string public
        config.addV1System(self._snmpEngine, "agent", "public")
        #let anyone accessing 'public' read anything in the subtree below,
        #which is the enterprises subtree that we defined our MIB to be in
        config.addVacmUser(self._snmpEngine, 2, "agent", "noAuthNoPriv",
                           readSubTree=(1,3,6,1,4,1))

        #each app has one or more contexts
        self._snmpContext = context.SnmpContext(self._snmpEngine)

        #the builder is used to load mibs. tell it to look in the
        #current directory for our new MIB. We'll also use it to
        #export our symbols later
        mibBuilder = self._snmpContext.getMibInstrum().getMibBuilder()
        mibSources = mibBuilder.getMibSources() + (builder.DirMibSource('.'),)
        mibBuilder.setMibSources(*mibSources)
        
        Integer, ObjectIdentifier, OctetString = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
        MibScalar, MibScalarInstance = mibBuilder.importSymbols(
            'SNMPv2-SMI', 'MibScalar', 'MibScalarInstance'
        )
        
        class DockerDaemonUpTimeMibScalarInstance(MibScalarInstance):
            def getValue(self, name, idx):
                out = check_output(['ps', 'aux'])
                res = [line for line in  out.split('\n') if 'MacOS/Docker' in line][0].split()[1]
                if res == []:
                    result = 0
                    return self.getSyntax().clone(result)
                    
                out = check_output(['ps', '-o', 'etime=','-p',res])
                try:
                    t=datetime.datetime.strptime(out,'%H:%M:%S\n')
                except:
                    result = 0
                    return self.getSyntax().clone(result)
                result =  (((t.hour * 60) + t.minute) * 60 + t.second) * 100
                return self.getSyntax().clone(result)
                
                dockerDaemonRestart
                
        class DockerDaemonRestartMibScalarInstance(MibScalarInstance):
            def getValue(self, name, idx):
                return self.getSyntax().clone(randint(0,1))
        
        NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
        ConstraintsUnion, SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint, ValueRangeConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsUnion", "SingleValueConstraint", "ConstraintsIntersection", "ValueSizeConstraint", "ValueRangeConstraint")
        NotificationGroup, ModuleCompliance, ObjectGroup = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance", "ObjectGroup")
        Integer32, MibScalar, MibTable, MibTableRow, MibTableColumn, NotificationType, MibIdentifier, IpAddress, TimeTicks, Counter64, Unsigned32, enterprises, iso, Gauge32, ModuleIdentity, ObjectIdentity, Bits, Counter32 = mibBuilder.importSymbols("SNMPv2-SMI", "Integer32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "NotificationType", "MibIdentifier", "IpAddress", "TimeTicks", "Counter64", "Unsigned32", "enterprises", "iso", "Gauge32", "ModuleIdentity", "ObjectIdentity", "Bits", "Counter32")
        DisplayString, TextualConvention = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
        dockerRoot = ObjectIdentity((1, 3, 6, 1, 4, 1, 12345))
        if mibBuilder.loadTexts: dockerRoot.setStatus('current')
        dockerDaemon = MibIdentifier((1, 3, 6, 1, 4, 1, 12345, 1))
        
        # Done
        dockerDaemonUptime = MibScalar((1, 3, 6, 1, 4, 1, 12345, 1, 1), TimeTicks()).setMaxAccess("readonly")
        mibBuilder.exportSymbols("ANDRE-GLOBAL-REG",dockerDaemonUptime, DockerDaemonUpTimeMibScalarInstance((1, 3, 6, 1, 4, 1, 12345, 1, 1),(0,),TimeTicks()))
        
        
        
        # On Hold
        dockerDaemonRestart = MibScalar((1, 3, 6, 1, 4, 1, 12345, 1, 2), Integer32().subtype(subtypeSpec=SingleValueConstraint(0, 1)).clone(namedValues=NamedValues(("notRestarting", 0), ("restaring", 1)))).setMaxAccess("readwrite")
        mibBuilder.exportSymbols("ANDRE-GLOBAL-REG",dockerDaemonRestart, DockerDaemonRestartMibScalarInstance((1, 3, 6, 1, 4, 1, 12345, 1, 2),(0,),  Integer32().subtype(subtypeSpec=SingleValueConstraint(0, 1)).clone(namedValues=NamedValues(("notRestarting", 0), ("restaring", 1)))))
        
        
        if mibBuilder.loadTexts: dockerDaemonRestart.setStatus('current')
        dockerDaemonMandatoryImplementations = ObjectGroup((1, 3, 6, 1, 4, 1, 12345, 1, 3)).setObjects(("ANDRE-GLOBAL-REG", "dockerDaemonUptime"), ("ANDRE-GLOBAL-REG", "dockerDaemonRestart"))
        if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
            dockerDaemonMandatoryImplementations = dockerDaemonMandatoryImplementations.setStatus('current')
        dockerContainers = MibIdentifier((1, 3, 6, 1, 4, 1, 12345, 2))
        containeListTable = MibTable((1, 3, 6, 1, 4, 1, 12345, 2, 1), )
        if mibBuilder.loadTexts: containeListTable.setStatus('current')
        containeListEntry = MibTableRow((1, 3, 6, 1, 4, 1, 12345, 2, 1, 1), ).setIndexNames((0, "ANDRE-GLOBAL-REG", "containeListHashIdentifier"), (0, "ANDRE-GLOBAL-REG", "containeListUptime"), (0, "ANDRE-GLOBAL-REG", "containeListName"), (0, "ANDRE-GLOBAL-REG", "containeListStatus"))
        if mibBuilder.loadTexts: containeListEntry.setStatus('current')
        containeListHashIdentifier = MibTableColumn((1, 3, 6, 1, 4, 1, 12345, 2, 1, 1, 1), OctetString()).setMaxAccess("readonly")
        if mibBuilder.loadTexts: containeListHashIdentifier.setStatus('current')
        containeListImageID = MibTableColumn((1, 3, 6, 1, 4, 1, 12345, 2, 1, 1, 2), OctetString()).setMaxAccess("readonly")
        if mibBuilder.loadTexts: containeListUptime.setStatus('current')
        containeListName = MibTableColumn((1, 3, 6, 1, 4, 1, 12345, 2, 1, 1, 3), OctetString()).setMaxAccess("readonly")
        if mibBuilder.loadTexts: containeListName.setStatus('current')
        containeListStatus = MibTableColumn((1, 3, 6, 1, 4, 1, 12345, 2, 1, 1, 4), OctetString()).setMaxAccess("readonly")
        if mibBuilder.loadTexts: containeListStatus.setStatus('current')
        mibBuilder.exportSymbols("ANDRE-GLOBAL-REG", dockerContainers=dockerContainers, containeListName=containeListName, dockerRoot=dockerRoot, containeListEntry=containeListEntry, containeListImageID=containeListImageID, dockerDaemonUptime=dockerDaemonUptime, dockerDaemonRestart=dockerDaemonRestart, containeListStatus=containeListStatus, dockerDaemon=dockerDaemon, dockerDaemonMandatoryImplementations=dockerDaemonMandatoryImplementations, containeListHashIdentifier=containeListHashIdentifier, containeListTable=containeListTable)
        
        container_info = getDockerProcesses()
        docker_informations = loads(check_output(['curl','--unix-socket','/var/run/docker.sock', 'http://localhost/containers/json']))
        print docker_informations[0]
        class ContaineListHashIdentifierStateInstance(MibScalarInstance):
          def readGet(self, name, val, *args):
            try:
                return self.name, self.syntax.clone(docker_informations[name[-1] - 1]["Id"])
            except:
              MibScalarInstance.readGet(self, name, val, *args)
              
        class ContaineListNameStateInstance(MibScalarInstance):
          def readGet(self, name, val, *args):
            return self.name, self.syntax.clone(docker_informations[name[-1] - 1]["Image"])
            
        class ContaineListStatusStateInstance(MibScalarInstance):
          def readGet(self, name, val, *args):
            return self.name, self.syntax.clone(docker_informations[name[-1] - 1]["Status"])

        class ContaineListImageIDStateInstance(MibScalarInstance):
          def readGet(self, name, val, *args):
            return self.name, self.syntax.clone(docker_informations[name[-1] - 1]["ImageID"])
                      
        for i in range(len(docker_informations)):                
            mibBuilder.exportSymbols("ANDRE-GLOBAL-REG",
                ContaineListNameStateInstance(containeListName.getName(), (i+1,), containeListName.getSyntax()),
                ContaineListHashIdentifierStateInstance(containeListHashIdentifier.getName(), (i+1,), containeListHashIdentifier.getSyntax()),
                ContaineListStatusStateInstance(containeListStatus.getName(), (i+1,), containeListStatus.getSyntax()),
                ContaineListImageIDStateInstance(containeListImageID.getName(), (i+1,), containeListImageID.getSyntax()),
            )
        
        #Export Test Table
        

        #our variables will subclass this since we only have scalar types
        #can't load this type directly, need to import it
        MibScalarInstance, = mibBuilder.importSymbols('SNMPv2-SMI',
                                                      'MibScalarInstance')


        # tell pysnmp to respotd to get, getnext, and getbulk
        cmdrsp.GetCommandResponder(self._snmpEngine, self._snmpContext)
        cmdrsp.NextCommandResponder(self._snmpEngine, self._snmpContext)
        cmdrsp.BulkCommandResponder(self._snmpEngine, self._snmpContext)


    def setTrapReceiver(self, host, community):
        """Send traps to the host using community string community
        """
        config.addV1System(self._snmpEngine, 'nms-area', community)
        config.addVacmUser(self._snmpEngine, 2, 'nms-area', 'noAuthNoPriv',
                           notifySubTree=(1,3,6,1,4,1))
        config.addTargetParams(self._snmpEngine,
                               'nms-creds', 'nms-area', 'noAuthNoPriv', 1)
        config.addTargetAddr(self._snmpEngine, 'my-nms', udp.domainName,
                             (host, 162), 'nms-creds',
                             tagList='all-my-managers')
        #set last parameter to 'notification' to have it send
        #informs rather than unacknowledged traps
        config.addNotificationTarget(
            self._snmpEngine, 'test-notification', 'my-filter',
            'all-my-managers', 'trap')


    def sendTrap(self):
        print "Sending trap"
        ntfOrg = ntforg.NotificationOriginator(self._snmpContext)
        errorIndication = ntfOrg.sendNotification(
            self._snmpEngine,
            'test-notification',
            ('MY-MIB', 'testTrap'),
            ())


    def serve_forever(self):
        print "Starting agent"
        self._snmpEngine.transportDispatcher.jobStarted(1)
        try:
           self._snmpEngine.transportDispatcher.runDispatcher()
        except:
            self._snmpEngine.transportDispatcher.closeDispatcher()
            raise

class Worker(threading.Thread):
    """Just to demonstrate updating the MIB
    and sending traps
    """

    def __init__(self, agent, mib):
        threading.Thread.__init__(self)
        self._agent = agent
        self._mib = mib
        self.setDaemon(True)

    def run(self):
        while True:
            time.sleep(3)
            self._agent.sendTrap()

if __name__ == '__main__':
    mib = Mib()
    objects = [MibObject('ANDRE-GLOBAL-REG', 'dockerDaemonUptime', mib.dockerDaemonUptime),
               MibObject('ANDRE-GLOBAL-REG', 'dockerDaemonRestart', mib.dockerDaemonRestart),]
    agent = SNMPAgent(objects)
    agent.setTrapReceiver('192.168.1.14', 'traps')
    Worker(agent, mib).start()
    try:
        agent.serve_forever()
    except KeyboardInterrupt:
        print "Shutting down"