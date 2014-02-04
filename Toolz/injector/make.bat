@cl.exe injector.c /W3 /GF /GS- /GA /MT /nologo /c /TC /D_CRT_SECURE_NO_WARNINGS
@link injector.obj /release /subsystem:console /out:war_injector.exe /MACHINE:IX86 /BASE:0x400000 /MANIFEST:NO  /merge:.rdata=.text /DYNAMICBASE:NO

del *.obj
del *.exp

pause