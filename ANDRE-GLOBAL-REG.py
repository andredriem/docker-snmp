#
# PySNMP MIB module ANDRE-GLOBAL-REG (http://snmplabs.com/pysmi)
# ASN.1 source file:///Users/andredriemeyer/Documents/docker-snmp/docker.mib
# Produced by pysmi-0.3.2 at Thu Nov 15 19:16:50 2018
# On host MacBook-Air-de-Andre.local platform Darwin version 17.7.0 by user andredriemeyer
# Using Python version 2.7.15 (default, Aug 29 2018, 18:52:32) 
#

print "hello there, general kenoby"
Integer, ObjectIdentifier, OctetString = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ConstraintsUnion, SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint, ValueRangeConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsUnion", "SingleValueConstraint", "ConstraintsIntersection", "ValueSizeConstraint", "ValueRangeConstraint")
NotificationGroup, ModuleCompliance, ObjectGroup = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance", "ObjectGroup")
Integer32, MibScalar, MibTable, MibTableRow, MibTableColumn, NotificationType, MibIdentifier, IpAddress, TimeTicks, Counter64, Unsigned32, enterprises, iso, Gauge32, ModuleIdentity, ObjectIdentity, Bits, Counter32 = mibBuilder.importSymbols("SNMPv2-SMI", "Integer32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "NotificationType", "MibIdentifier", "IpAddress", "TimeTicks", "Counter64", "Unsigned32", "enterprises", "iso", "Gauge32", "ModuleIdentity", "ObjectIdentity", "Bits", "Counter32")
DisplayString, TextualConvention = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
dockerRoot = ObjectIdentity((1, 3, 6, 1, 4, 1, 12345))
if mibBuilder.loadTexts: dockerRoot.setStatus('current')
dockerDaemon = MibIdentifier((1, 3, 6, 1, 4, 1, 12345, 1))
dockerDaemonUptime = MibScalar((1, 3, 6, 1, 4, 1, 12345, 1, 1), TimeTicks()).setMaxAccess("readonly")
if mibBuilder.loadTexts: dockerDaemonUptime.setStatus('current')
dockerDaemonRestart = MibScalar((1, 3, 6, 1, 4, 1, 12345, 1, 2), Integer32().subtype(subtypeSpec=SingleValueConstraint(0, 1)).clone(namedValues=NamedValues(("notRestarting", 0), ("restaring", 1)))).setMaxAccess("readwrite")
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
containeListUptime = MibTableColumn((1, 3, 6, 1, 4, 1, 12345, 2, 1, 1, 2), TimeTicks()).setMaxAccess("readonly")
if mibBuilder.loadTexts: containeListUptime.setStatus('current')
containeListName = MibTableColumn((1, 3, 6, 1, 4, 1, 12345, 2, 1, 1, 3), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: containeListName.setStatus('current')
containeListStatus = MibTableColumn((1, 3, 6, 1, 4, 1, 12345, 2, 1, 1, 4), Integer32().subtype(subtypeSpec=SingleValueConstraint(1, 2, 3)).clone(namedValues=NamedValues(("up", 1), ("restarting", 2), ("down", 3)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: containeListStatus.setStatus('current')
mibBuilder.exportSymbols("ANDRE-GLOBAL-REG", dockerContainers=dockerContainers, containeListName=containeListName, dockerRoot=dockerRoot, containeListEntry=containeListEntry, containeListUptime=containeListUptime, dockerDaemonUptime=dockerDaemonUptime, dockerDaemonRestart=dockerDaemonRestart, containeListStatus=containeListStatus, dockerDaemon=dockerDaemon, dockerDaemonMandatoryImplementations=dockerDaemonMandatoryImplementations, containeListHashIdentifier=containeListHashIdentifier, containeListTable=containeListTable)
