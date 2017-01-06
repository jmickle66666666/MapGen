import omg
import drawmap
from shape import Shape

def test_square_map():
    # return a new mapedit object with a small square room
    output = omg.mapedit.MapEditor()
    shape = Shape()
    shape.add_vertex(0,0)
    shape.add_vertex(128,0)
    shape.add_vertex(128,128)
    shape.add_vertex(0,128)
    shape.write_to_map(output)
    return output

def test_concave_map():
    # return a new mapedit object with a small concave room
    output = omg.mapedit.MapEditor()
    shape = Shape()
    shape.add_vertex(0,0)
    shape.add_vertex(64,64)
    shape.add_vertex(128,0)
    shape.add_vertex(64,128)
    shape.write_to_map(output)
    return output

def test_multiple_sectors_map():
    output = omg.mapedit.MapEditor()

    shape = Shape()
    shape.add_vertex(0,0)
    shape.add_vertex(64,64)
    shape.add_vertex(128,0)
    shape.add_vertex(64,128)
    shape.add_vertex(0,128)
    shape.write_to_map(output)

    shape = Shape()
    shape.add_vertex(128,0)
    shape.add_vertex(256,0)
    shape.add_vertex(192,128)
    shape.add_vertex(64,128)
    shape.write_to_map(output)

    shape = Shape()
    shape.add_vertex(64,192)
    shape.add_vertex(0,192)
    shape.add_vertex(0,128)
    shape.add_vertex(64,128)
    shape.z_floor = 64
    shape.write_to_map(output)

    return output

def test_line_splitting():
    output = omg.mapedit.MapEditor()

    shape = Shape()
    shape.add_vertex(0,0)
    shape.add_vertex(128,0)
    shape.add_vertex(128,128)
    shape.write_to_map(output)

    shape = Shape()
    shape.add_vertex(-32,-32)
    shape.add_vertex(-64,32)
    shape.add_vertex(-64,96)
    shape.add_vertex(96,96)
    shape.reverse()
    shape.write_to_map(output)

    return output


if __name__=="__main__":
    wad = omg.WAD()
    wad.maps["MAP01"] = test_line_splitting().to_lumps()
    wad.to_file('test.wad')
    drawmap.drawmap(wad,"MAP01",300).show()
