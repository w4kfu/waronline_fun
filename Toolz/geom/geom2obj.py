import sys
import geom_parser
    
def main():
    if len(sys.argv) != 2:
        print "Usage: %s <.geom>" % (sys.argv[0])
        sys.exit(1)
    geom = geom_parser.Geom(sys.argv[1])
    if geom.is_valid_geom() == False:
        sys.exit(1)
    geom_parser.print_geom_header(geom.header)
    fd_out = open("test.obj", "wb")
    bones = geom.get_bones()
    #for bone in bones:
    #    print_bones_data(bone)
    print len(bones)
    meshes = geom.get_meshes()
    fd_out.write("o test.y\n")
    nb_vertices = 0
    for mesh in meshes:
        for vertex in mesh['vertices']:
            fd_out.write("v %f %f %f\n" % (vertex['position_x'], vertex['position_y'], vertex['position_z']))
            fd_out.write("vn %f %f %f\n" % (vertex['normal_x'], vertex['normal_y'], vertex['normal_z']))
        for triangle in mesh['triangles']:
            fd_out.write("f %d %d %d\n" % (triangle['vertex_indice'][0] + 1 + nb_vertices, triangle['vertex_indice'][1] + 1 + nb_vertices, triangle['vertex_indice'][2] + 1 + nb_vertices))
        nb_vertices += mesh['nb_vertices']
    print len(meshes)
    fd_out.close()
    sys.exit(1)

if __name__ == "__main__":
    main()
