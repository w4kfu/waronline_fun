# World Server Opcodes list received

List of opcodes and packet data structur for all received packet FROM the
client.

## 0x04

    004B2E63 SendPacket_0x04 proc near

Packet data :

    +0x00   :   SESSION_ID          [WORD]
    +0x02   :   UNK_WORD_00         [WORD]

## 0x0B

    004B2F33 PrepareSendPacket_0x0B proc near

Packt data :

    +0x00   :   UNK_DWORD_00        [DWORD]
    +0x04   :   UNK_DWORD_01        [DWORD]
    +0x08   :   UNK_DWORD_02        [DWORD]
    +0x0C   :   UNK_DATA            [WORD] * 3
    +0x012  :   UNK_WORD_00         [WORD]

The server must answer with opcode 0x81.

## 0x0F

...

    004B29A8     PrepareSendPacket_0x0F_01 proc near

...

    004B27CF     PrepareSendPacket_0x0F_02 proc near

Packet data :

    +0x00   :   UNK_BYTE_00         [BYTE]
    +0x01   :   UNK_BYTE_01         [BYTE]
    +0x02   :   MAJOR_VERSION       [BYTE]
    +0x03   :   MINOR_VERSION       [BYTE]
    +0x04   :   REVISION_VERSION    [BYTE]
    +0x05   :   UNK_BYTE_02         [BYTE]
    +0x06   :   UNK_WORD_00         [WORD]
    +0x08   :   PROTOCOL_VERSION    [DWORD]
    +0x0C   :   SESSION             [BYTE] * 101
    +0x71   :   USERNAME            [BYTE] * 21
    +0x86   :   SIZE_XML            [WORD]
    +0x88   :   XML_DATA            [BYTE] * SIZE_XML

### XML DATA

*TODO, not really important*

The server must answer with opcode 0x82.

## 0x13

...

    004B162A SendPacket_0x13 proc near

Packet data :

    +0x00   :   UNK_BYTE_00         [BYTE]

The server must answer with opcode 0x13.

## 0x54

This packet can be send from two functions.

Packet data :

    +0x00   :   COMMAND             [WORD]
    +0x02   :   UNK_BYTE_00         [BYTE]

### 0x2D58

    004B19C6 SendPacket_0x54_0x2D58 proc near

The server must answer with opcode 0x56.

### 0x2D53

    004B1A64 SendPacket_0x54_0x2D53 proc near

The server must answer with opcode 0x55.


## 0x5C

First packet received from the client after connection.
This packet can be send from two functions.

### 0x5C (First)

    004B17D7     SendPacket_0x5C_1 proc near

* VA    : 0x004B17D7
* RVA   : 0x000B17D7

Packet data :

    +0x00   :   KEY_PRESENT         [BYTE]
    +0x01   :   UNK_BYTE_00         [BYTE]
    +0x02   :   MAJOR_VERSION       [BYTE]
    +0x03   :   MINOR_VERSION       [BYTE]
    +0x04   :   REVISION_VERSION    [BYTE]
    +0x05   :   UNK_BYTE_01         [BYTE]

The server must answer with opcode 0x8A.

### 0x5C (Second)

    004B2B84     SendPacket_0x5C_2 proc near

* VA    : 0x004B2B84
* RVA   : 0x000B2B84

Packet data :

    +0x00   :   KEY_PRESENT         [BYTE]
    +0x01   :   UNK_BYTE_00         [BYTE]
    +0x02   :   MAJOR_VERSION       [BYTE]
    +0x03   :   MINOR_VERSION       [BYTE]
    +0x04   :   REVISION_VERSION    [BYTE]
    +0x05   :   UNK_BYTE_01         [BYTE]
    +0x06   :   WAR_RC4_KEY         [BYTE] * 256

The server doesn't need to answer to this.

## 0x68

    004B3ABD SendPacket_0x68 proc near

Packet data :

    +0x00   :   CHAR_NAME           [BYTE] * 24
    +0x18   :   PADDING             [DWORD]
    +0x1C   :   PADDING             [WORD]
    +0x1E   :   USER_NAME           [BYTE] * 20
    +0x32   :   PADDING             [DWORD]

The server must answer with opcode 0x6A.

## 0x91

    004C6DFA SendPacket_0x91 proc near

Packet data :

The server must answer with opcode 0x58, or 0x59 for error.

## 0xB8

    004B2C27 PrepareSendPacket_0xB8 proc near

Packet data :

    +0x00   :   UNK_WORD_00         [WORD]
    +0x02   :   UNK_BYTE_00         [BYTE]
    +0x03   :   UNK_BYTE_01         [BYTE]
    +0x04   :   UNK_DATA_00         [BYTE] * 24
    +0x1C   :   NS_PORT             [WORD]
    +0x1E   :   LANGAGE             [BYTE] * 6
    +0x24   :   UNK_DWORD_00        [DWORD]
    +0x28   :   UNK_DWORD_01        [DWORD]
    +0x2C   :   UNK_DWORD_02        [DWORD]

The server must answer with opcode 0x80.
