Login Service Handler
=====================

This file gives all the location of each important functions used for handling
received messages for login service.

LoginServiceHandler
-------------------

All messages received for the login service are handled by this function :

* VA    : 0x0095858B
* RVA   : 0x0055858B

.. code-block:: text
    :caption: PAT signature of LoginServiceHandler (for sigmake IDA)

    b8........e8........51515356578bd98365fc008b430c8b308b7d088b4704 19 0016 01F5 :0000 LoginServiceHandler

Handle_VerifyProtocolReply
--------------------------

* VA    : 0x0095734B
* RVA   : 0x0055734B

.. code-block:: text
    :caption: PAT signature of Handle_VerifyProtocolReply (for sigmake IDA)

    558bec83e4f86aff64a10000000068........506489250000000083ec58538b 05 89B4 0153 :0000 Handle_VerifyProtocolReply

Handle_AuthInitialTokenReply
----------------------------

* VA    : 0x0095749E
* RVA   : 0x0055749E

.. code-block:: text
    :caption: PAT signature of Handle_AuthInitialTokenReply (for sigmake IDA)

    558bec538b5d085657bf........578bf08b460c8b0868........6a0350ff51 14 06A6 00F1 :0000 Handle_AuthInitialTokenReply

Handle_AuthSessionTokenReply
----------------------------

* VA    : 0x0095758F
* RVA   : 0x0055758F

.. code-block:: text
    :caption: PAT signature of Handle_AuthSessionTokenReply (for sigmake IDA)

    538b5c24085657be........568bf88b470c8b0868........6a0350ff51048b 12 9A91 00B0 :0000 Handle_AuthSessionTokenReply

Handle_GetCharListReply
-----------------------

* VA    : 0x00957B11
* RVA   : 0x00557B11

.. code-block:: text
    :caption: PAT signature of Handle_GetCharListReply (for sigmake IDA)

    558bec83e4f86aff68........64a100000000506489250000000083ec38538b 05 3207 021D :0000 Handle_GetCharListReply

Handle_GetClusterListReply
--------------------------

* VA    : 0x0095763F
* RVA   : 0x0055763F

.. code-block:: text
    :caption: PAT signature of Handle_GetClusterListReply (for sigmake IDA)

    558bec83e4f86aff68........64a100000000506489250000000081ecc80000 12 C9A2 04D2 :0000 Handle_GetClusterListReply

Handle_GetAccountPropertiesReply
--------------------------------

* VA    : 0x00957D2E
* RVA   : 0x00557D2E

.. code-block:: text
    :caption: PAT signature of Handle_GetAccountPropertiesReply (for sigmake IDA)

    558bec83e4f86aff68........64a100000000506489250000000083ec248364 0E 3AC3 0147 :0000 Handle_GetAccountPropertiesReply
