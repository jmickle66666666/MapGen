import omg
import drawmap

# this class stores a list of vertex positions and can write itself to a map
class Shape:
    def __init__(self):
        self.vertexes = []

        # default values
        self.z_floor = 0
        self.z_ceil = 128
        self.tx_floor = 'SLIME14'
        self.tx_ceil = 'SLIME14'
        self.tx_sides = 'WOOD5'
        self.light = 192

    def add_vertex(self,x,y):
        # add a vertex. vertexes must be clockwise
        self.vertexes.append([int(x),int(y)])

    def write_to_map(self,mapedit):
        # add the first vertex to the end of the list to make it a closed sector
        self.vertexes.append([self.vertexes[0][0],self.vertexes[0][1]])

        # this is to make sectors drawn clockwise, not counter-clockwise
        self.vertexes.reverse() 

        # first create the sector data the shape will use
        new_sector = omg.mapedit.Sector()
        new_sector.z_floor = self.z_floor
        new_sector.z_ceil = self.z_ceil
        new_sector.tx_floor = self.tx_floor
        new_sector.tx_ceil = self.tx_ceil
        new_sector.light = self.light

        def add_vertex(v_id):
            # first have a look in the map's vertexes to see if the one we want
            # to add is already there, and just return that instead
            for vx in mapedit.vertexes:
                if self.vertexes[v_id][0] == vx.x:
                    if self.vertexes[v_id][1] == vx.y:
                        return mapedit.vertexes.index(vx)

            # give an index for the vertex in our own vertexes list, 
            # and add it to the map, returning an index in the map's vertexes list
            new_vx = omg.mapedit.Vertex()
            new_vx.x = self.vertexes[v_id][0]
            new_vx.y = self.vertexes[v_id][1]
            mapedit.vertexes.append(new_vx)
            return len(mapedit.vertexes)-1

        # due to the dodgy way i'm adding lines, we store this data so the loop works correctly
        vxb = add_vertex(0)

        for i in range(len(self.vertexes)-1):
            # set up all the new data
            vxa = vxb

            vxb = add_vertex(i+1)

            new_side = omg.mapedit.Sidedef()
            new_side.tx_mid = self.tx_sides
            new_side.sector = len(mapedit.sectors)

            new_line = omg.mapedit.Linedef()
            new_line.vx_a = vxa
            new_line.vx_b = vxb
            new_line.flags = 1
            new_line.front = len(mapedit.sidedefs)

            # add the new data
            
            mapedit.sidedefs.append(new_side)
            mapedit.linedefs.append(new_line)

        # finally, add the last vertex and sector
        add_vertex(len(self.vertexes)-1)
        mapedit.sectors.append(new_sector)

        self.vertexes.reverse() 

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
    shape.write_to_map(output)

    return output

if __name__=="__main__":
    wad = omg.WAD()
    wad.maps["MAP01"] = test_multiple_sectors_map().to_lumps()
    wad.to_file('test.wad')
    drawmap.drawmap(wad,"MAP01",300).show()
