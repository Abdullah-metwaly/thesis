
from pysnmp.hlapi import bulkCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity
interfaces = ['1.3.6.1.2.1.2.2.1.2' , '1.3.6.1.2.1.2.2.1.10' , '1.3.6.1.2.1.2.2.1.16']
for oid in interfaces :    
    for errorIndication, errorStatus, \
        errorIndex, varBinds in bulkCmd(
            SnmpEngine(),
            CommunityData('private'),
            UdpTransportTarget(('192.168.0.88', 161)),
            ContextData(),
            0, 50,  # GETBULK specific: request up to 50 OIDs in a single response
            ObjectType(ObjectIdentity(oid)),
            lookupMib=False, lexicographicMode=False):

        if errorIndication:
            print(errorIndication)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
            break
        else:
             for var, value in varBinds:
                print(f'{var.prettyPrint()} = {value.prettyPrint()}')
