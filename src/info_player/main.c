#include <windows.h>
#include <stdio.h>
#include <psapi.h>

#pragma comment(lib,"Psapi.lib")

#define PTR_STRUCT_PLAYER 0x00F7512C

struct info_s
{
	DWORD pid;
	HANDLE hProcess;
	DWORD addr_splayer;
};

struct player_s
{
	int X;
	int Y;
	int Z;
};

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
		return (0);
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
	struct info_s info;
	struct player_s player;
	DWORD nbread;

	EnableDebugPriv();
	
	info.pid = get_warhammer_pid();
	info.hProcess = OpenProcess(PROCESS_ALL_ACCESS, 0, info.pid);
	if (info.hProcess == NULL)
	{
		printf("[-] OpenProcess() failed : %d\n", GetLastError());
		exit(EXIT_FAILURE);
	}

	ReadProcessMemory(info.hProcess, (LPVOID)PTR_STRUCT_PLAYER, &info.addr_splayer, 4, &nbread);
	if (nbread != 4)
	{
		printf("[-] ReadProcessMemory() failed : %d\n", GetLastError());
		exit(EXIT_FAILURE);
	}
	ReadProcessMemory(info.hProcess, (LPVOID)(info.addr_splayer + 0x24), &player, 4 * 3, &nbread);
	printf("X = %X\n", player.X);
	printf("Y = %X\n", player.Y);
	printf("Z = %X\n", player.Z);
	system("pause");
	return (0);
}