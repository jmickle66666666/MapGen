import omg

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

    def reverse(self):
        self.vertexes.reverse()

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

        def check_and_split(v_id,ld):
            v = mapedit.vertexes[v_id]
            #first check the vertex isn't literally part of the line, dummy
            if ld.vx_a != v_id and ld.vx_b != v_id: 
                #then check if the vertex is in the bounds of the line
                v1 = mapedit.vertexes[ld.vx_a]
                v2 = mapedit.vertexes[ld.vx_b]
                x1 = min(v1.x,v2.x)
                x2 = max(v1.x,v2.x)
                y1 = min(v1.y,v2.y)
                y2 = max(v1.y,v2.y)

                if (v.x >= x1 and v.x <= x2 and
                    v.y >= y1 and v.y <= y2): 
                    # now see if the point is actually on the line
                    split = False
                    dx = v1.x-v2.x
                    dy = v1.y-v2.y
                    if dx == 0:
                        split = True
                    elif dy == 0:
                        split = True
                    else:
                        perc = float(v.x - v1.x) / float(dx)
                        ly = float(dy) * perc
                        if abs(ly - v.y) < 0.1: 
                            split = True

                    if split:
                        temp_vx = ld.vx_b
                        ld.vx_b = v_id
                        side = add_sidedef(mapedit.sidedefs[ld.front].sector,mapedit.sidedefs[ld.front].tx_mid)
                        add_line(v_id,temp_vx,side)

        def add_line(vx_a,vx_b,sidedef):
            output = -1

            # first check if there is already a line in the map using these vertexes
            # but the other way round, and if so we attach onto the back of
            # that line, and don't create a new one
            for ld in mapedit.linedefs:
                if ld.vx_a == vx_b:
                    if ld.vx_b == vx_a:
                        ld.back = sidedef
                        # fix texturing too
                        mapedit.sidedefs[ld.front].tx_up = mapedit.sidedefs[ld.front].tx_mid
                        mapedit.sidedefs[ld.front].tx_low = mapedit.sidedefs[ld.front].tx_mid
                        mapedit.sidedefs[ld.front].tx_mid = '-'
                        mapedit.sidedefs[ld.back].tx_up = mapedit.sidedefs[ld.back].tx_mid
                        mapedit.sidedefs[ld.back].tx_low = mapedit.sidedefs[ld.back].tx_mid
                        mapedit.sidedefs[ld.back].tx_mid = '-'
                        output = mapedit.linedefs.index(ld)

            if output == -1:
                # create a line
                new_line = omg.mapedit.Linedef()
                new_line.vx_a = vx_a
                new_line.vx_b = vx_b
                new_line.flags = 1
                new_line.front = sidedef
                mapedit.linedefs.append(new_line)
                output = len(mapedit.linedefs)-1

            # split line across existing vertexes!!!
            # for vx in range(len(mapedit.vertexes)):
            #     check_and_split(vx,mapedit.linedefs[output])

            return output

        def add_sidedef(sector, texture):
            new_side = omg.mapedit.Sidedef()
            new_side.tx_mid = texture
            new_side.sector = sector
            mapedit.sidedefs.append(new_side)
            return len(mapedit.sidedefs)-1

        def add_vertex(v_id):
            v = self.vertexes[v_id]

            # first have a look in the map's vertexes to see if the one we want
            # to add is already there, and just return that instead
            output = -1
            for vx in mapedit.vertexes:
                if v[0] == vx.x:
                    if v[1] == vx.y:
                        exists = True
                        output = mapedit.vertexes.index(vx)

            if output == -1:
                # give an index for the vertex in our own vertexes list, 
                # and add it to the map, returning an index in the map's vertexes list
                new_vx = omg.mapedit.Vertex()
                new_vx.x = v[0]
                new_vx.y = v[1]
                mapedit.vertexes.append(new_vx)
                output = len(mapedit.vertexes)-1

            # check to see if vertex lands upon an existing line, and split it if so
            for ld in mapedit.linedefs:
                check_and_split(output,ld)

            return output

        

        # due to the dodgy way i'm adding lines, we store this data so the loop works correctly
        vxb = add_vertex(0)

        for i in range(len(self.vertexes)-1):
            vxa = vxb
            vxb = add_vertex(i+1)
            sd = add_sidedef(len(mapedit.sectors),self.tx_sides)
            add_line(vxa,vxb,sd)

        # finally, add the last vertex and sector
        add_vertex(len(self.vertexes)-1)
        mapedit.sectors.append(new_sector)

        self.vertexes.reverse() 