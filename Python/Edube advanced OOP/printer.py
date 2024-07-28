class Scanner:
    def scan():
        print('scan() method from Scanner class')
class Printer:
    def print():
        print('print() method from Printer class')
class Fax:
    def send():
        print('send() method from Fax class')
    def print():
        print('print() method from Fax class')

class MFD_SPF(Scanner,Printer,Fax):
    def __init__(self):
        pass

class MFD_SFP(Scanner,Fax,Printer):
    def __init__(self):
        pass
    
MFD_SPF.scan()
MFD_SPF.print()
MFD_SPF.send()
MFD_SFP.scan()
MFD_SFP.print()
MFP_SFP.send()
