#include <stdio.h>
#include <Windows.h>

#pragma comment(lib, "LDE64.lib")

#define LDE_X86 0
#define FILE_DBG "dbg_replace_xml.txt"

#ifdef __cplusplus
    extern "C"
#endif
int __stdcall LDE(void* address , DWORD type);
DWORD (__stdcall *ResumeXML)(void) = NULL;
char default_ip_addr[32] = "127.0.0.1";

void DbgMsg(char *format, ...)
{
    char buffer[512];
    va_list args;
    FILE *fp = NULL;
    static int init_dbg = 0;

    va_start(args, format);
    memset(buffer, 0, sizeof (buffer));
    vsprintf_s(buffer, sizeof (buffer) - 1, format, args);
    if (!init_dbg) {
        fopen_s(&fp, FILE_DBG, "w");
        init_dbg = 1;
    }
    else {
        fopen_s(&fp, FILE_DBG, "a");
    }
    va_end(args);
    if (fp) {
        fprintf(fp, "%s", buffer);
    }
    fclose(fp);
}

BOOL SetupHook(char *module, char *name_export, void *Hook_func, void *trampo, DWORD addr)
{
	DWORD OldProtect;
	DWORD len = 0;
	FARPROC Proc;
	
	if (addr != 0) {
		Proc = (FARPROC)addr;
	}
	else {
		Proc = GetProcAddress(GetModuleHandleA(module), name_export);
		if (!Proc) {
			DbgMsg("[-] GetProcAddress() failed: %lu\n", GetLastError());
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

VOID ReplaceXML(char *Buffer)
{
	char FormatXML[] = "<?xml version=\"1.0\" encoding=\"utf-8\"?><RootElementOfAnyName><MythLoginServiceConfig>"
					 "<Settings><ProductId>2</ProductId><LogLevel>10</LogLevel><MessageTimeoutSecs>20</MessageTimeoutSecs>"
					 "</Settings><RegionList><Region regionName=\"WAR Live\"><PingServer serverName=\"None\">"
					 "<Address>0.0.0.0</Address><Port>0</Port></PingServer>"
					 "<LoginServerList><LoginServer serverName=\"login 1\">"
					 "<Address>%s</Address><Port>18046</Port>"
					 "</LoginServer>"
					 "</LoginServerList></Region>"
					 "</RegionList></MythLoginServiceConfig></RootElementOfAnyName>\x0A\x0A\x00\x00";
    char NewXML[540] = {0};                 
                     
    sprintf_s(NewXML, sizeof (NewXML) - 1, FormatXML, default_ip_addr);
	memcpy(Buffer, NewXML, sizeof (NewXML));				 
}

DWORD __declspec (naked) HookXML(VOID)
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
		jmp     ResumeXML
	}
}

VOID MakeHook(VOID)
{
	ResumeXML = (DWORD(__stdcall *)(VOID))VirtualAlloc(0, 0x1000, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	memset(ResumeXML, 0x90, 0x1000);
	/*
        .text:004ACF6F                 mov     ecx, [eax]
        .text:004ACF71                 mov     edi, ecx
        .text:004ACF73                 add     esp, 0Ch
        .text:004ACF76                 mov     [eax], ebx
	*/
	SetupHook("WAR", "WAR", &HookXML, ResumeXML, 0x004ACF6F);
}

VOID LoadServerIp(VOID)
{
    FILE *fp = NULL;
    char buffer[512] = {0};
    int ipbytes[4];
    
    fopen_s(&fp, "server_ip.txt", "r");
    if (fp == NULL) {
        DbgMsg("[+] server_ip.txt not found using default value ip address: %s\n", default_ip_addr);
        return;
    }
    fread(buffer, 1, 15, fp);
    if (sscanf_s(buffer, "%3d.%3d.%3d.%3d", &ipbytes[3], &ipbytes[2], &ipbytes[1], &ipbytes[0]) != 4) {
        DbgMsg("[-] Malformated ip in server_ip.txt\n");
        fclose(fp);
        return;
    }
    sprintf_s(default_ip_addr, sizeof (default_ip_addr) - 1, "%s", buffer);
    DbgMsg("[+] server_ip.txt found! new default value ip address is : %s\n", default_ip_addr);
    fclose(fp);
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
    switch(fdwReason) {
        case DLL_PROCESS_ATTACH:
            DisableThreadLibraryCalls(GetModuleHandleA(NULL));
            MakeHook();
            LoadServerIp();
            break;
        default:
            break;
	}
	return TRUE;
}