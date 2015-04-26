#include "patcher_test.h"

void hex_dump(const void *data, size_t size)
{
    unsigned char *p =(unsigned char*)data;
    unsigned char c;
    size_t n;
    char bytestr[4] = {0};
    char addrstr[10] = {0};
    char hexstr[16 * 3 + 5] = {0};
    char charstr[16 * 1 + 5] = {0};

    for(n = 1; n <= size; n++) {
        if (n % 16 == 1) {
            #ifdef WINDOWS
            sprintf_s(addrstr, sizeof (addrstr), "%.4x", (unsigned int)(p - (unsigned char*)data));
            #else
            snprintf(addrstr, sizeof (addrstr), "%.4x", (unsigned int)(p - (unsigned char*)data));
            #endif
        }
        c = *p;
        if (isalnum(c) == 0) {
            c = '.';
        }
        #ifdef WINDOWS
        sprintf_s(bytestr, sizeof (bytestr), "%02X ", *p);
        strncat_s(hexstr, sizeof (hexstr), bytestr, sizeof(hexstr) - strlen(hexstr) - 1);
        sprintf_s(bytestr, sizeof (bytestr), "%c", c);
        strncat_s(charstr, sizeof (charstr), bytestr, sizeof(charstr) - strlen(charstr) - 1);
        #else
        snprintf(bytestr, sizeof (bytestr), "%02X ", *p);
        strncat(hexstr, bytestr, sizeof(hexstr) - strlen(hexstr) - 1);
        snprintf(bytestr, sizeof (bytestr), "%c", c);
        strncat(charstr, bytestr, sizeof(charstr) - strlen(charstr) - 1);        
        #endif
        if (n % 16 == 0) {
            printf("[%4.4s]   %-50.50s  %s\n", addrstr, hexstr, charstr);
            hexstr[0] = 0;
            charstr[0] = 0;
        }
		else if (n % 8 == 0) {
            #ifdef WINDOWS
            strncat_s(hexstr, sizeof (hexstr), "  ", sizeof(hexstr) - strlen(hexstr) - 1);
            strncat_s(charstr, sizeof (charstr), " ", sizeof(charstr) - strlen(charstr) - 1);
            #else
            strncat(hexstr, "  ", sizeof(hexstr) - strlen(hexstr) - 1);
            strncat(charstr, " ", sizeof(charstr) - strlen(charstr) - 1);            
             #endif
        }
        p++;
    }
    if (strlen(hexstr) > 0) {
        printf("[%4.4s]   %-50.50s  %s\n", addrstr, hexstr, charstr);
    }
}

void compute_sha256(const char *buf, size_t size, unsigned char *sha256sum)
{
    sha256_context ctx;

    sha256_starts(&ctx);
    sha256_update(&ctx, (uint8 *)buf, size);
    sha256_finish(&ctx, sha256sum);
}

char *get_signature(struct PatcherFile *signature_file, int *signature_len)
{
    char line[0x200] = {0};
    char *signature = NULL;
    char *signature_end = NULL;

    if (patcher_file_readline(signature_file, line, sizeof (line)) == 0) {
        return NULL;
    }
    if (patcher_file_readline(signature_file, line, sizeof (line)) == 0) {
        return NULL;
    }
    signature = strstr(line, "v=\"");
    if (signature == NULL) {
        return NULL;
    }
    signature = signature + 3;
    signature_end = strstr(signature, "\" />");
    if (signature_end == NULL) {
        return NULL;
    }
    *(signature_end)= 0;
    signature_end = signature;
    *signature_len = Base64decode_len(signature);
    if (*signature_len == 0) {
        return NULL;
    }
    signature = (char*)calloc(*signature_len, sizeof (char));
    if (signature == NULL) {
        return NULL;
    }
    Base64decode(signature, signature_end);
    return signature;
}

int check_signature(unsigned char *signature, unsigned char *sha256sum)
{
    unsigned char patcher_rsa_n[129] = {
        0x02, 0x5D, 0x0D, 0xB8, 0xED, 0x5B, 0x04, 0xC0, 0x20, 0x4F, 0x7B, 0x07,
        0xEB, 0x0B, 0xC9, 0xCF, 0x85, 0xF6, 0xB1, 0xE0, 0x6B, 0x96, 0x05, 0x6D,
        0xF1, 0xD0, 0xFA, 0x47, 0x96, 0x53, 0x97, 0x72, 0x98, 0xDD, 0xA5, 0x72,
        0xA7, 0x43, 0x45, 0x40, 0xA5, 0xAB, 0xC7, 0x12, 0xA8, 0x4D, 0x2E, 0x5B,
        0xBA, 0x85, 0x4A, 0x1B, 0x82, 0x2D, 0x5F, 0xC6, 0x1D, 0x7A, 0x28, 0x93,
        0x5C, 0xFA, 0x64, 0xFE, 0x57, 0xAF, 0xB7, 0x54, 0x5B, 0xF7, 0x6A, 0xF9,
        0x38, 0xE2, 0xCB, 0xB0, 0x57, 0x36, 0xDE, 0x4C, 0xA8, 0x75, 0x5D, 0xB9,
        0x21, 0x3C, 0xC1, 0xC9, 0x4E, 0xD0, 0x8D, 0x1B, 0xDC, 0x49, 0xEB, 0xCB,
        0x9D, 0xA8, 0x46, 0x3E, 0x86, 0x12, 0x97, 0x18, 0x90, 0x42, 0xE3, 0xFB,
        0xE9, 0x5F, 0x37, 0xC1, 0x43, 0xBA, 0xDE, 0x8F, 0x91, 0xA5, 0xB1, 0xE6,
        0x36, 0x76, 0x90, 0x4C, 0xD9, 0xAA, 0xED, 0xEE, 0x1F
    };

    unsigned char patcher_rsa_e[3] = {
        0x01, 0x00, 0x01
    };
 
	mp_int mp_signature;
	mp_int mp_e;
	mp_int mp_n;

    int res;
    unsigned char buf[4096];
    
	if ((res = mp_init(&mp_signature)) != MP_OKAY) {
		fprintf(stderr, "[-] mp_init failed : %d\n", res);
		return 0;
	}
	if ((res = mp_init(&mp_e)) != MP_OKAY) {
		fprintf(stderr, "[-] mp_init failed : %d\n", res);
		return 0;
	}
	if ((res = mp_init(&mp_n)) != MP_OKAY) {
		fprintf(stderr, "[-] mp_init failed : %d\n", res);
		return 0;
	}    
    //printf("[+] signature_len : %d\n", signature_len - 4);
	if ((res = mp_read_unsigned_bin(&mp_signature, signature + 2, *(unsigned char*)(signature + 1))) != MP_OKAY) {
		fprintf(stderr, "[-] mp_read_unsigned_bin failed : %d\n", res);
		return 0;
	}
	if ((res = mp_read_unsigned_bin(&mp_n, patcher_rsa_n, sizeof (patcher_rsa_n))) != MP_OKAY) {
		fprintf(stderr, "[-] mp_read_unsigned_bin failed : %d\n", res);
		return 0;
	}
	if ((res = mp_read_unsigned_bin(&mp_e, patcher_rsa_e, sizeof (patcher_rsa_e))) != MP_OKAY) {
		fprintf(stderr, "[-] mp_read_unsigned_bin failed : %d\n", res);
		return 0;
	}
	if (mp_exptmod(&mp_signature, &mp_e, &mp_n, &mp_signature) != MP_OKAY) {
		fprintf(stderr, "[-] mp_exptmod failed\n");
		return 0;
	}    
	memset(buf, 0, sizeof (buf));
	mp_to_unsigned_bin(&mp_signature, buf);
    printf("[+] signature:\n");
	hex_dump(buf, mp_unsigned_bin_size(&mp_signature));
    printf("[+] sha256sum:\n");
    hex_dump(sha256sum, 32);
    return 1;
}

int main(void)
{
    struct PatcherFile *patcher_file = NULL;
    struct PatcherFile *signature_file = NULL;
    char *signature = NULL;
    int signature_len = 0;
    unsigned char sha256sum[32];

    patcher_file = patcher_file_open("patcher-goa.prod");
    if (patcher_file == NULL) {
        return -1;
    }
    signature_file = patcher_file_open("patcher-goa.prod.sig");
    if (signature_file == NULL) {
        return -1;
    }
    signature = get_signature(signature_file, &signature_len);
    if (signature == NULL) {
        return -1;
    }
    //hex_dump(signature, signature_len);
    compute_sha256(patcher_file->buf, patcher_file->length, sha256sum);
    //hex_dump(sha256sum, sizeof (sha256sum));
    check_signature((unsigned char*)signature, sha256sum);
    free(signature);
    patcher_file_close(patcher_file);
    patcher_file_close(signature_file);
    return 0;
}