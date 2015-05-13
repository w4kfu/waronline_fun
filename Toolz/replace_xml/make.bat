@cl.exe replace_xml.c  /Ox /W3 /GF /GA /MT /nologo /c /TC
@link replace_xml.obj /dll /release /MANIFEST:NO /MACHINE:IX86 /out:replace_xml.dll

del *.obj
del *.exp

:end
pause