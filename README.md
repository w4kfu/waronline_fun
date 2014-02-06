# Warhammer Online Fun

## What is WOF ?

TODO

Set of tools to play with Warhammer Online 1.4.8.573

## Requirements

* [Python 2.7][python_2_7]
* [Python Protobuf][python_protobuf]

## Information about the files

* Doc : Folder containing full documentation
    * [Doc/LoginServiceProtocol.md](Doc/LoginServiceProtocol.md) : Documentation about protocol used by the
      login service
* Misc : Folder containing miscellaneous files
	* Misc/ProtoBuf : Contains all .proto files recovered/extracted from WAR.exe
	* Misc/WAR_RC4_test.py : python test script to test the weird RC4 implementation in Warhammer Online
	* Misc/SendWorldPacket_.md : Non exhaustive list of opcodes and handle RVA use for World Server
	* ...
* Toolz : Folder containing all toolz developped during the stud of the game
	* Toolz/IDAScript : A set of IDA python scripts to extract usefull informations
	* Toolz/injector : A simple DLL injector
	* Toolz/log_hash : A simple DLL to extract the hash associated with their filenames
	* Toolz/myp_extractor : MYP archive extractor
	* Toolz/replace_xml : DLL to change the content of mythloginserviceconfig.xml without modifying the archive data.myp
	* Toolz/server : A python server emulator for the game
	* ...

[python_2_7]: http://www.python.org/getit/
[python_protobuf]: https://developers.google.com/protocol-buffers/docs/pythontutorial
