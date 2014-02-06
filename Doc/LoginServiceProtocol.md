# Login Service Protocol

WAR.exe at launch will extract XML data from the file *data/mythloginserviceconfig.xml* (data.myp ; Hash name : 0x3FE03665349E2A8C)

The original content is :

    <?xml version="1.0" encoding="utf-8"?>
    <RootElementOfAnyName>
      <MythLoginServiceConfig>
        <Settings>
          <ProductId>2</ProductId>
          <MessageTimeoutSecs>20</MessageTimeoutSecs>
        </Settings>
        <RegionList>
          <Region regionName="WAR Live">
            <PingServer serverName="None">
              <Address>0.0.0.0</Address>
              <Port>0</Port>
            </PingServer>
            <LoginServerList>
              <LoginServer serverName="login 1">
                <Address>107.23.232.189</Address>
                <Port>8046</Port>
              </LoginServer>
              <LoginServer serverName="login 2">
                <Address>107.23.135.143</Address>
                <Port>8046</Port>
              </LoginServer>
            </LoginServerList>
          </Region>
        </RegionList>
      </MythLoginServiceConfig>
    </RootElementOfAnyName>

If you want to be able to manage your own login service, you have to replace
the content of the file inside the data.myp archive, or you can use this
[DLL project][replacexml] that replace the content at runtime.

## Packet format

All the packet sent and received by this service follows the following packet
layout :

    +0x00 : Size_Packet     [BYTE]
    +0x01 : Opcode_Packet   [BYTE]
    +0x02 : ProtoBuff_Data  // Depends of the opcode

## Opcodes list

### 0x01 (VerifyProtocolReq)

The client (WAR.exe) send this packet after the connection.

Protocol buffer message types (VerifyProtocolReq.proto) :

    message VerifyProtocolReq {
     required uint32 protocol_version = 1;
     required uint32 product_id = 2;
     required bytes client_public_key = 3;
    }

You must answer with opcode 0x02 (VerifyProtocolReply).

### 0x02 (VerifyProtocolReply)

This opcode is for the answer of opcode 0x01.

Protocol buffer message types (VerifyProtocolReply.proto) :

    message VerifyProtocolReply {
     required ResultCode result_code = 1;
     optional bytes iv1 = 2;
     optional bytes iv2 = 3;
    }

The result code must be RES_SUCESS, and the iv1, and iv2, can be something
random like : iv1 = "\x42" * 16 and iv2 = "\x42" * 16.

### 0x05 (AuthSessionTokenReq)

After answering with opcode 0x02 (*TODO CONFIRM ALL CASES*), this opcode will be received.

Protocol buffer message types (AuthSessionTokenReq.proto) :

    message AuthSessionTokenReq {
     required bytes session_token = 1;
    }

You must answer with opcode 0x06 (AuthSessionTokenReply).

### 0x06 (AuthSessionTokenReply)

This opcode is for the answer of opcode 0x05.

Protocol buffer message types (AuthSessionTokenReply.proto) :

    message AuthSessionTokenReply {
     required ResultCode result_code = 1;
    }

The result code must be RES_SUCESS.


[replacexml]: https://github.com/w4kfu/waronline_fun/tree/master/Toolz/replace_xml
