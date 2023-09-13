LoggingLevel = {
    "OVERRIDE": 0,
    "FATAL": 1,
    "ERROR": 2,
    "WARNING": 3,
    "INFO": 4,
    "LOG": 5,
    "DEBUG": 6,
    "TRACE": 7,
}

from sys import stdout

class Logging:
    def __init__(self):
        self.isEnabled = False
        self.CurrentLevel = LoggingLevel["FATAL"]
        self.LogLocation = None

        self.isEcho = False
        self.echoLocation = stdout

    def SetLevel(self, level):
        self.CurrentLevel = level
    
    def SetLocation(self, location):
        self.LogLocation = location
    
    def Enable(self):
        self.isEnabled = True
    
    def Disable(self):
        self.isEnabled = False
    
    def Print(self, level, message):
        if self.isEnabled and level <= self.CurrentLevel:
            if self.LogLocation is not None:
                with open(self.LogLocation, "a") as f:
                    f.write(message + "\n")
            if self.isEcho:
                print(message, file=self.echoLocation)
    
    def Override(self, message):
        self.Print(LoggingLevel["OVERRIDE"], message)

    def Fatal(self, message):
        self.Print(LoggingLevel["FATAL"], message)
    
    def Error(self, message):
        self.Print(LoggingLevel["ERROR"], message)
    
    def Warning(self, message):
        self.Print(LoggingLevel["WARNING"], message)

    def Info(self, message):
        self.Print(LoggingLevel["INFO"], message)
    
    def Log(self, message):
        self.Print(LoggingLevel["LOG"], message)
    
    def Debug(self, message):
        self.Print(LoggingLevel["DEBUG"], message)
    
    def Trace(self, message):
        self.Print(LoggingLevel["TRACE"], message)
    
    def Echo(self, echo):
        self.isEcho = echo