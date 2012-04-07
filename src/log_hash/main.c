#include <stdio.h>
#include <Windows.h>

/* War.exe require to be launch by warpatch.exe, because it initialize
some security token.
The idea is simple, we will launch warpatch.exe, and hook CreateProcessA
function, put the process in suspended state, inject the dll, and resume thread */

int main(void)
{

	return (0);
}