# .geom

Mythic geometry stored in thoses file.

Hash list can be found in [geom_hash_filelist.txt](geom_hash_filelist.txt).

## File Header Specification

    + 0x00 :       signature            [DWORD]
    + 0x04 :       version              [DWORD]
    + 0x08 :       file_size            [DWORD]
    + 0x0C :       unk_dword_00         [DWORD]         // CRC?
    + 0x10 :       nb_bones             [DWORD]
    + 0x14 :       offset_bones         [DWORD]
    + 0x18 :       nb_meshes            [DWORD]
    + 0x1C :       offset_meshes        [DWORD]

## Charmesh 2 obj

![result/result_geom2obj.png][1]

Problem: Wavefront .obj file doesn't support mesh vertex-colors, armatures, 
animation, lamps, camera, empty-objects, parenting or transformations.

[1]:result/result_geom2obj.png