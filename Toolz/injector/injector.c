#include <stdio.h>
#include <Windows.h>

void create_warpatch_process(int argc, char **dll_name)
{
	int i;
	STARTUPINFOA		si;
	PROCESS_INFORMATION pi;
	PVOID				Addr;
	HANDLE				hThread;
	HMODULE				hKernel32;
	LPSTR 				cmdArgs = "war.exe --acctname=U1VDRQ== --sesstoken=U1VDRQ==";

	hKernel32 = GetModuleHandleA("kernel32.dll");
	memset(&si, 0, sizeof(STARTUPINFO));
	si.cb = sizeof(STARTUPINFO);
	memset(&pi, 0, sizeof(PROCESS_INFORMATION));

	if (!CreateProcessA("war.exe", cmdArgs, 0, 0, 0, CREATE_SUSPENDED, 0, 0, &si, &pi))
	{
		printf("[-] CreateProcessA() failed : is correct ? LastError : %x\n", GetLastError());
		exit(EXIT_FAILURE);
	}
	for (i = 0; i < argc; i++)
	{
		Addr = (PVOID)VirtualAllocEx(pi.hProcess, 0, strlen(dll_name[i + 1]) + 1, MEM_COMMIT, PAGE_READWRITE);
		if (Addr == NULL)
		{
			printf("[-] VirtualAllocEx failed(), LastError : %x\n", GetLastError());
			TerminateProcess(pi.hProcess, 42);
			exit(EXIT_FAILURE);
		}
		WriteProcessMemory(pi.hProcess, Addr, (void*)dll_name[i + 1], strlen(dll_name[i + 1]) + 1, NULL);
		hThread = CreateRemoteThread(pi.hProcess, NULL, 0,
					(LPTHREAD_START_ROUTINE)GetProcAddress(hKernel32, "LoadLibraryA"), 
					(LPVOID)Addr, 0, NULL);
		WaitForSingleObject(hThread, INFINITE);
	}
	ResumeThread(pi.hThread);
	CloseHandle(hThread);
}


int main(int argc, char **argv)
{
	PVOID OldValue = NULL;

	if (argc < 2)
	{
		printf("Usage : %s <dll_name.dll>\n", argv[0]);
		exit(EXIT_FAILURE);
	}
	Wow64DisableWow64FsRedirection(&OldValue);
	create_warpatch_process(argc - 1, argv);
	return 0;
}