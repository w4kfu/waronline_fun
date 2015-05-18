Server Emulator
===============

.. warning::

    Server emulator is not fully functional. It's just a proof of concept.
    Lots of WorldServer events are only triggerable from python 
    `InteractiveConsole`_.
    
.. _server-requirements:    
    
Requirements
------------

In order to run the differents scripts, you must have installed:

* Python 2.7 can be found on the official website `here <https://www.python.org/ftp/python/2.7.9/python-2.7.9.msi>`_
* Python Protobuf : Microsoft Installer available `protobuf-2.5.0.win32.msi <http://war.w4kfu.com/protobuf-2.5.0.win32.msi>`_
* Python Colorama : Microsoft Installer available `colorama-0.3.3.win32.msi <http://war.w4kfu.com/colorama-0.3.3.win32.msi>`_
* Python Construct : Microsoft Installer available `construct-2.5.2.win32.msi <http://war.w4kfu.com/construct-2.5.2.win32.msi>`_
* Python six (requirement for construct) : Microsoft Installer available `six-1.9.0.win32.msi <http://war.w4kfu.com/six-1.9.0.win32.msi>`_
     
MythLoginServiceConfig
----------------------
   
:file:`WAR.exe` at launch will extract XML data from the file :file:`data/MythLoginServiceConfig.xml` (data.myp ; Hash name : 0x3FE03665349E2A8C).

XML data contains address and port used for the LoginServer, if you want to run
your own server, you will have to replace this configuration file.

:file:`MythLoginServiceConfig.xml` file entry informations in :file:`data.myp`:

* offset = 12463784
* size_header = 136
* sizez = 306
* size = 810
* name = 4602738627475024524
* crc = 1840099700
* flag = 1   
    
.. code-block:: python
    :caption: Get original content of MythLoginServiceConfig.xml from data.myp
    
    >>> import hashlib
    >>> import zlib
    >>> hashlib.md5(open("data.myp", "rb").read()).hexdigest()
    'fc0cac05ba416e920b3a6dd7defa8fc1'
    >>> fd = open("data.myp", "rb")
    >>> fd.seek(12463784 + 136, 0)          # seek to (offset + size_header)
    >>> print zlib.decompress(fd.read(306)) # read sizez
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
    
Loading of this file is done in sub at 0x004ACE41.
    
.. code-block:: text

    .text:004ACF1E 68 AC 98 A7 00          push    offset aMythloginservi ; "MythLoginServiceConfig.xml"
    .text:004ACF23 68 58 24 A7 00          push    offset aData    ; "data"    
    
    ...
    
    .text:004ACF6A E8 C5 06 3E 00          call    sub_88D634
    .text:004ACF6F 8B 08                   mov     ecx, [eax]
    
The call to 0x0088D634 will get the content of file :file:`MythLoginServiceConfig.xml` from
:file:`data.myp` archive. 
    
In order to not alter the :file:`data.myp` file, we can insert a Hook just after 
the call 0x0088D634 and we will be able to replace the content of the file.

The DLL `replace_xml`_ will setup an hook for replacing the content at runtime 
when injected inside :file:`WAR.exe`.

Replace XML
-----------

You can create a file :file:`server_ip.txt` inside warhammer online folder that 
will be load by :file:`replace_xml.dll` for the server address.

.. code-block:: text
    :caption: Example server_ip.txt

    E:\Game\Warhammer Online>type server_ip.txt
    192.168.1.42
    
If :file:`server_ip.txt` is not found, the default ip address value is: 127.0.0.1
 
Inject DLL
----------

You can use the project `injector`_ for injecting the DLL in :file:`WAR.exe`.

.. warning::

    acctname and sesstoken arguments for WAR.exe are hardcoded inside the injector
    
.. code-block:: text
    :caption: Example
    
    E:\Game\Warhammer Online>war_injector.exe replace_xml.dll
    
You can create a shortcut (.lnk) or a script (.bat) for next launch

Now warhammer online will connect to the LoginServer at IP address you specified 
or default one.
    
LoginServer
-----------   

Before running :file:`WAR_LoginServer.py`, you must have installed correctly all 
the requirements (see :ref:`server-requirements`.).

Open a window cmd shell, navigate to server folder, and launch 
WAR_LoginServer.py.

Any authentication token is accepted, there is no check/validation.

If the WorldServer is not running on localhost, edit in the function :func:`handle_GetClusterList` 
in :file:`WAR_LoginServer.py` the following line:

.. code-block:: python

    cluster_info.lobby_host = "127.0.0.1" # IP TO REPLACE


WorldServer
-----------

Before running :file:`WAR_WorldServer.py`, you must have installed correctly 
all the requirements (see :ref:`server-requirements`.).

Open a window cmd shell, navigate to server folder, and launch WAR_WorldServer.py.

Only one character is sent to the client for character list, but you can edit the 
dict :class:`CHARACTER` in :func:`premaidcharacter`.

Once your character choosed, you can edit the packet :class:`PACKET_S_PLAYER_INITTED` 
in :func:`response_S_PLAYER_INITTED` for all infos regarding the positioning of 
your character.

:class:`object_id` of player is hardcoded to value 0x4242.

Interactive Console
"""""""""""""""""""

TODO
    
References
----------   
    
.. [#InteractiveConsole] https://docs.python.org/2/library/code.html
.. [#replace_xml] https://github.com/w4kfu/waronline_fun/tree/master/Toolz/replace_xml
.. [#injector] https://github.com/w4kfu/waronline_fun/tree/master/Toolz/injector