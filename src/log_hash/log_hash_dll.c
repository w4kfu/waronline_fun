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
						lpEnvironment, lpCurrentDirectory, lpStartupInfo, lpProcessInformation);
	Addr = (DWORD)VirtualAllocEx(lpProcessInformation->hProcess, 0, strlen(DLL_NAME) + 1, MEM_COMMIT, PAGE_READWRITE);
	if (Addr == NULL)
	{
		MessageBoxA(NULL, "VirtualAllocEx failed()", "Error", 0);
		TerminateProcess(lpProcessInformation->hProcess, 42);
		exit(EXIT_FAILURE);
	}
	WriteProcessMemory(lpProcessInformation->hProcess, (LPVOID)Addr, (void*)DLL_NAME, strlen(DLL_NAME) + 1, NULL);
	hThread = CreateRemoteThread(lpProcessInformation->hProcess, NULL, 0,(LPTHREAD_START_ROUTINE) ::GetProcAddress(hKernel32,"LoadLibraryA" ), (LPVOID)Addr, 0, NULL);
	WaitForSingleObject(hThread, INFINITE);
	ResumeThread(lpProcessInformation->hThread);
	CloseHandle(hThread);
	return (result);
}

void setup_hook_create_process(void)
{
	/* Alloc enough place for CreateProcess Hook */
	Resume_CreateProcessW = (DWORD(__stdcall *)(LPCWSTR, LPWSTR, LPSECURITY_ATTRIBUTES, 
												LPSECURITY_ATTRIBUTES, BOOL, DWORD, LPVOID, 
												LPCWSTR, LPSTARTUPINFOW, LPPROCESS_INFORMATION))
												VirtualAlloc(0, 0x1000, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	if (!Resume_CreateProcessW)
	{
		MessageBoxA(NULL, "VirtualAllocEx failed()", "Error", 0);
	}
	memset(Resume_CreateProcessW, 0x90, 0x1000);
	setup_hook("kernel32.dll", "CreateProcessW", &Hook_CreateProcessW, Resume_CreateProcessW);
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved)
{
	char name[256];

	if (fdwReason == DLL_PROCESS_DETACH)
		return (FALSE);
	if (fdwReason == DLL_PROCESS_ATTACH)
	{
		//DisableThreadLibraryCalls(GetModuleHandleA(DLL_NAME));
		GetModuleFileNameA(GetModuleHandleA(NULL), (LPSTR)name, 256);
		/* If dll has been injected into warpatch.exe we need to inject it into warpatch.bin */
		if (strstr(name, "warpatch.exe"))
		{
			setup_hook_create_process();
		}
		if (strstr(name, "warpatch.bin"))
		{
		//setup_hook_create_process();
		MessageBoxA(NULL, "WUT", "WUT", 0);
		}
	}
	return (TRUE);
}