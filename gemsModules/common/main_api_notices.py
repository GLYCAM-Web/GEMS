#!/usr/bin/env python3
# ###############################################################
from typing import Dict, List
from pydantic import BaseModel, Field, PrivateAttr

from gemsModules.common.code_utils import GemsStrEnum

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class NoticeTypes(GemsStrEnum):
    note = 'Note'
    warning = 'Warning'
    error = 'Error'
#    exit = 'Exit' # can't use 'exit' as a variable name.
    fatal = 'Exit'


class Notice(BaseModel):
    """Description of a Notice."""
    Brief: str = Field(
            None,
            title='Brief',
            alias='brief',
            description='Brief title, status or name for this notice or notice type.'
            )
    Type : NoticeTypes = Field(
            None,
            title='Type',
            alias='type'
            )
    Code : str = Field(
            None,
            title='Code',
            alias='code',
            description='Numeric code associated with this notice, for users who like this sort of thing.'
            )
    Message : str = Field(
            None,
            title='Message',
            alias='message',
            description='A more detailed message for this notice.'
            )
    Scope : str = Field(
            None,
            title='Context of notice',
            alias='scope',
            description='The scope at which the error occured.'
            )
    Messenger : str = Field(
            None,
            title='Messaging Entity',
            description='The Entity that raised the notice, if known.'
            )
    AdditionalInfo : Dict[str,str] = Field(
            None,
            description='Key-value pairs that are specific to each entity, service, etc'
            )


def makeDefaultNoticesList() :
    from gemsModules.common.notice_data import NoticeData
    theNotices : List[Notice] = []
    tempNotice : Notice = Notice()   
    for noticedatum in NoticeData :
        tempNotice.Brief      =  noticedatum.Brief
        tempNotice.Type       =  noticedatum.Type
        tempNotice.Code       =  noticedatum.Code
        tempNotice.Scope      =  noticedatum.Scope
        tempNotice.Message    =  noticedatum.Message
        tempNotice.Messenger  =  noticedatum.Messenger
        theNotices.append(tempNotice.copy())
    return theNotices
  

class Notices(BaseModel):

    __root__ : List[Notice] = None
    _defaultNoticeTypes : List[Notice] = PrivateAttr(default_factory=makeDefaultNoticesList)


    def printDefaults(self, sendTo='logs', style='easyRead'):
        self.printNotices(sendTo=sendTo, style=style, whatToPrint='Defaults')


    def printNotices(self, sendTo='logs', style='easyRead', whatToPrint='Notices'):
        if whatToPrint == 'Notices':
            printString = "Printing the Notices: \n" + self.noticesString(style, whatToPrint=whatToPrint)
        elif whatToPrint == 'Defaults' :
            printString = "Printing the Default Notices: \n" + self.defaultNoticesString(style)
        else :
            log.error("Unknown printTarget (whatToPrint) in printNotices")
            return ""
        if sendTo == 'logs' :
            log.debug(printString)
        elif sendTo == 'stdout' :
            print(printString)
        else :
            log.error("The sendTo option given to Notices.printDefaults() is not known.  Cannot print.")


    def defaultNoticesString(self, style='easyRead'):
        return self.noticesString(style=style, whatToPrint='Defaults')


    def noticesString(self, style='easyRead', whatToPrint='Notices'):
        if whatToPrint == 'Notices':
            printTarget = self.__root__
        elif whatToPrint == 'Defaults' :
            printTarget = self._defaultNoticeTypes
        else :
            log.error("Unknown printTarget (whatToPrint) in noticesString")
            return ""
        if style == 'easyRead' :
            printString = ""
            for noticedatum in printTarget:
                printString = printString + noticedatum.json(indent=2) 
        elif style == 'minified' :
            printString = ""
            for noticedatum in printTarget:
                printString = printString + noticedatum.json() 
        elif style == 'terse' :
            import pprint 
            printString = pprint.pformat(printTarget)
        else: 
            log.error("Style type given to Notices.defaultNoticesString() is not known.  Cannot generate string.")
            printString = "'Unable to generate'"
        return printString


    def addDefaultNotice(self,
            Brief           : str  = 'UnknownError' ,  # Lookup keyword for the error
            Scope           : str  = None,             # Is this from entity? service? transaction?
            Messenger       : str  = None,             # Which entity sends this message?
            Type      : str  = None,             # Error, Warning, Info
            Code            : str  = None,             # Numeric code because those can be useful
            Message         : str  = None,             # Human-readable brief description
            AdditionalInfo  : Dict = None  # Free-form dictionary of data to return 
            ):
        log.info("addDefaultNotice() was called.\n")
      
        baseNotice = None

        for N in self._defaultNoticeTypes :
            if N.Brief == Brief :
                baseNotice = N
                break

        if baseNotice is None :
            errorMessage="Request to addDefaultNotice for unknown Brief -  " + Brief 
            log.error(errorMessage)
            for N in self._defaultNoticeTypes :
                if N.Brief == 'UnknownError' :
                    baseNotice = N
                    break
            if AdditionalInfo is None :
                AdditionalInfo = {}
            AdditionalInfo['commonServicerMessage']=errorMessage

        if Scope is None :
            Scope = baseNotice.Scope 
        if Type is None :
            Type = baseNotice.Type
        if Code is None :
            Code = baseNotice.Code
        if Messenger is None :
            Messenger = baseNotice.Messenger
        if Message is None :
            Message = baseNotice.Message

        self.addNotice(Brief=Brief, Scope=Scope, Messenger=Messenger, Type=Type, Code=Code, Message=Message, AdditionalInfo=AdditionalInfo)


    def addNotice(self,
            Brief           : str,    # Lookup keyword for the error
            Scope           : str,    # Is this from entity? service? transaction?
            Messenger       : str,    # Which entity sends this message?
            Type      : str,    # Error, Warning, Info
            Code            : str,    # Numeric code because those can be useful
            Message         : str,    # Human-readable brief description
            AdditionalInfo  : Dict = None  # Free-form dictionary of data to return 
            ):
        log.info("addNotice() was called.\n")
        
        # Build the notice 
        thisNotice = Notice()
        thisNotice.Brief=Brief
        thisNotice.Scope=Scope
        thisNotice.Type=Type
        thisNotice.Code=Code
        thisNotice.Message=Message
        thisNotice.Messenger=Messenger
        if AdditionalInfo is not None : 
            thisNotice.AdditionalInfo=AdditionalInfo
    
        if self.__root__ is None:
            self.__root__ : List[Notice] = []
        self.__root__.append(thisNotice)

    def addSimpleInfoNotice(self, message, brief="Info Message", scope="Unknown", messenger="Unknown", additionalInfo=None):
        self.addNotice(
            Brief=brief,
            Scope=scope,
            Messenger=messenger,
            Type='Info',
            Code='0',
            Message=message,
            AdditionalInfo=additionalInfo
        )
        
    def __iter__(self):
        return iter(self.__root__)
    
    def __next__(self):
        return next(self.__root__)
    
    def extend(self, other):
        self.__root__.extend(other.__root__)
    
    def append(self, notice: Notice):
        self.__root__.append(notice)


def generateSchema():
    from pydantic.schema import schema
    print(Notices.schema_json(indent=2))


def showDefaultNotices():
    tempNotices=Notices()
    ##  Examples of other ways to output the default notice types
    #tempNotices.printDefaults(style='easyRead')
    #tempNotices.printDefaults(style='minified')
    ## Print the default notice types to the screen
    tempNotices.printDefaults(style='terse', sendTo='stdout')


def testDefaultNoticeAddition():
    tempNotices=Notices()
    #tempNotices.addDefaultNotice(Brief='notKnownBrief')
    tempNotices.addDefaultNotice(Brief='GemsError')
    tempNotices.printNotices(style='terse',sendTo='stdout')


