# import asyncio
# from pysnmp.hlapi.asyncio import *
# from pysnmp import debug


# @asyncio.coroutine
# def getone(snmpEngine, hostname):
#     errorIndication, errorStatus, errorIndex, varBinds = yield from getCmd(
#         snmpEngine,
#         CommunityData('public', mpModel=1),
#         UdpTransportTarget(hostname),
#         ContextData(),
#         ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
#     )

#     if errorIndication:
#         print(errorIndication)
#     elif errorStatus:
#         print('%s at %s' % (
#             errorStatus.prettyPrint(),
#             errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
#         )
#               )
#     else:
#         for varBind in varBinds:
#             print(' = '.join([x.prettyPrint() for x in varBind]))

# debug.setLogger(debug.Debug('io', 'msgproc'))

# snmpEngine = SnmpEngine()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(
#     asyncio.wait([getone(snmpEngine, ('127.0.0.1', 161)),
#                   getone(snmpEngine, ('127.0.0.1', 161)),
#                   getone(snmpEngine, ('127.0.0.1', 161))])
# )
from pysnmp.hlapi import *

g = getCmd(SnmpEngine(),
       CommunityData('public'),
       UdpTransportTarget(('www.google.com', 161)),
       ContextData(),
       ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))

print(next(g))