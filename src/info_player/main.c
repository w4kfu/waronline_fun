#include <windows.h>
#include <stdio.h>
#include <psapi.h>

#pragma comment(lib,"Psapi.lib")

void EnableDebugPriv(void)
{
	HANDLE hToken;
	LUID sedebugnameValue;
	TOKEN_PRIVILEGES tkp;

	if (!OpenProcessToken( GetCurrentProcess(),
		TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken ) )
		return;
	if (!LookupPrivilegeValue( NULL, SE_DEBUG_NAME, &sedebugnameValue ) ){
		CloseHandle( hToken );
		return;
	}
	tkp.PrivilegeCount = 1;
	tkp.Privileges[0].Luid = sedebugnameValue;
	tkp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
	if (!AdjustTokenPrivileges( hToken, FALSE, &tkp, sizeof tkp, NULL, NULL ) )
		CloseHandle( hToken );
}

int is_warhammer(DWORD pid)
{
	DWORD	cbNeeded;
	HANDLE	hProcess;
	HMODULE hMod;
	char	path[512];


	hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, 0, pid);
	if (hProcess == NULL)
	{
		fprintf(stderr, "[-] OpenProcess() failed : %d\n", GetLastError());
		return (0);
	}
	if (EnumProcessModules(hProcess, &hMod, sizeof(hMod), &cbNeeded))
	{
		if (GetModuleBaseNameA(hProcess, hMod, path, 512))
		{
			if (!strcmp(path, "WAR.exe"))
			{
				CloseHandle(hProcess);
				return (1);
			}
		}
	}
	CloseHandle(hProcess);
	return (0);
}

int get_warhammer_pid(void)
{
	DWORD	aProcesses[1024], cbNeeded, cProcesses;
	unsigned int i;

	if (!EnumProcesses(aProcesses, sizeof(aProcesses), &cbNeeded))
		return (0);
	cProcesses = cbNeeded / sizeof(DWORD);
	for (i = 0; i < cProcesses; i++)
	{
		if(aProcesses[i] != 0)
		{
			if (is_warhammer(aProcesses[i]))
			{
				return (aProcesses[i]);
			}
		}
	}
	printf("[-] Can't find warhammer online pid\n");
	exit(EXIT_FAILURE);
}

int main(void)
{
	EnableDebugPriv();
	printf("%d\n", get_warhammer_pid());
	return (0);
}