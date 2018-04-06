#file  -- trntitle.py --

import var
from helpers import readBE, readLE, encodeTimestamp

def unlockTitle(trophy_id):
    var.timestamp = encodeTimestamp(var.date_str)
    with open(var.TITLE, 'r+b') as f:
        # Read contents of TRPTITLE.DAT
        trptitle = f.read()

        # Set offsets for main progress bar and two trophy blocks
        progress_offset = readBE(trptitle, 0x124, 4) + 0x70
        trophy_offset1 = readBE(trptitle, 0x104, 4) + (trophy_id * var.TRPBLOCK1)
        trophy_offset2 = readBE(trptitle, 0x164, 4) + (trophy_id * var.TRPBLOCK2)

        # Assigns trophy blocks for easier parsing and editing
        trophyblock1 = bytearray(trptitle[trophy_offset1:trophy_offset1 + var.TRPBLOCK1])
        trophyblock2 = bytearray(trptitle[trophy_offset2:trophy_offset2 + var.TRPBLOCK2])

        # Checks if trophy is already unlocked and returns
        if trophyblock2[var.TROPHYSTATE] == var.UNLOCKED:
            return False

        # Obtain trophy type (Bronze, Silver, Gold, Platinum)
        var.trophy_type = readBE(trophyblock1, 0x14, 4)

        # Obtain group IDs of the trophies from trophy block 1 for later use
        group_id = readBE(trophyblock1, 0x24, 4)

        # Sets unlocked status in both trophy block 2, sets unlock time
        trophyblock2[var.TROPHYSTATE] = var.UNLOCKED
        trophyblock2[var.TROPHYDATE1] = var.timestamp

        # Writes modified trophy block 2 to file
        f.seek(trophy_offset2)
        f.write(trophyblock2)

        # Checks and updates main progress bar
        progress = readLE(trptitle, progress_offset, 16)
        progress |= (1 << trophy_id)
        f.seek(progress_offset)
        f.write(progress.to_bytes(16, byteorder='little'))
        f.seek(-0x20, 1)

        # Checks for group IDs and updates those progress bars and update dates separately
        if group_id == 0xFFFFFFFF:
            f.seek(var.GROUPSIZE, 1)
            progress = readLE(trptitle, progress_offset + var.GROUPSIZE, 16)
        else:
            f.seek(var.GROUPSIZE * (group_id + 2), 1)
            progress = readLE(trptitle, progress_offset + (var.GROUPSIZE * (group_id + 2)), 16)

        f.write(var.timestamp)
        f.seek(0x8, 1)
        progress |= (1 << trophy_id)
        f.write(progress.to_bytes(16, byteorder='little'))
    # Increase count for unlockAll() output
    var.processedCount += 1
    return True

def lockTitle(trophy_id):
    with open(var.TITLE, 'r+b') as f:
        # Read contents of TRPTITLE.DAT
        trptitle = f.read()

        # Set offsets for main progress bar and two trophy blocks
        progress_offset = readBE(trptitle, 0x124, 4) + 0x70
        trophy_offset1 = readBE(trptitle, 0x104, 4) + (trophy_id * var.TRPBLOCK1)
        trophy_offset2 = readBE(trptitle, 0x164, 4) + (trophy_id * var.TRPBLOCK2)
        trophyblock1 = bytearray(trptitle[trophy_offset1:trophy_offset1 + var.TRPBLOCK1])
        trophyblock2 = bytearray(trptitle[trophy_offset2:trophy_offset2 + var.TRPBLOCK2])

        # Checks if trophy is already locked and returns
        if trophyblock2[var.TROPHYSTATE] == var.LOCKED:
            return False

        # Obtain group IDs of the trophies from trophy block 1 for later use
        group_id = readBE(trophyblock1, 0x24, 4)

        # Sets locked status in both trophy block 1 and 2, clears unlock time
        trophyblock2[var.TROPHYSTATE] = var.LOCKED
        trophyblock2[var.TROPHYSSYNC] = var.NOTSYNCED
        trophyblock2[var.TROPHYDATE1] = var.EMPTYDATE
        trophyblock2[var.TROPHYDATE2] = var.EMPTYDATE

        # Writes modified trophy block 1 and 2 to file
        f.seek(trophy_offset2)
        f.write(trophyblock2)

        # Checks and updates main progress bar
        progress = readLE(trptitle, progress_offset, 16)
        progress &= 0xFFFFFFFFFFFFFFFFFFFFFFFF ^ (1 << trophy_id)
        f.seek(progress_offset)
        f.write(progress.to_bytes(16, byteorder='little'))
        f.seek(-0x20, 1)

        # Checks for group IDs and updates those progress bars and update dates separately
        if group_id == 0xFFFFFFFF:
            f.seek(var.GROUPSIZE, 1)
            progress = readLE(trptitle, progress_offset + var.GROUPSIZE, 16)
        else:
            f.seek(var.GROUPSIZE * (group_id + 2), 1)
            progress = readLE(trptitle, progress_offset + (var.GROUPSIZE * (group_id + 2)), 16)
        f.write(var.EMPTYDATE)
        f.write(var.EMPTYDATE)
        progress &= 0xFFFFFFFFFFFFFFFFFFFFFFFF ^ (1 << trophy_id)
        f.write(progress.to_bytes(16, byteorder='little')) 
    # Increase count for lockAll() output
    var.processedCount += 1
    return True
