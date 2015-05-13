Login Service Protocol
======================

Packet format
-------------

All the packet sent and received by this service follows the following packet
layout :

.. code-block:: text

    +0x00 : Size_Packet     [BYTE]
    +0x01 : Opcode_Packet   [BYTE]
    +0x02 : ProtoBuff_Data  // Depends of the opcode

Opcodes list
------------

0x01 (VerifyProtocolReq)
""""""""""""""""""""""""

The client (WAR.exe) send this packet after the connection.

Protocol buffer message types (VerifyProtocolReq.proto) :

.. code-block:: text

    message VerifyProtocolReq {
        required uint32 protocol_version = 1;
        required uint32 product_id = 2;
        required bytes client_public_key = 3;
    }

You must answer with opcode 0x02 (VerifyProtocolReply).

0x02 (VerifyProtocolReply)
""""""""""""""""""""""""""

This opcode is for the answer of opcode 0x01.

Protocol buffer message types (VerifyProtocolReply.proto) :

.. code-block:: text

    message VerifyProtocolReply {
        required ResultCode result_code = 1;
        optional bytes iv1 = 2;
        optional bytes iv2 = 3;
    }

The result code must be RES_SUCESS, and the iv1, and iv2, can be something
random like : iv1 = "\x42" * 16 and iv2 = "\x42" * 16.

0x05 (AuthSessionTokenReq)
""""""""""""""""""""""""""

After answering with opcode 0x02 (*TODO CONFIRM ALL CASES*), this opcode will be received.

Protocol buffer message types (AuthSessionTokenReq.proto) :

.. code-block:: text

    message AuthSessionTokenReq {
        required bytes session_token = 1;
    }

You must answer with opcode 0x06 (AuthSessionTokenReply).

0x06 (AuthSessionTokenReply)
""""""""""""""""""""""""""""

This opcode is for the answer of opcode 0x05.

Protocol buffer message types (AuthSessionTokenReply.proto) :

.. code-block:: text

    message AuthSessionTokenReply {
        required ResultCode result_code = 1;
    }

The result code must be RES_SUCESS.

0x07 (GetCharSummaryListReq)
""""""""""""""""""""""""""""

No ProtoBuff_Data for this opcode.

Answer with opcode 0x08 (GetCharSummaryListReply).

0x08 (GetCharSummaryListReply)
""""""""""""""""""""""""""""""

Protocol buffer message types (GetCharSummaryListReply.proto) :

.. code-block:: text

    message GetCharSummaryListReply {
        required ResultCode result_code = 1;
        repeated CharSummary summary_list = 2;
    }

CharSummary
'''''''''''

Protocol buffer message types (CharSummary.proto) :

.. code-block:: text

    message CharSummary {
        required uint32 server_id = 1;
        required uint32 character_id = 2;
        required int64 last_played_time = 3;
        optional string xml_data = 4;
    }

*TODO describe*

0x09 (GetClusterList)
"""""""""""""""""""""

No ProtoBuff_Data for this opcode.

Answer with opcode 0x0A (GetClusterListReply).

0x0A (GetClusterListReply)
""""""""""""""""""""""""""

This opcode is the answer of 0x09.

Protocol buffer message types (GetClusterListReply.proto) :

.. code-block:: text

    message GetClusterListReply {
        required ResultCode result_code = 1;
        repeated ClusterInfo cluster_list = 2;
    }

ClusterInfo
'''''''''''

Protocol buffer message types (ClusterInfo.proto) :

.. code-block:: text

    message ClusterInfo {
        required uint32 cluster_id = 1;
        required string cluster_name = 2;
        optional string lobby_host = 3;
        optional uint32 lobby_port = 4;
        optional uint32 cluster_pop = 5;
        optional uint32 max_cluster_pop = 6;
        optional ClusterPopStatus cluster_pop_status = 7;
        required uint32 language_id = 8;
        required ClusterStatus cluster_status = 9;
        repeated ServerInfo server_list = 10;
        repeated ClusterProp property_list = 11;
    }

In cluster_id put the REALM_ID, in cluster_name put REALM_NAME, in lobby host
put ip address of your World Service and service port in lobby_port.

Language_id
@@@@@@@@@@@

* *TODO*
* *TODO*
* *TODO value*

For cluster_status set STATUS_ONLINE.

ServerInfo
@@@@@@@@@@

Protocol buffer message types (ServerInfo.proto) :

.. code-block:: text

    message ServerInfo {
        required uint32 server_id = 1;
        required string server_name = 2;
    }

Put REALM_ID in server_id and REALM_NAME in server_name.

ClusterProp
@@@@@@@@@@@

*TODO*

Protocol buffer message types (ClusterProp.proto) :

.. code-block:: text

    message ClusterProp {
        required string prop_name = 1;
        required string prop_value = 2;
    }

And finally set the result_code to RES_SUCESS.


0x0B (MetricEventNotify)
""""""""""""""""""""""""

Protocol buffer message types (MetricEventNotify.proto) :

.. code-block:: text

    message MetricEventNotify {
        required uint32 event_id = 1;
        optional bytes event_data = 2;
    }

Don't know how to deal with this stuff (*TODO*).

0x0C (GetAcctPropListReply)
"""""""""""""""""""""""""""

This opcode is for the answer of opcode 0x0D.

Protocol buffer message types (GetAcctPropListReply.proto) :

.. code-block:: text

    message GetAcctPropListReply {
        required ResultCode result_code = 1;
        repeated AcctProp prop_list = 2;
    }

Protocol buffer message types (AcctProp.proto) :

.. code-block:: text

    message AcctProp {
        required uint32 property_id = 1;
        required int32 property_value = 2;
    }

No informations related to property_id and property_value (*TODO*).

You can answer just by setting the result_code to RES_SUCESS.

0x0D (GetAccountProperties)
"""""""""""""""""""""""""""

Nothing related to the proto inside WAR.exe has been found so this proto is maybe wrong.

Protocol buffer message types (GetAccountProperties.proto) :

.. code-block:: text

    message GetAcctPropListReq {
        repeated AcctProp prop_list = 1;
    }

You must answer with opcode 0x0C (GetAcctPropListReply)

All data inside packet use the Google's data interchange format [#Google_proto]_.

References
----------

.. [#Google_proto] https://code.google.com/p/protobuf/