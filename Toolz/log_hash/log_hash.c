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

DWORD (__stdcall *Resume_hash)(void) = NULL;

char	*format_hash = "[+] \"%s\" = %08X%08X\n";

VOID	MyLogHash(char *Filename, DWORD dwHash_High, DWORD dwHash_Low, DWORD dwRetAddr)
{
	//if (!strncmp(Filename, "data", 4))
	//{
		dbg_msg("[+] \"%s\" = %08X%08X (dwRetAddr = %08X)\n", Filename, dwHash_High, dwHash_Low, dwRetAddr);
		if (!strcmp(Filename, "data/mythloginserviceconfig.xml"))
		{
			/*__asm
			{
				jmp $
			}*/
		}
	//}
}

DWORD __declspec ( naked ) Hook_hash(void)
{
	__asm
	{
		pushad
		mov 	eax, dword ptr [esp + 0x34]
		mov 	ebx, dword ptr [esp + 0x30]
		push	ebx
		push	edi
		push	ecx
		push	eax
		call	MyLogHash
		add		esp, 10h
		popad
		jmp Resume_hash
	}
}

void Make_Hook(void)
{
	Resume_hash = (DWORD(__stdcall *)(void))VirtualAlloc(0, 0x1000, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	memset(Resume_hash, 0x90, 0x1000);
	/*
.text:0099492D                 pop     edi
.text:0099492E                 pop     esi
.text:0099492F                 pop     ebp
.text:00994930                 mov     [eax], ecx
.text:00994932                 pop     ebx
.text:00994933                 retn
	*/
	setup_hook("WAR", "WAR", &Hook_hash, Resume_hash, 0x0099492D);
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