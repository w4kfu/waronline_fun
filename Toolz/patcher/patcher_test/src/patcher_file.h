#ifndef PATCHER_FILE_H
#define PATCHER_FILE_H

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <sys/types.h>
#include <sys/stat.h>

#ifdef WINDOWS
#include <windows.h>
#else
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#endif

struct PatcherFile
{
    char filename[FILENAME_MAX];
    char *buf;
    unsigned int length;
    unsigned int pos;

#ifdef WINDOWS
    HANDLE file;
    HANDLE map;
#else
    int fd;
#endif
};

struct PatcherFile *patcher_file_open(const char *filename);
void patcher_file_info(const struct PatcherFile *file);

int patcher_file_read(struct PatcherFile *file, void *buf, size_t count);
int patcher_file_readline(struct PatcherFile *file, char *buf, size_t count);
void patcher_file_seek(struct PatcherFile *file, unsigned int offset);
int patcher_file_close(struct PatcherFile *file);

#endif /* PATCHER_FILE_H */