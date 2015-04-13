# .diffuse

## Specification

### File Header 

    + 0x00 :       signature            [DWORD]         // 0x464C6469 'idLF' / 'FLdi'
    + 0x04 :       version              [DWORD]
    + 0x08 :       file_size            [DWORD]
    + 0x0C :       unk_dword_00         [DWORD]         // CRC?
    + 0x10 :       mipmap_width_max     [WORD]
    + 0x12 :       mipmap_height_max    [WORD]
    + 0x14 :       num_mipmaps          [DWORD]