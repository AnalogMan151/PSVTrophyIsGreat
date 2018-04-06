#!/usr/bin/env python3
# Author: AnalogMan
# Thanks to: silicaandpina
# Modified Date: 2018-04-06
# Purpose: Locks or unlock PS Vita Trophies in decrypted TRPTITLE.DAT & TRPTRANS.DAT file
# Notes: Place decrypted TROP.SFM, TRPTITLE.DAT & TRPTRANS.DAT files in 'files' directory
# Edit main function and uncomment which function you'd like to do

import argparse
import var
import os
from helpers import encodeTimestamp
from datetime import datetime
from trntitle import unlockTitle, lockTitle
from trntrans import unlockTrans, lockTrans

version = '0.8.0'

# Find trophy block, unlock it, write it, then update the progress bar
def unlockTrophy(trophy_id):
    if unlockTitle(trophy_id):
        unlockTrans(trophy_id)
        print('ID: {:3} | Type: {} | Name: {}\nDesc: {}\n'.format(var.trophyData['id'][trophy_id], var.trophyData['type'][trophy_id], var.trophyData['name'][trophy_id], var.trophyData['desc'][trophy_id]))
        print('Unlock successful')
    else:
        print('Trophy already unlocked')

# Find trophy block, lock it, write it, then update the progress bar
def lockTrophy(trophy_id):
    if lockTitle(trophy_id):
        lockTrans(trophy_id)
        print('ID: {:3} | Type: {} | Name: {}\nDesc: {}\n'.format(var.trophyData['id'][trophy_id], var.trophyData['type'][trophy_id], var.trophyData['name'][trophy_id], var.trophyData['desc'][trophy_id]))
        print('Lock successful')
    else:
        print('Trophy already locked')

# Unlock all trophies
def unlockAll():
    for i in range(var.maxTrophies):
        timestamp = encodeTimestamp(var.date_str)
        if unlockTitle(i):
            unlockTrans(i)
    print('Unlocked {} {}'.format(var.processedCount, 'trophy' if var.processedCount == 1 else 'trophies'))

# Lock all trophies
def lockAll():
    for i in range(var.maxTrophies):
        if lockTitle(i):
            lockTrans(i)
    print('Locked {} {}'.format(var.processedCount, 'trophy' if var.processedCount == 1 else 'trophies'))

# Print trophy data for passed ID
def printTrophy(trophy_id):
  for i in range(len(var.trophyData['id'])):
    if var.trophyData['id'][i] == trophy_id:
      print('ID: {:3} | Type: {} | Name: {}\nDesc: {}\n'.format(var.trophyData['id'][i], var.trophyData['type'][i], var.trophyData['name'][i], var.trophyData['desc'][i]))
      break

# Print trophy data for all trophies
def printAll():
    for i in range(var.maxTrophies):
        printTrophy(i)

def main():
    # Arg parser for program options
    parser = argparse.ArgumentParser(description='Unlock or lock PS Vita trophies. Requires TROP.SFM, TRPTITLE.DAT & TRPTRANS.DAT (decrypted)')
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('ID', type=lambda s: s.lower(), help='Trophy ID number or "all" to process all trophies')
    group.add_argument('-u', '--unlock', action="store_true", help='Unlock trophy')
    group.add_argument('-l', '--lock', action="store_true", help='Lock trophy')
    group.add_argument('-p', '--print', action="store_true", help='Print trophy details')
    parser.add_argument('-ts', '--timestamp', help='Optional timestamp in format "YYYYMMDDHHMMSS" (default: current time)')

    # Check if required files exist
    if os.path.isfile(var.TROP) == False:
        print('TROP.SFM cannot be found')
        return 1
    if os.path.isfile(var.TITLE) == False:
        print('TRPTITLE.DAT cannot be found')
        return 1
    if os.path.isfile(var.TRANS) == False:
        print('TRPTRANS.DAT cannot be found')
        return 1

    # Initialize variables
    var.init_globals()
    var.init_trophyData()

    # Parse the TROP.SFM file for trophy data
    htmlparser = var.MyHTMLParser()
    with open(os.path.join(var.PATH, 'TROP.SFM'), 'r', encoding='utf-8') as f:
        trop = f.read()
    htmlparser.feed(str(trop))

    # Begin program
    print()
    print('{:^80}'.format('===== PSVTrophyIsGreat v.{} ====='.format(version)))
    print()

    # Check passed arguments
    args = parser.parse_args()

    # Set timestamp to current time if one was not provided
    if args.timestamp == None:
        var.date_str = datetime.now().strftime('%Y%m%d%H%M%S')
    else:
        var.date_str = args.timestamp

    # Run unlock functions
    if args.unlock:
        if args.ID == 'all':
            unlockAll()
        else:
            trophyID = int(args.ID)
            if trophyID < 0 or trophyID >= var.maxTrophies:
                print('Invalid trophy ID')
            else:
                unlockTrophy(trophyID)
    
    # Run lock functions
    if args.lock:
        if args.ID == 'all':
            lockAll()
        else:
            trophyID = int(args.ID)
            if trophyID < 0 or trophyID >= var.maxTrophies:
                print('Invalid trophy ID')
            else:
                lockTrophy(trophyID)
    
    # Run print functions
    if args.print:
        if args.ID == 'all':
            printAll()
        else:
            trophyID = int(args.ID)
            if trophyID < 0 or trophyID >= var.maxTrophies:
                print('Invalid trophy ID')
            else:
                printTrophy(trophyID)
    print()
    return 0

if __name__ == "__main__":
    main()
