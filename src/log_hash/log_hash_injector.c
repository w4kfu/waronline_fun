#include <stdio.h>
#include <Windows.h>

/* War.exe require to be launch by warpatch.exe, because it initialize
some security token.
The idea is simple, we will launch warpatch.exe, and hook CreateProcessA
function, put the process in suspended state, inject the dll, and resume thread */

void create_warpatch_process(char *name, char *dll_name)
{
	STARTUPINFOA		si;
	PROCESS_INFORMATION pi;
	DWORD				Addr;
	HANDLE				hThread;
	HMODULE				hKernel32;

	hKernel32 = GetModuleHandleA("kernel32.dll");
	memset(&si, 0, sizeof(STARTUPINFO));
	si.cb = sizeof(STARTUPINFO);
	memset(&pi, 0, sizeof(PROCESS_INFORMATION));

	if (!CreateProcessA(name, 0, 0, 0, 0, CREATE_SUSPENDED, 0, 0, &si, &pi))
	{
		printf("[-] CreateProcessA() failed : %s is correct ? LastError : %x\n", name, GetLastError());
		exit(EXIT_FAILURE);
	}
	Addr = (DWORD)VirtualAllocEx(pi.hProcess, 0, strlen(dll_name) + 1, MEM_COMMIT, PAGE_READWRITE);
	if (Addr == NULL)
	{
		printf("[-] VirtualAllocEx failed(), LastError : %x\n", GetLastError());
		TerminateProcess(pi.hProcess, 42);
		exit(EXIT_FAILURE);
	}
	WriteProcessMemory(pi.hProcess, (LPVOID)Addr, (void*)dll_name, strlen(dll_name) + 1, NULL);
	hThread = CreateRemoteThread(pi.hProcess, NULL, 0,(LPTHREAD_START_ROUTINE) ::GetProcAddress(hKernel32,"LoadLibraryA" ), (LPVOID)Addr, 0, NULL);
	WaitForSingleObject(hThread, INFINITE);
	ResumeThread(pi.hThread);
	CloseHandle(hThread);
}


int main(void)
{
	create_warpatch_process("warpatch.exe", "log_hash.dll");
	return (0);
}