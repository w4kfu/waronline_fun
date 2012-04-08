#include    <windows.h>
#include    <stdio.h>

#define		LDE_X86			0
#define		LDE_X64			64
#define		UNKNOWN_OPCODE	-1
#define		DLL_NAME		"log_hash_dll.dll"

#ifdef __cplusplus
extern "C"
#endif
int __stdcall LDE(void* address , DWORD type);

#pragma comment(lib, "LDE64.lib")

DWORD	hash_low;
DWORD	hash_high;
char	*str;
FILE	*hfile;

void	setup_hook(char *module, char *name_export, void *Hook_func, void *trampo, DWORD addr)
{
	DWORD	OldProtect;
	DWORD	len;
	FARPROC	Proc;

	if (addr != 0)
	{
		Proc = (FARPROC)addr;
	}
	else
	{
		Proc = GetProcAddress(GetModuleHandleA(module), name_export);
		if (!Proc)
			MessageBoxA(NULL, name_export, module, 0);
	}
	len = 0;
	while (len < 5)
		len += LDE((BYTE*)Proc + len , LDE_X86);
	memcpy(trampo, Proc, len);
	*(BYTE *)((BYTE*)trampo + len) = 0xE9;
	*(DWORD *)((BYTE*)trampo + len + 1) = (BYTE*)Proc - (BYTE*)trampo - 5;
	VirtualProtect(Proc, len, PAGE_EXECUTE_READWRITE, &OldProtect);
	*(BYTE*)Proc = 0xE9;
	*(DWORD*)((char*)Proc + 1) = (BYTE*)Hook_func - (BYTE*)Proc - 5;
	VirtualProtect(Proc, len, OldProtect, &OldProtect);
}

DWORD (__stdcall *Resume_hash)(void) = NULL;

DWORD __declspec ( naked ) Hook_hash(void)
{
	__asm
	{
		pushad
		mov hash_high, ecx
		mov hash_low, edi
		/* 
			debug :] 
			__asm jmp $
		*/
		mov eax, dword ptr [esp + 0x34]
		mov str, eax
	}
	hfile = fopen("log_hash.txt", "a");
	if (hfile)
	{
		fprintf(hfile, "\"%s\" = %08X%08X\n", str, hash_high, hash_low);
		fclose(hfile);
	}
	__asm
	{
		popad
		jmp Resume_hash
	}
}

DWORD (__stdcall *Resume_CreateProcessW)(LPCWSTR, LPWSTR, LPSECURITY_ATTRIBUTES, 
					LPSECURITY_ATTRIBUTES,
					BOOL, DWORD, LPVOID, LPCWSTR, 
					LPSTARTUPINFOW, LPPROCESS_INFORMATION) = NULL;

/* This hook will inject again the dll in the other process */
DWORD __stdcall Hook_CreateProcessW(LPCWSTR lpApplicationName,
					LPWSTR lpCommandLine,
					LPSECURITY_ATTRIBUTES lpProcessAttributes,
					LPSECURITY_ATTRIBUTES lpThreadAttributes,
					BOOL bInheritHandles,
					DWORD dwCreationFlags,
					LPVOID lpEnvironment,
					LPCWSTR lpCurrentDirectory,
					LPSTARTUPINFOW lpStartupInfo,
					LPPROCESS_INFORMATION lpProcessInformation)
{
	BOOL result;
	DWORD	Addr;
	HANDLE	hThread;
	HMODULE	hKernel32;

	hKernel32 = GetModuleHandleA("kernel32.dll");
	/* Change Creation flag to CREATE_SUSPENDED */
	dwCreationFlags = CREATE_SUSPENDED;
	/* Call real CreateProcess function */
	result = Resume_CreateProcessW(lpApplicationName, lpCommandLine, lpProcessAttributes, 
					lpThreadAttributes, bInheritHandles, dwCreationFlags,
					lpEnvironment, lpCurrentDirectory, lpStartupInfo, 
					lpProcessInformation);
	Addr = (DWORD)VirtualAllocEx(lpProcessInformation->hProcess, 0, strlen(DLL_NAME) + 1, 
					MEM_COMMIT, PAGE_READWRITE);
	if (Addr == NULL)
	{
		MessageBoxA(NULL, "VirtualAllocEx failed()", "Error", 0);
		TerminateProcess(lpProcessInformation->hProcess, 42);
		exit(EXIT_FAILURE);
	}
	WriteProcessMemory(lpProcessInformation->hProcess, (LPVOID)Addr, (void*)DLL_NAME, strlen(DLL_NAME) + 1, NULL);
	hThread = CreateRemoteThread(lpProcessInformation->hProcess, NULL, 0,
					(LPTHREAD_START_ROUTINE) ::GetProcAddress(hKernel32,"LoadLibraryA" ), 
					(LPVOID)Addr, 0, NULL);
	WaitForSingleObject(hThread, INFINITE);
	ResumeThread(lpProcessInformation->hThread);
	CloseHandle(hThread);
	return (result);
}

void setup_hook_create_processw(void)
{
	/* Alloc enough place for CreateProcess Hook */
	Resume_CreateProcessW = (DWORD(__stdcall *)(LPCWSTR, LPWSTR, LPSECURITY_ATTRIBUTES, 
							LPSECURITY_ATTRIBUTES, BOOL, DWORD, LPVOID, 
							LPCWSTR, LPSTARTUPINFOW, LPPROCESS_INFORMATION))
							VirtualAlloc(0, 0x1000, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	if (!Resume_CreateProcessW)
	{
		MessageBoxA(NULL, "VirtualAllocEx failed()", "Error", 0);
		return;
	}
	memset(Resume_CreateProcessW, 0x90, 0x1000);
	setup_hook("kernel32.dll", "CreateProcessW", &Hook_CreateProcessW, Resume_CreateProcessW, 0);
}

void setup_hook_hash(void)
{
	Resume_hash = (DWORD(__stdcall *)(void))VirtualAlloc(0, 0x1000, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	memset(Resume_hash, 0x90, 0x1000);
	/*
	.text:0099485D                 pop     edi
	.text:0099485E                 pop     esi
	.text:0099485F                 pop     ebp
	.text:00994860                 mov     [eax], ecx
	.text:00994862                 pop     ebx
	.text:00994863                 retn
	*/
	setup_hook("WAR", "WAR", &Hook_hash, Resume_hash, 0x0099485D);
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved)
{
	char name[256];

	if (fdwReason == DLL_PROCESS_DETACH)
		return (TRUE);
	if (fdwReason == DLL_PROCESS_ATTACH)
	{
		DisableThreadLibraryCalls(GetModuleHandleA(DLL_NAME));
		GetModuleFileNameA(GetModuleHandleA(NULL), (LPSTR)name, 256);
		/* If dll has been injected into warpatch.exe we need to inject it into warpatch.bin */
		if (strstr(name, "warpatch.exe"))
		{
			setup_hook_create_processw();
		}
		/* If dll has been injected into warpatch.bin we need to inject it into WAR.exe */
		else if (strstr(name, "warpatch.bin"))
		{
			setup_hook_create_processw();
		}
		else if (strstr(name, "WAR.exe"))
		{
			setup_hook_hash();
		}
	}
	return (TRUE);
}
