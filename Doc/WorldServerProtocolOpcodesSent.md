# World Server Opcodes list sent

List of opcodes and packet data structur for all packets sent TO the
client.

## 0x13

Answer to packet 0x13.

    004C3300 mov     [ebp+var_10], offset aF_request_char ; "F_REQUEST_CHAR_TEMPLATES"

...

    004C8AA5 Handle_0x13 proc near

Packet data :

    +0x00   :   NB_AVAILABLETEMPLATES_NAMES     [DWORD]
    +0x04   :   TEMPLATES_NAMES                 [WAR_BUFFER] * NB_AVAILABLETEMPLATES_NAMES
    +0x..   :   NB_AVAILABLETEMPLATES_CLASSES   [DWORD]
    +0x..   :   TEMPLATES_CLASSES               [DWORD] * NB_AVAILABLETEMPLATES_CLASSES
    +0x..   :   NB_AVAILABLETEMPLATES_RACES     [DWORD]
    +0x..   :   TEMPLATES_RACES                 [DWORD] * NB_AVAILABLETEMPLATES_RACES
    +0x..   :   NB_AVAILABLETEMPLATES_GENDERS   [DWORD]
    +0x..   :   TEMPLATES_GENDERS               [DWORD] * NB_AVAILABLETEMPLATES_GENDERS

## 0x19

Answer to packet 0x35.

    004C973B Handle_0x19 proc near

## 0x55

Answer to packet 0x54 with command 0x2D53

    004C8CC1 Handle_0x55 proc near

Packet data :

    +0x00   :   UNK_DWORD_00        [DWORD]

## 0x56

Answer to packet 0x54 with command 0x2D58

No function handler.

    .text:004C3C23                 movzx   eax, byte ptr [edi]  // Buffer
    .text:004C3C26                 push    eax
    .text:004C3C27                 push    56h

Packet data :

    +0x00   :   UNK_BYTE_00         [BYTE]

## 0x59

Answer to packet 0x91 in case of character error creation.

    004C991E Handle_0x59 proc near

Packet data :

    +0x00   :   PADDING             [BYTE] * 24
    +0x18   :   MSG_ERROR           [BYTE] * 100

MSG\_ERROR will be displayed

## 0x6A

Answer to packet 0x68.
Check if the character name is valid and not used.

No function handler, only check the byte value at offset 0x32, WTF

    .text:004C3E58                 xor     eax, eax
    .text:004C3E5A                 cmp     [edi+32h], al
    .text:004C3E5D                 setz    al

Packet data :

    +0x00   :   DATA_OSEF           [BYTE] * 0x31
    +0x32   :   NAME_VALID          [BYTE]

## 0x80

Answer to packet 0xB8.

    004C8A86 Handle_0x80 proc near

Packet data :

    +0x00   :   SESSION_ID          [WORD]


## 0x82

Answer to packet 0x0F.

    004C88F9     Handle_0x82 proc near
    ...
    004C8954 mov     [ebp+var_C], offset aS_connected ; "S_CONNECTED"

Packet data :

    +0x00   :   UNK_BYTE_00         [BYTE]
    +0x01   :   UNK_BYTE_01         [BYTE]
    +0x02   :   UNK_BYTE_02         [BYTE]
    +0x03   :   UNK_BYTE_03         [BYTE]
    +0x04   :   PROTOCOL_VERSION    [DWORD]
    +0x08   :   SERVER_ID           [BYTE]
    +0x09   :   UNK_BYTE_04         [BYTE]
    +0x0A   :   UNK_BYTE_05         [BYTE]
    +0x0B   :   UNK_BYTE_06         [BYTE]
    +0x0C   :   TRANSFER_FLAG       [BYTE]
    +0x0D   :   USERNAME            [WAR_B_BUFFER]
    +0x..   :   SERVER_NAME         [WAR_B_BUFFER]
    +0x..   :   UNK_BYTE_07         [BYTE]  // nb iteration to read a BYTE
    +0x..   :   UNK_DATA            [BYTE] * UNK_BYTE_07

Protocol version must be equal to 0xEB8DB21.

## 0x85

Answer to packet 0x17.

No function handler.

## 0x8A

Answer to packet 0x5C.

    004C8883     Handle_0x8A proc near

* VA    : 0x004C8883
* RVA   : 0x000C8883

Packet data :

    +0x00   :   SEND_KEY            [BYTE]

SEND_KEY must be equal to 1, and the client will send opcode 0x5C again
containing the key for encrypt/decrypt.

## 0x88

...

    004DE151 Handle_0x88 proc near

...

Packet data :

    +0x00   :   UNK_DWORD_00        [DWORD]
    +0x04   :   PLAYER_MONEY        [DWORD]

## 0x39

Send experience informations

    .text:004C382F                 push    dword ptr [edi] ; netlong
    .text:004C3831                 call    ntohl
    .text:004C3836                 push    dword ptr [edi+4] ; netlong
    .text:004C3839                 mov     [edi], eax
    .text:004C383B                 call    ntohl
    .text:004C3840                 push    dword ptr [edi+8] ; netlong
    .text:004C3843                 mov     [edi+4], eax
    .text:004C3846                 call    ntohl
    .text:004C384B                 and     [ebp+var_14], 0
    .text:004C384F                 mov     [edi+8], eax
    .text:004C3852                 lea     eax, [ebx-0Dh]
    .text:004C3855                 mov     [ebp+var_1C], eax
    .text:004C3858                 mov     [ebp+var_18], eax
    .text:004C385B                 lea     eax, [ebp+var_20]
    .text:004C385E                 lea     ecx, [edi+0Dh]
    .text:004C3861                 push    eax
    .text:004C3862                 mov     [ebp+var_20], ecx
    .text:004C3865                 mov     [ebp+var_10], offset aF_player_exper ; "F_PLAYER_EXPERIENCE"

Packet data :

    +0x00   :   CURRENT_EXPERIENCE  [DWORD]
    +0x04   :   NEXT_LEVEL_EXP      [DWORD]
    +0x08   :   RESTED_EXPERIENCE   [DWORD]
    +0x0C   :   CURRENT_LEVEL       [DWORD] // Little Endian

## 0x4E

Send renown informations

    .text:004C3A28                 push    dword ptr [edi] ; netlong
    .text:004C3A2A                 call    ntohl
    .text:004C3A2F                 push    dword ptr [edi+4] ; netlong
    .text:004C3A32                 mov     [edi], eax
    .text:004C3A34                 call    ntohl
    .text:004C3A39                 and     [ebp+var_14], 0
    .text:004C3A3D                 mov     [edi+4], eax
    .text:004C3A40                 lea     eax, [ebx-0Bh]
    .text:004C3A43                 mov     [ebp+var_1C], eax
    .text:004C3A46                 mov     [ebp+var_18], eax
    .text:004C3A49                 lea     eax, [ebp+var_20]
    .text:004C3A4C                 lea     ecx, [edi+0Bh]
    .text:004C3A4F                 push    eax
    .text:004C3A50                 mov     [ebp+var_20], ecx
    .text:004C3A53                 mov     [ebp+var_10], offset aF_player_renow ; "F_PLAYER_RENOWN"

Packet data :

    +0x00   :   CURRENT_RENOWN_EXP  [DWORD]
    +0x04   :   NEXT_RENOWN_EXP     [DWORD]
    +0x08   :   RENOWN_RANK         [DWORD] // Little Endian

## 0x05

Send Health informations

    .text:004DBBB0 Handle_0x05     proc near

Packet data :

    +0x00   :   ACTUAL_HIT_POINTS   [DWORD]
    +0x04   :   MAX_HIT_POINTS      [DWORD]
    +0x08   :   ACTUAL_ACTION_POINTS[WORD]
    +0x0A   :   MAX_ACTION_POINTS   [WORD]
    +0x0C   :   UNK_WORD_00         [WORD]
    +0x0E   :   UNK_WORD_01         [WORD]

## 0x52

Send Wealth informations

Packet data :

    +0x00   :   UNK_DWORD_00        [DWORD]
    +0x04   :   PLAYER_MONEY        [DWORD]

## 0x1E

Send Velocity informations

Packet data :

    +0x00   :   UNK_WORD_00         [WORD]

## 0xAA

    .text:004D64A2 Handle_0xAA     proc near

Packet data :

    +0x00   :   NB_ITEM             [BYTE]
    +0x01   :   PADDING             [BYTE]
    +0x02   :   PADDING             [WORD]
    +0x04   :   OBJECT(S)           [WAR_OBJECT] * NB_TIME
