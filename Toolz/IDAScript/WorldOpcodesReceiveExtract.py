from idaapi import *
from idc import *
from idautils import *

# HandleWorldPacket
FUNC_EA = 0x004C30CE

TABLE_OPCODES = 0x004C56FA

SWITCH_TABLE = 0x004C5482

MAX_OPCODES_ENTRY = 0xFD # 253

for i in xrange(0, MAX_OPCODES_ENTRY):
    index = Byte(TABLE_OPCODES + i)
    loc = Dword(SWITCH_TABLE + (index * 4))
    print "[+] Opcode %02X (%d) ; index %02X (%d) ; Loc = %08X" % (i + 1, i + 1, index, index, loc)