#file  -- var.py --

import os
from html.parser import HTMLParser
from helpers import getTrophyCount

LOCKED, UNLOCKED = 0x0, 0x1          # Values for locked and unlocked status of trophy
SYNCED, NOTSYNCED = 0x20, 0x00       # Values for if a trophy was synced online or not
PL, GO, SI, BR = 0x1, 0x2, 0x3, 0x4  # Values for trophy types (Platinum, Gold, Silver, Bronze)
NUMOFTROPHY = 0xFF                   # Number of trophies, found in header of trptitle.dat
GROUPSIZE = 0x70                     # Size of a trophy group block
TRPBLOCK1 = 0x70                     # Size of TRPTITLE trophy data block1
TRPBLOCK2 = 0x60                     # Size of TRPTITLE trophy data block2
TRANBLOCK = 0xB0                     # Size of TRPTRANS trophy block
TROPHYID = 0x13                      # 0 for platinum
TROPHYSTATE = 0x17                   # 0 for lock, 1 for unlock
TROPHYSSYNC = 0x1A                   # 0x00 for unsynced and 0x20 for synced
TROPHYDATE1 = slice(0x20, 0x28)      # Date trophy was unlocked
TROPHYDATE2 = slice(0x28, 0x30)      # Date trophy was synced to PSN
EMPTYDATE = bytes(8)                 # Empty date value
PATH = 'files'                       # Default folder for support files
TROP = os.path.join(PATH, 'TROP.SFM')
TITLE = os.path.join(PATH, 'TRPTITLE.DAT')
TRANS = os.path.join(PATH, 'TRPTRANS.DAT')

def init_globals():
    global processedCount, date_str, timestamp, trophy_type, maxTrophies
    processedCount = 0                   # Global variable to store number of trophies altered
    date_str = ''                        # Global variable to store date string
    timestamp = bytearray(8)             # Global variable to store timestamp
    trophy_type = 0                      # Global variable to store trophy type
    maxTrophies = getTrophyCount()       # Global variable to store number of trophies

# Creates variable to store trophy data from TROP.SFM
def init_trophyData():
    global trophyData
    trophyData = {'id': [], 'type': [], 'name': [], 'desc': []}

# Treats TROP.SFM like HTML and parses the tags, attributes and data
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.nameTag = False
        self.detailTag = False

    #HTML Parser Methods
    def handle_starttag(self, tag, attrs):
        if tag not in ('trophy', 'name', 'detail'):
            return
        # If trophy tag is found, gather ID and Type
        if tag == 'trophy':
            for name, value in attrs:
                if name == 'id':
                    trophyData['id'].append(int(value))
                if name == 'ttype':
                    trophyData['type'].append(value)
        # If name tag is found, set variable true so handle_data will gather name
        if tag == 'name':
            self.nameTag = True
        # If detail tag is found, set variable true so handle_data will gather detail
        if tag == 'detail':
            self.detailTag = True

    def handle_data(self, data):
        # If name variable is true, gather name for this trophy
        if self.nameTag == True:
            trophyData['name'].append(data)
            self.nameTag = False
        # If detail variable is true, gather detail for this trophy
        if self.detailTag == True:
            trophyData['desc'].append(data)
            self.detailTag = False




    
