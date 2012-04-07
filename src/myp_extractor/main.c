#include <stdio.h>
#include <Windows.h>

struct myp_header
{
	DWORD magic;
	DWORD version;
	DWORD byteorder;
	DWORD addr_filetable_LW;
	DWORD addr_filetable_HI;
	DWORD nb_file;
	DWORD all_nb_file;
	DWORD nb_filetable;
	DWORD nb_filetable2;
};

struct filetable_header
{
	DWORD nb_entry;
	DWORD offset_LW;
	DWORD offset_HI;
};

struct hash
{
   DWORD hi;
   DWORD lo;
};

#pragma pack(1)
struct file_entry
{
	DWORD offset_LW;
	DWORD offset_HI;
	DWORD unknow;
	DWORD cmp_size;
	DWORD ucmp_size;
	DWORD64 name;
	DWORD crc;
	WORD  compressed;
};

unsigned int hash_filename(char *buffer, int seed, unsigned int size);

int is_valid_myp(struct myp_header *hdr)
{
	if (hdr->magic == 0x0050594d)
		return (1);
	return (0);
}

void print_header_info(struct myp_header *hdr)
{
	printf("[+] Header Information\n");
	printf("MAGIC = 0x%X\n", hdr->magic);
	printf("Version = 0x%X\n", hdr->version);
	printf("Byte Order Marker = 0x%X\n", hdr->byteorder);
	printf("Address First FileTable Low = 0x%X\n", hdr->addr_filetable_LW);
	printf("Address First FileTable High = 0x%X\n", hdr->addr_filetable_HI);
	printf("Nb file inside First Table = 0x%X\n", hdr->nb_file);
	printf("Total file into archive = 0x%X\n", hdr->all_nb_file);
	printf("Nb FileTable = 0x%X\n", hdr->nb_filetable);
	printf("Nb FileTable = 0x%X (again?)\n", hdr->nb_filetable2);
	printf("\n");
}

void print_filetable(struct filetable_header *hdr)
{
	printf("[+] FileTable Information\n");
	printf("Nb Entry = 0x%X\n", hdr->nb_entry);
	printf("Offset Low = 0x%X\n", hdr->offset_LW);
	printf("Offset High = 0x%X\n", hdr->offset_HI);
	printf("\n");
}

void print_file_entry_info(struct file_entry *fe)
{
	printf("[+] FileEntry Information\n");
	printf("Offset Low = 0x%X\n", fe->offset_LW);
	printf("Offset High = 0x%X\n", fe->offset_HI);
	printf("Unknow = 0x%X\n", fe->unknow);
	printf("Compressed Size = 0x%X\n", fe->cmp_size);
	printf("Uncompressed Size = 0x%X\n", fe->ucmp_size);
	printf("Name = %I64X\n", fe->name);
	printf("CRC = 0x%X\n", fe->crc);
	printf("%s\n", fe->compressed ? "Is compressed" : "Is not compressed");
}

int main(void)
{
	HANDLE hFile;
	HANDLE	sFile;
	BYTE	*mFile;
	struct myp_header *hdr;
	struct filetable_header *hdrf;
	struct file_entry *fe;

	printf("Soze = %x\n", sizeof(struct file_entry));

	if ((hFile = CreateFileA("world.myp", GENERIC_READ, FILE_SHARE_READ, 0, OPEN_EXISTING, 0, 0)) == INVALID_HANDLE_VALUE)
	{
		printf("[-] CreateFileA() failed : %x\n", GetLastError());
		exit(EXIT_FAILURE);
	}
	sFile = CreateFileMappingA(hFile, 0, PAGE_READONLY, 0, 0, 0);
	mFile = (BYTE*)MapViewOfFile(sFile, FILE_MAP_READ, 0, 0, 0);
	if (!mFile)
	{
		printf("[-] MapViewOfFile() failed : %x\n", GetLastError());
		exit(EXIT_FAILURE);
	}

	hdr = (struct myp_header*)mFile;
	if (is_valid_myp(hdr))
	{
		print_header_info(hdr);
		hdrf = (struct filetable_header*)(mFile + hdr->addr_filetable_LW);
		print_filetable(hdrf);
		fe = (struct file_entry*)(mFile + hdr->addr_filetable_LW + sizeof(struct filetable_header));
		print_file_entry_info(fe);
	}
	else
		printf("[-] Magic number wrong\n");

	printf("%08X\n", hash_filename("Interface/InterfaceCore/InterfaceCorePreload.xml", 0x67520592, strlen("Interface/InterfaceCore/InterfaceCorePreload.xml")));

	UnmapViewOfFile(mFile);
	CloseHandle(sFile);
	CloseHandle(hFile);
	return (0);
}
