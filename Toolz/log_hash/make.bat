@cl.exe log_hash.c  /Ox /W3 /GF  /GA /MT /nologo /c /TC /D "_CRT_SECURE_NO_WARNINGS"
@link log_hash.obj /dll /release /MANIFEST:NO /MACHINE:IX86 /out:log_hash.dll


del *.obj
del *.exp

:end
pause