#file  -- trntrans.py --

import var
import os
from helpers import readBE, readLE

def unlockTrans(trophy_id):   
    with open(var.TRANS, 'r+b') as f:
        # Read the contents of TRNTRANS.DAT
        trptrans = f.read()

        # Set offsets for how many trophies are in the file and where the trophy blocks are
        trans_num_offset = readBE(trptrans, 0x84, 4) + 0x24
        trans_trp_offset = readBE(trptrans, 0xA4, 4)

        # Gets number of trophies in file and increases it for added trophy
        trans_num = readBE(trptrans, trans_num_offset, 4)
        f.seek(trans_num_offset)
        f.write((trans_num + 1).to_bytes(4, byteorder='big'))

        # Move to the next available empty block and write trophy data
        f.seek(trans_trp_offset + (var.TRANBLOCK * trans_num))
        f.seek(0x14, 1)
        f.write((0x02).to_bytes(4, byteorder='big'))
        f.seek(0x18, 1)
        f.write(trophy_id.to_bytes(4, byteorder='big'))
        f.write(var.trophy_type.to_bytes(4, byteorder='big'))
        f.write((0x2000).to_bytes(4, byteorder='big'))
        f.seek(0x4, 1)
        f.write(var.timestamp)

def lockTrans(trophy_id):
    with open(var.TRANS, 'r+b') as f:
        # Read contents of TRPTITLE.DAT
        trptrans = f.read()

        # Set offsets for how many trophies are in the file and where the trophy blocks are
        trans_num_offset = readBE(trptrans, 0x84, 4) + 0x24
        trans_trp_offset = readBE(trptrans, 0xA4, 4)

        # Gets number of trophies in file and decreases it for removed trophy and decrease last sync trophy
        trans_num = readBE(trptrans, trans_num_offset, 4)
        trans_synced = readBE(trptrans, trans_num_offset + 0x4, 4)
        f.seek(trans_num_offset)
        f.write((trans_num - 1).to_bytes(4, byteorder='big'))

        # If there's only one trophy, prevent last synced trophy from reducing
        if trans_synced > 1:
            f.write((trans_synced - 1).to_bytes(4, byteorder='big'))

        # Loop through trophy blocks looking for trophy ID to remove
        for i in range(1, trans_num):
            f.seek(trans_trp_offset + (var.TRANBLOCK * i))
            f.seek(0x30, 1)

            # If trophy block does not match, continue loop
            if f.read(0x80)[:4] != trophy_id.to_bytes(4, byteorder='big'):
                continue

            # When found, move each remaining entry up to prevent blank spaces
            while i < trans_num:
                f.seek(0x30, 1)
                blk = f.read(0x80)
                f.seek(var.TRANBLOCK * -2, 1)
                f.seek(0x30, 1)
                f.write(blk)
                f.seek(var.TRANBLOCK, 1)
                i += 1
            break
        
        # Cleanup final block to ensure it's empty
        f.seek(var.TRANBLOCK * -2, 1)
        f.seek(0x14, 1)
        f.write((0x0.to_bytes(4, byteorder='big')))
