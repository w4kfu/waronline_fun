#include "patcher_file.h"

#ifdef WINDOWS

struct PatcherFile *patcher_file_open(const char *filename)
{
    struct PatcherFile *file = NULL;

    if (filename == NULL)
        return NULL;
    file = malloc(sizeof (struct PatcherFile));
    if (file == NULL) {
        fprintf(stderr, "[-] patcher_file_open - malloc failed\n");
        return NULL;
    }
    memset(file, 0, sizeof (struct PatcherFile));
    strncpy_s(file->filename, FILENAME_MAX - 1, filename, FILENAME_MAX - 1);
    file->file = CreateFileA(filename, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    if (file->file == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "[-] patcher_file_open - CreateFileA failed\n");
        free(file);
        return NULL;
    }
    file->length = GetFileSize(file->file, NULL);
    file->map = CreateFileMapping(file->file, NULL, PAGE_READONLY, 0, 0, NULL);
    if (file->map == 0) {
        fprintf(stderr, "[-] patcher_file_open - CreateFileMapping failed\n");
        CloseHandle(file->file);
        free(file);
        return NULL;
    }
    file->buf = MapViewOfFile(file->map, FILE_MAP_READ, 0, 0, 0);
    if (file->buf == 0) {
        fprintf(stderr, "[-] patcher_file_open - CreateFileMapping failed\n");
        CloseHandle(file->map);
        CloseHandle(file->file);
        free(file);
        return NULL;
    }
    return file;
}

#else

struct PatcherFile *patcher_file_open(const char *filename)
{
    struct PatcherFile *file = NULL;
	struct stat st;

    if (filename == NULL)
        return NULL;
    file = malloc(sizeof (struct PatcherFile));
    if (file == NULL) {
        fprintf(stderr, "[-] patcher_file_open - malloc failed\n");
        return NULL;
    }
    memset(file, 0, sizeof (struct PatcherFile));
    strncpy(file->filename, filename, FILENAME_MAX - 1);
    file->fd = open(filename, O_RDONLY);
    if (file->fd == -1) {
        fprintf(stderr, "[-] patcher_file_open - open failed\n");
        free(file);
        return NULL;
    }
    if (fstat(file->fd, &st) == -1) {
        fprintf(stderr, "[-] patcher_file_open - fstat failed\n");
        close(file->fd);
        free(file);
        return NULL;
    }
    file->length = st.st_size;
    if ((file->buf = mmap (NULL, file->length, PROT_READ, MAP_PRIVATE, file->fd, 0)) == MAP_FAILED) {
        fprintf(stderr, "[-] patcher_file_open - fstat failed\n");
        close(file->fd);
        free(file);
        return NULL;
    }
    return file;
}

#endif

int patcher_file_read(struct PatcherFile *file, void *buf, size_t count)
{
    size_t length;

    if (buf == NULL)
        return 0;
    if (file->pos > file->length)
        return 0;
    if (count < (file->length - file->pos))
        length = count;
    else
        length = file->length - file->pos;
    if (length > 0) {
        memcpy(buf, file->buf + file->pos, length);
    }
    file->pos += length;
    return length;
}

int patcher_file_readline(struct PatcherFile *file, char *buf, size_t count)
{
    size_t length;
    char *newline = NULL;

    if (buf == NULL)
        return 0;
    if (file->pos > file->length)
        return 0;
    newline = strchr((const char*)(file->buf + file->pos), 0x0A);
    if (newline == NULL)
        return 0;
    length = (newline + 1) - (file->buf + file->pos);
    if (length > count)
        return 0;
    length = patcher_file_read(file, buf, length);
    buf[length] = 0x00;
    return length;
}

void patcher_file_seek(struct PatcherFile *file, unsigned int offset)
{
    if (offset > file->length)
        return;
    file->pos = offset;
}

int patcher_file_close(struct PatcherFile *file)
{
    if (file == NULL)
        return 0;
#ifdef WINDOWS
    CloseHandle(file->file);
    CloseHandle(file->map);
    UnmapViewOfFile(file->buf);
#else
    munmap(file->buf, file->length);
    close(file->fd);
#endif
    free(file);
    return 1;
}