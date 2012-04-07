#include    <windows.h>
#include    <stdio.h>

#define		LDE_X86			0
#define		LDE_X64			64
#define		UNKNOWN_OPCODE	-1

#ifdef __cplusplus
extern "C"
#endif
int __stdcall LDE(void* address , DWORD type);

#pragma comment(lib, "LDE64.lib")

void	setup_hook(char *module, char *name_export, void *Hook_func, void *trampo)
{
	DWORD	OldProtect;
	DWORD	len;
	FARPROC	Proc;

	Proc = GetProcAddress(GetModuleHandleA(module), name_export);
	if (!Proc)
		MessageBoxA(NULL, name_export, module, 0);
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

BOOL (__stdcall *Resume_CreateProcess)(LPCSTR, LPSTR, LPSECURITY_ATTRIBUTES, LPSECURITY_ATTRIBUTES,
										BOOL, DWORD, LPVOID, LPCSTR, LPSTARTUPINFOA, LPPROCESS_INFORMATION) = NULL;

BOOL __stdcall Hook_CreateProcess(LPCSTR lpApplicationName,
									LPSTR lpCommandLine,
									LPSECURITY_ATTRIBUTES lpProcessAttributes,
									LPSECURITY_ATTRIBUTES lpThreadAttributes,
									BOOL bInheritHandles,
									DWORD dwCreationFlags,
									LPVOID lpEnvironment,
									LPCSTR lpCurrentDirectory,
									LPSTARTUPINFOA lpStartupInfo,
									LPPROCESS_INFORMATION lpProcessInformation)
{
	BOOL result;

	dwCreationFlags = CREATE_SUSPENDED;
	result = Resume_CreateProcess(lpApplicationName, lpCommandLine, lpProcessAttributes, 
						lpThreadAttributes, bInheritHandles, dwCreationFlags,
						lpEnvironment, lpCurrentDirectory, lpStartupInfo, lpProcessInformation);
	return (result);
}

void setup_hook_create_process(void)
{
	Resume_CreateProcess = (BOOL(__stdcall *)(LPCSTR, LPSTR, LPSECURITY_ATTRIBUTES, LPSECURITY_ATTRIBUTES,
										BOOL, DWORD, LPVOID, LPCSTR, LPSTARTUPINFOA, LPPROCESS_INFORMATION))VirtualAlloc(0, 0x1000, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	memset(Resume_CreateProcess, 0x90, 0x1000);
	setup_hook("kernel32.dll", "CreateProcessA", &Hook_CreateProcess, Resume_CreateProcess);
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved)
{
	char name[256];

	if (fdwReason == DLL_PROCESS_DETACH)
		return (0);

	DisableThreadLibraryCalls(GetModuleHandleA("log_hash_dll"));
	GetModuleFileNameA(GetModuleHandleA(NULL), (LPSTR)name, 256);
	if (strstr(name, "warpatch.exe"))
	{
		setup_hook_create_process();
		MessageBoxA(NULL, (LPCSTR)name, (LPCSTR)name, 0);
	}
	return (0);
}