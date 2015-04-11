# .geom

Mythic geometry stored in thoses file.

Hash list can be found in [geom_hash_filelist.txt](geom_hash_filelist.txt).

## Specification

### File Header 

    + 0x00 :       signature            [DWORD]         // 0x464c7367 'gsLF'
    + 0x04 :       version              [DWORD]
    + 0x08 :       file_size            [DWORD]
    + 0x0C :       unk_dword_00         [DWORD]         // CRC?
    + 0x10 :       nb_bones             [DWORD]
    + 0x14 :       offset_bones         [DWORD]
    + 0x18 :       nb_meshes            [DWORD]
    + 0x1C :       offset_meshes        [DWORD]
    
### Meshes

    + 0x00 :       unk_word_00          [WORD]
    + 0x02 :       nb_vertices          [WORD]
    + 0x04 :       offset_vertices      [DWORD]
    + 0x08 :       nb_triangles         [DWORD]
    + 0x0C :       offset_triangles     [DWORD]
    + 0x10 :       unk_dword_00         [DWORD]
    + 0x14 :       unk_dword_01         [DWORD]
    + 0x18 :       unk_dword_02         [DWORD]
    + 0x1C :       unk_dword_03         [DWORD]
    
Vertices (list of vertex data) are stored at offset (FileHeader->offset_meshes + Meshes->offset_vertices + num_meshes * sizeof (Meshes)).

### Vertex data
    
    + 0x00 :       position_x           [DWORD]
    + 0x04 :       position_y           [DWORD]
    + 0x08 :       position_z           [DWORD]
    + 0x0C :       normal_x             [DWORD]
    + 0x10 :       normal_y             [DWORD]
    + 0x14 :       normal_z             [DWORD]
    + 0x18 :       texture_u            [DWORD]
    + 0x1C :       texture_v            [DWORD]

### Triangles

    + 0x00 :       vertex_indice_1      [WORD]
    + 0x02 :       vertex_indice_2      [WORD]
    + 0x04 :       vertex_indice_3      [WORD]
    
## charmesh2obj.py

### Requirements

* [Python 2.7][python_2_7]
* [Python Construct][python_construct]

Convert .geom file to [Wavefront .obj file][wavefront] so
[blender][blender_software] (an open-source 3D computer graphics software) can import 
them!

### Screenshot

![result/result_geom2obj.png][1]

Problem: Wavefront .obj file doesn't support mesh vertex-colors, armatures, 
animation, lamps, camera, empty-objects, parenting or transformations.

[1]:result/result_geom2obj.png
[wavefront]: http://en.wikipedia.org/wiki/Wavefront_.obj_file
[blender_software]: http://www.blender.org/
[python_2_7]: http://www.python.org/getit/
[python_construct]: https://pypi.python.org/pypi/construct
