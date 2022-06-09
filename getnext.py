#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: http://www.oidview.com/mibs/0/SNMPv2-MIB.html


from typing import Iterator
import sqlite3db 
from databaseClass import Interface
from pysnmp.hlapi import nextCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity
interfaces = ['1.3.6.1.2.1.2.2.1.10' , '1.3.6.1.2.1.2.2.1.16' , '1.3.6.1.2.1.2.2.1.5']
inoctets = []
outoctets = []
speeds = []
for hrProcessorLoad in interfaces :
    def get_iterator(hrProcessorLoad, host: str, port: int = 161, community: str = '') -> Iterator:
        return nextCmd(
            SnmpEngine(),
            CommunityData(community, mpModel=1),
            UdpTransportTarget((host, port)),
            ContextData(),
            ObjectType(ObjectIdentity(hrProcessorLoad)),
            lexicographicMode=False,
        )


    iterator = get_iterator(hrProcessorLoad, '192.168.0.88', 161, 'private')
    items = list(iterator)
    # print(items)
    # print(f"number of interfaces values: {len(items)}\n")
    print(30*"#")
    for i, (error_indication, error_status, error_index, var_binds) in enumerate(items, 1):
        if error_indication:
            print(f'Error indication: {error_indication}')

        elif error_status:
            at = '?'
            if error_index:
                at = var_binds[int(error_index) - 1][0]
            print(f'Error status {error_status.prettyPrint()!r} at {at}')

        else:
            for var, value in var_binds:
                # print(f'{var} = {value}')
                # print(f'{var.getOid()} = {value}')
                val = value.prettyPrint()
                vari = var.prettyPrint()
                if str(var.getOid())[-3:-2] == "0" :
                    print(f"Oid: {vari}, ifinoctets: {val}")
                    inoctets.append(val)
                    # sqlite3db.insert_ifInOctets(val)          
                elif str(var.getOid())[-3:-2] == "6" :
                    print(f"Oid: {vari}, ifoutoctets: {val}")  
                    outoctets.append(val)            
                    # sqlite3db.insert_ifOutOctets(val)
                elif str(var.getOid())[-3:-2] == "5" :
                    print(f"Oid: {vari}, ifspeed: {val}")                    
                    speeds.append(val)
                # print(f'{var.prettyPrint()} = {value.prettyPrint()}')
                # sqlite3db.insert_ifInOctets(value.prettyPrint())
                # print()
# print(inoctets, outoctets, speeds)

lo = []
eth = []
wlan = []
i = 0
for inoctet, outoctet , speed in zip(inoctets, outoctets, speeds):
    if i == 0 :
        lo.append(int(inoctet))
        lo.append(int(outoctet))
        lo.append(int(speed))
    elif i == 1 :
        eth.append(int(inoctet))
        eth.append(int(outoctet))
        eth.append(int(speed))
    elif i == 2 :
        wlan.append(int(inoctet))
        wlan.append(int(outoctet))
        wlan.append(int(speed))
    i = i + 1 
        

sqlite3db.insertDataForLo(lo[0], lo[1], lo[2])
sqlite3db.insertDataForEth(eth[0], eth[1], eth[2])
sqlite3db.insertDataForWlan(wlan[0], wlan[1], wlan[2])