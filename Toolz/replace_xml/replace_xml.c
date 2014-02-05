#include <stdio.h>
#include <Windows.h>

#pragma comment(lib, "LDE64.lib")

#define LDE_X86 0
#define FILE_DBG "dbg_log_hash_msg.txt"

#ifdef __cplusplus
extern "C"
#endif
int __stdcall LDE(void* address , DWORD type);

int init_dbg = 0;

void dbg_msg(char *format, ...)
{
  char buffer[512];
  va_list args;
  FILE *fp = NULL;

  va_start(args, format);
  memset(buffer, 0, sizeof (buffer));
  vsprintf(buffer, format, args);
  if (!init_dbg)
  {
		fp = fopen(FILE_DBG, "w");
		init_dbg = 1;
  }
  else
  {
		fp = fopen(FILE_DBG, "a");
  }
  va_end(args);
  fprintf(fp, "%s", buffer);
  fclose(fp);
}

BOOL setup_hook(char *module, char *name_export, void *Hook_func, void *trampo, DWORD addr)
{
	DWORD OldProtect;
	DWORD len = 0;
	FARPROC Proc;
	
	if (addr != 0)
	{
		Proc = (FARPROC)addr;
	}
	else
	{
		Proc = GetProcAddress(GetModuleHandleA(module), name_export);
		if (!Proc)
		{
			dbg_msg("[-] GetProcAddress()\n");
			return FALSE;
		}
	}
	while (len < 5)
		len += LDE((BYTE*)Proc + len , LDE_X86);
	memcpy(trampo, Proc, len);
	*(BYTE*)((BYTE*)trampo + len) = 0xE9;
	*(DWORD*)((BYTE*)trampo + len + 1) = (BYTE*)Proc - (BYTE*)trampo - 5;
	VirtualProtect(Proc, len, PAGE_EXECUTE_READWRITE, &OldProtect);
	*(BYTE*)Proc = 0xE9;
	*(DWORD*)((char*)Proc + 1) = (BYTE*)Hook_func - (BYTE*)Proc - 5;
	VirtualProtect(Proc, len, OldProtect, &OldProtect);
	return TRUE;
}

DWORD (__stdcall *Resume_xml)(void) = NULL;

VOID	ReplaceXML(char *Buffer)
{
	char new_xml[] = "<?xml version=\"1.0\" encoding=\"utf-8\"?><RootElementOfAnyName><MythLoginServiceConfig>"
					 "<Settings><ProductId>2</ProductId><MessageTimeoutSecs>20</MessageTimeoutSecs>"
					 "</Settings><RegionList><Region regionName=\"WAR Live\"><PingServer serverName=\"None\">"
					 "<Address>0.0.0.0</Address><Port>0</Port></PingServer>"
					 "<LoginServerList><LoginServer serverName=\"login 1\">"
					 "<Address>127.0.0.1</Address><Port>18046</Port>"
					 "</LoginServer>"
					 //<LoginServer serverName=\"login 2\">"
					 //"<Address>127.0.0.1</Address><Port>18047</Port>"
					 //"</LoginServer>"
					 "</LoginServerList></Region>"
					 "</RegionList></MythLoginServiceConfig></RootElementOfAnyName>\x0A\x0A\x00\x00";
					 
	memcpy(Buffer, new_xml, sizeof (new_xml));				 
}

DWORD __declspec ( naked ) Hook_xml(void)
{
	__asm
	{
		pushad
		mov		eax, [eax]
		add		eax, 18h
		mov		eax, [eax]
		push	eax
		call	ReplaceXML
		add		esp, 4
		popad
		jmp Resume_xml
	}
}

void Make_Hook(void)
{
	Resume_xml = (DWORD(__stdcall *)(void))VirtualAlloc(0, 0x1000, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	memset(Resume_xml, 0x90, 0x1000);
	/*
.text:004ACF6F                 mov     ecx, [eax]
.text:004ACF71                 mov     edi, ecx
.text:004ACF73                 add     esp, 0Ch
.text:004ACF76                 mov     [eax], ebx
	*/
	setup_hook("WAR", "WAR", &Hook_xml, Resume_xml, 0x004ACF6F);
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
	switch(fdwReason)
	{
		case DLL_PROCESS_ATTACH:
			DisableThreadLibraryCalls(GetModuleHandleA(NULL));
			Make_Hook();
			break;
		default:
			break;
	}
	return TRUE;
}