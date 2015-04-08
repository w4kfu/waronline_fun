#include <stdio.h>
#include <Windows.h>

#pragma comment(lib, "LDE64.lib")

#define LDE_X86 0
#define FILE_DBG "dbg_log_hash_msg.txt"

#ifdef __cplusplus
extern "C"
#endif
int __stdcall LDE(void* address , DWORD type);

void dbg_msg(char *format, ...)
{
	static int init = 0;
    char buffer[512];
    va_list args;
    FILE *fp = NULL;

    va_start(args, format);
    memset(buffer, 0, sizeof (buffer));
    vsprintf_s(buffer, 512, format, args);
    //EnterCriticalSection(&CriticalSection);
    if (!init) {
        fopen_s(&fp, FILE_DBG, "w");
        init = 1;
    }
    else {
        fopen_s(&fp, FILE_DBG, "a");
    }
    va_end(args);
    if (fp != NULL) {
        fprintf(fp, "%s", buffer);
        fclose(fp);
    }
    printf("%s", buffer);
    //LeaveCriticalSection(&CriticalSection);
}

void hexdump(void *data, int size)
{
    unsigned char *p = (unsigned char*)data;
    unsigned char c;
    int n;
    char bytestr[4] = {0};
    char addrstr[10] = {0};
    char hexstr[16 * 3 + 5] = {0};
    char charstr[16 * 1 + 5] = {0};

    for (n = 1; n <= size; n++) {
        if (n % 16 == 1) {
            sprintf_s(addrstr, sizeof(addrstr), "%.4x", ((unsigned int)p - (unsigned int)data));
        }
        c = *p;
        if (isprint(c) == 0) {
            c = '.';
        }
        sprintf_s(bytestr, sizeof(bytestr), "%02X ", *p);
        strncat_s(hexstr, sizeof(hexstr), bytestr, sizeof(hexstr) - strlen(hexstr) - 1);
        sprintf_s(bytestr, sizeof(bytestr), "%c", c);
        strncat_s(charstr, sizeof(charstr), bytestr, sizeof(charstr) - strlen(charstr) - 1);
        if (n % 16 == 0) {
            dbg_msg("[%4.4s]   %-50.50s  %s\n", addrstr, hexstr, charstr);
            hexstr[0] = 0;
            charstr[0] = 0;
        }
        else if (n % 8 == 0) {
            strncat_s(hexstr, sizeof(hexstr), "  ", sizeof(hexstr)-strlen(hexstr)-1);
        }
        p++;
    }
    if (strlen(hexstr) > 0) {
        dbg_msg("[%4.4s]   %-50.50s  %s\n", addrstr, hexstr, charstr);
    }
}

VOID MakeConsole(VOID)
{
	DWORD dwMode;
	struct _CONSOLE_SCREEN_BUFFER_INFO sbi;
	HANDLE hStd;
	FILE *fStream;
  
	AllocConsole();
	hStd = GetStdHandle(STD_INPUT_HANDLE);
	GetConsoleMode(hStd, (LPDWORD)&dwMode);
	SetConsoleMode(hStd, dwMode & 0xFFFFFFEF);
	GetConsoleScreenBufferInfo(hStd, &sbi);
	sbi.dwSize.Y = 500;
	SetConsoleScreenBufferSize(hStd, sbi.dwSize);
	freopen_s(&fStream, "conin$", "r", stdin);
	freopen_s(&fStream, "conout$", "w", stdout);
	freopen_s(&fStream, "conout$", "w", stderr);
}

BOOL setup_hook(char *module, char *name_export, void *Hook_func, void *trampo, DWORD addr)
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

VOID Loglol(LPCSTR a, PVOID b, PDWORD c, PDWORD d)
{
    if (strstr(a, ".")) {
        //dbg_msg("[+] a = %s\n", a);
        dbg_msg("%s\n", a);
    }
    //dbg_msg("[+] a = %s ; b = %08X ; c = %08X (%08X) ; d = %08X (%08X)\n", (char*)a, b, c, *c, d, *d);
}

DWORD __declspec ( naked ) Hook_hash(void)
{
	__asm
	{
		pushad
        mov     eax, dword ptr [esp + 0x24]
        mov     ebx, dword ptr [esp + 0x28]
        mov     ecx, dword ptr [esp + 0x2C]
        mov     edx, dword ptr [esp + 0x30]
        push    edx
        push    ecx
        push    ebx
        push    eax
		//mov 	eax, dword ptr [esp + 0x34]
		//mov 	ebx, dword ptr [esp + 0x30]
		//push	ebx
		//push	edi
		//push	ecx
		//push	eax
        //push    [ebp + 0x
		//call	MyLogHash
        call    Loglol
		add		esp, 10h
		popad
		jmp     Resume_hash
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
    
    /*
    .text:00752A47 55                      push    ebp
    .text:00752A48 8B EC                   mov     ebp, esp
    .text:00752A4A 51                      push    ecx
    .text:00752A4B 8B 4D 10                mov     ecx, [ebp+a
    */
    
    /*
    .text:00752C53 89 38                   mov     [eax], edi
    .text:00752C55 5F                      pop     edi
    .text:00752C56 5E                      pop     esi
    .text:00752C57 5B                      pop     ebx
    .text:00752C58 C9                      leave
    .text:00752C59 C3                      retn
    */
	setup_hook("WAR", "WAR", &Hook_hash, Resume_hash, 0x00752A47);
    //setup_hook("WAR", "WAR", &Hook_hash, Resume_hash, 0x0075280F);
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
	switch(fdwReason)
	{
		case DLL_PROCESS_ATTACH:
			DisableThreadLibraryCalls(GetModuleHandleA(NULL));
			MakeConsole();
            Make_Hook();
			break;
		default:
			break;
	}
	return TRUE;
}