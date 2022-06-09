# from cgitb import lookup
from ast import And
from itertools import count
import sys 
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets,  uic
# from importlib_metadata import Lookup
# from graphql_relay import cursor_for_object_in_connection
# from numpy import var
from PyQt5.QtWidgets import  QTableWidget, QDialog ,QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem ,QDesktopWidget, QPushButton
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget,\
                         ContextData, ObjectType, ObjectIdentity, getCmd, nextCmd, bulkCmd
from sqlalchemy import null
# from sqlalchemy import true



class Ui(QtWidgets.QMainWindow):
    ip = "" 
    port = ""  
    auth = "" 
    req = "" 
    Oid = "" 
    nextiterator = null
    bulkIterator = null
    tableData = null
    emptyTable = True
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('snmp-gui.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.tableData = []
        self.sendButton.clicked.connect(self.chooseRequest)
        self.pushButton.clicked.connect(self.emptyTable)
        
    # for updating the inserted values from the gui
    def updateValues(self):
        # global ip , port, auth, req, Oid
        if self.checkValues() :
            self.ip = self.ipaddr.currentText() 
            self.port = self.portnumber.currentText()
            self.auth = self.communityString.text()
            self.req = self.snmpreq.currentText()
            self.Oid = self.objectId.text()
            self.constructNextIterator()
            self.constructBulkIterator()

        # print(f"Your ip: {self.ip} and the port: {self.port} and the password: {self.auth} the request: {self.req}, Your object id {self.Oid}")
    # for checking on the changed occured on values 
    def checkValues(self) :
        return self.ip != self.ipaddr.currentText() or \
            self.port != self.portnumber.currentText() \
                or self.auth != self.communityString.text()\
                    or self.req != self.snmpreq.currentText()\
                        or self.Oid != self.objectId.text()  \
                            or self.emptyTable == True

    def chooseRequest(self):
        self.updateValues()
        if self.req == "Get" :
            self.getRequestFunc()
        elif self.req == "GetNext" :
            self.getNextRequestFunc()
        elif self.req == "GetBulk" :
            self.getBulkRequestFunc()
            
    def emptyTable(self):
        self.updateValues()
        self.tableData.clear()
        self.loadData()
        self.emptyTable = True


    def loadData(self):
        self.emptyTable = False
        row = 0
        self.Results.setRowCount(len(self.tableData))
        for val in self.tableData :
            self.Results.setItem(row, 0, QtWidgets.QTableWidgetItem(val["name"]))
            self.Results.setItem(row, 1, QtWidgets.QTableWidgetItem(val["value"]))
            row=row+1

        
    def constructNextIterator(self):
        self.nextiterator = nextCmd(
                SnmpEngine(),
                CommunityData(self.auth, mpModel=1),
                UdpTransportTarget((self.ip, self.port)),
                ContextData(),
                ObjectType(ObjectIdentity('RFC1213-MIB')),
                lookupMib=False, lexicographicMode=False
            )
        currentOID = ""
        while(currentOID != self.Oid):
            errorIndication, errorStatus, errorIndex, varBinds = next(self.nextiterator)
            currentOID = str(varBinds[0][0])
            
    def constructBulkIterator(self):
        self.bulkIterator = bulkCmd(
                SnmpEngine(),
                CommunityData(self.auth, mpModel=1),
                UdpTransportTarget((self.ip, self.port)),
                ContextData(),
                0, 50,
                ObjectType(ObjectIdentity('RFC1213-MIB')),
                lookupMib=False, lexicographicMode=False
            )
        currentOID = ""
        while(currentOID != self.Oid):
            errorIndication, errorStatus, errorIndex, varBinds = next(self.bulkIterator)
            currentOID = str(varBinds[0][0])
            
    # the get request
    cmdGen = cmdgen.CommandGenerator()
    def getRequestFunc(self):
        self.updateValues()
        iterator = getCmd(
        SnmpEngine(),
        CommunityData(self.auth, mpModel=1),
        UdpTransportTarget((self.ip, self.port)),
        ContextData(),
        ObjectType(ObjectIdentity(self.Oid))
        )
        
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)   
        self.constructErrorFunc(errorIndication, errorStatus, errorIndex, varBinds)
        for oid, val in varBinds:
            newRow = {"name" : oid.prettyPrint() , "value" : val.prettyPrint()}
            self.tableData.append(newRow)
            self.loadData()
    
    # get next request for the snmp
    cmdGen = cmdgen.CommandGenerator()
    def getNextRequestFunc(self):        
        self.updateValues()
        errorIndication, errorStatus, errorIndex, varBinds = next(self.nextiterator)
        print(errorIndication)
        self.constructErrorFunc(errorIndication, errorStatus, errorIndex, varBinds)
        newRow = {"name" : varBinds[0][0].prettyPrint() , "value" : varBinds[0][1].prettyPrint()}
        self.tableData.append(newRow)
        self.loadData() 
        # items = list(self.nextiterator)
        # print(f"Number CPU cores: {len(items)}\n")          

    # get bulk request for the snmp 
    cmdGen = cmdgen.CommandGenerator()
    def getBulkRequestFunc(self) :
        self.updateValues()
        max_rep = 12
        count = 0
        while(count < max_rep):
            try:
                errorIndication, errorStatus, errorIndex, varBinds = next(self.bulkIterator)
                self.constructErrorFunc(errorIndication, errorStatus, errorIndex, varBinds)
                newRow = {"name" : varBinds[0][0].prettyPrint() , "value" : varBinds[0][1].prettyPrint()}
                self.tableData.append(newRow)
            except StopIteration:
                break

            count += 1
        self.loadData()   

        
    # checking returned errors
    def constructErrorFunc(self, errorIndication, errorStatus, errorIndex, varBinds):
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('{} at {}'.format(errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        

def main():        
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()



