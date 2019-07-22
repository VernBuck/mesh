# Sample code for starting the mesh processing project

rotate_flag = True    # automatic rotation of model?
time = 0   # keep track of passing time, for automatic rotation
#both of these lists store the needed values to draw
#global geometryTable
geometryTable = []
#global vertexTable
vertexTable = []
#global oppositeTable
oppositeTable = []
#global cornerTable
cornerTable = []
#global oppositeTable
oppositeTable = []
#global normal table 
normalTable = []

colorTable = []
#keeping track of the number of faces
global faceCount
#keeping track of the number of verticies
global vertCount
global colorWhite
colorWhite = False
colorRandom = False
perBoolean = False
global dualCount
dualCount = 0


# initalize stuff
def setup():
    size (600, 600, OPENGL)
    noStroke()

# draw the current mesh
def draw():
    global time
    global colorTable
    background(0)    # clear screen to black

    perspective (PI*0.333, 1.0, 0.01, 1000.0)
    camera (0, 0, 5, 0, 0, 0, 0, 1, 0)    # place the camera in the scene
    scale (1, -1, 1)    # change to right-handed coordinate system
    
    # create an ambient light source
    ambientLight (102, 102, 102)
  
    # create two directional light sources
    lightSpecular (204, 204, 204)
    directionalLight (102, 102, 102, -0.7, -0.7, -1)
    directionalLight (152, 152, 152, 0, 0, -1)
    
    pushMatrix();

    fill (50, 50, 200)            # set polygon color
    ambient (200, 200, 200)
    specular (0, 0, 0)            # no specular highlights
    shininess (1.0)
  
    rotate (time, 1.0, 0.0, 0.0)

    # THIS IS WHERE YOU SHOULD DRAW THE MESH
    if (colorWhite is True):
        fill(200,200,200)
    #print(colorTable)
    for item in range(0, len(vertexTable), 3):
        a = geometryTable[vertexTable[item]]
        b = geometryTable[vertexTable[item + 1]]
        c = geometryTable[vertexTable[item + 2]]
        if (colorRandom):
           # print(item)
            fill(colorTable[item//3])
        if(perBoolean is False):
            
            beginShape()  
            pa =  PVector(a[0], a[1], a[2])
            pb =  PVector(b[0], b[1], b[2])
            pc =  PVector(c[0], c[1], c[2])
    
            u = pb - pa
            v = pc - pa

            norma = PVector.cross(u,v)
            normCalc = -1*(norma / norma.mag())
            normal(normCalc.x, normCalc.y, normCalc.z)
            vertex(a[0],a[1],a[2])
            vertex(b[0],b[1],b[2])
            vertex(c[0],c[1],c[2])
        else:    
            global normalSum
            normalSum = [0,0,0]
            #get normal of every face N1 + N2... / # of faces
            beginShape()
            #normalCompute()   
            #normalSumX = storageL[0] / faceCount
            #normalSumY = storageL[1] / faceCount
            #normalSumZ = storageL[2] / faceCount
            
            thing = storageL[vertexTable[item]]
            thing2 = storageL[vertexTable[item + 1]]
            thing3 = storageL[vertexTable[item + 2]]
            normal(thing.x, thing.y, thing.z)
            #normal(storageL[vertexTable[item]], storageL[vertexTable[item + 1]], storageL[vertexTable[item + 2]]) #normal[vert[i]]    
            vertex(a[0],a[1],a[2]) #geo[vert[i]]
            #normal(storageL[vertexTable[item]], storageL[vertexTable[item + 1]], storageL[vertexTable[item + 2]])
            normal(thing2.x, thing2.y, thing2.z)
            vertex(b[0],b[1],b[2])
            normal(thing3.x, thing3.y, thing3.z)
            #normal(storageL[vertexTable[item]], storageL[vertexTable[item + 1]], storageL[vertexTable[item + 2]])
            vertex(c[0],c[1],c[2])
        
        endShape(CLOSE)
    
    popMatrix()
    
    # maybe step forward in time (for object rotation)
    if rotate_flag:
        time += 0.02

# process key presses
def keyPressed():
    global colorWhite
    global colorRandom
    global perBoolean
    global rotate_flag
    if key == ' ':
        rotate_flag = not rotate_flag
    elif key == '1':
        read_mesh ('tetra.ply')
    elif key == '2':
        read_mesh ('octa.ply')
    elif key == '3':
        read_mesh ('icos.ply')
    elif key == '4':
        read_mesh ('star.ply')
    elif key == '5':
        read_mesh ('torus.ply')
    elif key == 'n':
        perBoolean = not perBoolean
        
        pass  # toggle per-vertex shading
    elif key == 'r':
        colorRandom = not colorRandom
        colorWhite = False
        randomColorHelper()
        pass  # randomly color faces
    elif key == 'w':
        colorWhite = not colorWhite
        colorRandom = False
        pass  # color faces white
    elif key == 'd':
        #dualCount = dualCount + 1
        #if dualCount > 2:
        #    dualCount = 0
        #println(dualCount)
        dual()
        randomColorHelper()
        pass  # calculate the dual mesh
    elif key == 'q':
        exit()

# read in a mesh file (THIS NEEDS TO BE MODIFIED !!!)
def read_mesh(filename):
    global geometryTable
    geometryTable = []
    global vertexTable
    vertexTable = []
    global oppositeTable
    oppositeTable = []
    global cornerTable
    cornerTable = []
    global oppositeTable
    global normalTable
    normalTable = []
    global faceCount
    global colorTable
    colorTable = []
    
    
    colorWhite = False
    colorRandom = False
    perBoolean = False
    
    fname = "data/" + filename
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()
        
    # determine number of vertices (on first line)
    words = lines[0].split()
    num_vertices = int(words[1])
    print "number of vertices =", num_vertices
    #setting global verticies value
    vertCount = num_vertices

    # determine number of faces (on first second)
    words = lines[1].split()
    num_faces = int(words[1])
    print "number of faces =", num_faces
    #setting global face value
    faceCount = num_faces

    # read in the vertices
    for i in range(num_vertices):
        words = lines[i+2].split()
        x = float(words[0])
        y = float(words[1])
        z = float(words[2])
        print "vertex = ", x, y, z
        #modifying the global geometryTable
        geometryTable.append([x,y,z])
        #println(geometryTable)
        # face table
    
    global faceList
    faceList = []
    
    # read in the faces
    for i in range(num_faces):
        j = i + num_vertices + 2
        words = lines[j].split()
        nverts = int(words[0])
        if nverts != 3:
            print "error: this face is not a triangle"
            exit()
        
        index1 = int(words[1])
        index2 = int(words[2])
        index3 = int(words[3])
        print "face =", index1, index2, index3
        #modifying the global vertexTable
        vertexTable.append(index1)
        vertexTable.append(index2)
        vertexTable.append(index3)
        faceList.append(faceClass(index1, index2, index3))
        
    #println(vertexTable)
    
    oppositeTable = [0 for x in range(len(vertexTable))]
    #creates opposite table
    #indexC = 1
    #for a in cornerTable:
    for i in range(len(vertexTable)):
        a = i
        at = a //3
        an = 3 * at + (a + 1) % 3
        ap = ((an // 3) * 3) + (an + 1) % 3
        for j in range(len(vertexTable)):
            b = j
            bt = b //3
            bn = 3 * bt + (b + 1) % 3
            bp = ((bn // 3) * 3) + (bn + 1) % 3        
            if (vertexTable[an] == vertexTable[bp] and vertexTable[ap] == vertexTable[bn]):
                oppositeTable[i] = b
                oppositeTable[j] = a
    #println(oppositeTable)
    normalCompute() 
    randomColorHelper()
    
def swing(oppositeTableIndex):
    # v(c)): s(c)=p(l(c))
    s = oppositeTableIndex
    #first get the previous
    st = s //3
    sn = 3 * st + (s + 1) % 3
    sp = ((sn // 3) * 3) + (sn + 1) % 3
    #then calculate the left corner
    leftCorner = oppositeTable[sn]
    ltt = leftCorner // 3
    leftCN = 3 * ltt + (leftCorner + 1) % 3
    leftCP = ((leftCN // 3) * 3) + (leftCN + 1) % 3
    return leftCN
    

#Random color alternating method
def randomColorHelper():
    global colorTable
    reD = int(random(0,255))
    greeN = int(random(0,255))
    bluE = int(random(0,255))
        
    coloR = color(reD, greeN, bluE)
        
    colorTable = []
    for x in range(len(faceList)):
        newcoloR = color(int(random(0,255)),int(random(0,255)),int(random(0,255)))
        colorTable.append(newcoloR)
        #colorTable.append(coloR)
       # rand = int(random(0,6))
        #global randomVal
       # randomVal = randArr[rand]
    #println(colorTable)
    return newcoloR
    
def normalCompute():
    global storageL
    storageL = []
    for i in range(len(geometryTable)):
        index = vertexTable.index(i)
        sW = swing(index) 
        counter = 0
        normalSum = [0,0,0]
        while sW != index:
            counter = counter + 1
            temp = sW//3 *3
            a = geometryTable[vertexTable[temp]]
            b = geometryTable[vertexTable[temp + 1]]
            c = geometryTable[vertexTable[temp + 2]]
                
            pa =  PVector(a[0], a[1], a[2])
            pb =  PVector(b[0], b[1], b[2])
            pc =  PVector(c[0], c[1], c[2])
    
            u = pb - pa
            v = pc - pa
            norma = PVector.cross(u,v)
            normCalc = -1*(norma / norma.mag())
            normalSum[0] = normalSum[0] + normCalc.x 
            normalSum[1] = normalSum[1] + normCalc.y
            normalSum[2] = normalSum[2] + normCalc.z
            sW = swing(sW)
        itemL = PVector(normalSum[0], normalSum[1], normalSum[2])
        itemL = itemL.normalize()
        storageL.append(itemL)
        
def dual():
    #calculate centroid step
    #centroid average the verticies of the face
    global faceList
    global newGeoTable
    newGeoTable = []
    #println(faceList)
    global newVertTable
    global geometryTable
    global vertexTable
    newVertTable = []
    newFaceList = []
    
    for i in range(0, len(vertexTable),3):
        #newGeoTable.append(faceList[i].centroidCalculation())
        v1 = geometryTable[vertexTable[i]]
        v2 = geometryTable[vertexTable[i + 1]]
        v3 = geometryTable[vertexTable[i + 2]]
        newX = v1[0] + v2[0] + v3[0]
        newY = v1[1] + v2[1] + v3[1]
        newZ = v1[2] + v2[2] + v3[2]
        newGeoTable.append(PVector(newX/3,newY/3,newZ/3))
    println(newGeoTable)
    #println(newGeoTable)
    
    
    global adjFace
    
    #4 faces for first object
    #println(faceList)
    
    #println(geometryTable)
    for vert in geometryTable:
        adjFace = []
        for v in range(len(vertexTable)):
            curV = -1
            if geometryTable[vertexTable[v]] == vert:
                print("hit,")
                print(v)
                curV = v
                break 
        adjFace.append(curV//3)
        curV = swing(curV)
        #println(curV)
        
        #println(curV//3)
        #println(adjFace)
        while curV//3 != adjFace[0]:
            #println(curV//3)
            adjFace.append(curV//3)
            curV = swing(curV)
        #println(str(adjFace))


    #Calculate super cetroid of the list of centroid 
        global superCentroid
        superCentroid = PVector(0,0,0)
        for i in range(len(adjFace)):
            superCentroid += newGeoTable[adjFace[i]]
            println(i)
        superCentroid /= len(adjFace)
        println(superCentroid)
        newGeoTable.append(superCentroid)
        #c1 = NewGeoTable[i]
        #println(c1)
        
        for i in range(len(adjFace)):
            v1 = adjFace[i]
            v2 = adjFace[(i + 1) % len(adjFace)] 
            v3 = len(newGeoTable) - 1 
            
            newVertTable.append(v1)
            newVertTable.append(v2)
            newVertTable.append(v3)
            newFaceList.append(faceClass(v1,v2,v3))
        faceList = newFaceList
            
    geometryTable = []
    for x in newGeoTable:
        geometryTable.append([x.x, x.y, x.z])
    vertexTable = newVertTable
    println(newVertTable)
    println(len(newVertTable))
    println(newGeoTable)
    
    global oppositeTable
    oppositeTable = [0 for x in range(len(vertexTable))]
    #creates opposite table
    #indexC = 1
    #for a in cornerTable:
    for i in range(len(vertexTable)):
        a = i
        at = a //3
        an = 3 * at + (a + 1) % 3
        ap = ((an // 3) * 3) + (an + 1) % 3
        for j in range(len(vertexTable)):
            b = j
            bt = b //3
            bn = 3 * bt + (b + 1) % 3
            bp = ((bn // 3) * 3) + (bn + 1) % 3        
            if (vertexTable[an] == vertexTable[bp] and vertexTable[ap] == vertexTable[bn]):
                oppositeTable[i] = b
                oppositeTable[j] = a        
        

    #for x in geometryTable:
        #x = 0, PVector (0,0,0) theory example
        #faceClass(object)
        
        
        #adjFace.append(x)
        
    #println(adjFace)
         #adjFaceCentroid = geometryTable.append(faceList[i].centroidCalculation())
         #swing
        
        #swing(i)
        #for each vert in old GeoTable
        #get all adj faces for current vertex and save indicies of the face in a list
        # calculate ultimate centroid by going through all adj faces (centroid of each face)
        # add each adj face and divide by # of face
        
        #add the ultimate centroid to new geometry table (append it to the very end (c, c, c, uc)
        #still inside the same for loop
        # make new for loop
        # go through all adjacent faces
        # if at last adj face get 
        #println(newGeoTable)
       # superCentroid = superCentroid / len(newGeoTable)
       # println(superCentroid)
            
   #new vertex table step
   # println(newGeoTable)
    #for i in range faceList:
        
            
    #List of centroids around face Like vertex shading while loop above
    
    #Centroid and super centroids are new geometry table of the dual
    # super centroid is centroid for centroids
    #re assign vert, geo, opp, and norm redo
class faceClass(object):
    def __init__(self,index1,index2,index3):
        self.index1 = index1
        self.index2 = index2
        self.index3 = index3
    def centroidCalculation(self):
        v1 = geometryTable[self.index1]
        v2 = geometryTable[self.index2]
        v3 = geometryTable[self.index3]
        newX = v1[0] + v2[0] + v3[0]
        newY = v1[1] + v2[1] + v3[1]
        newZ = v1[2] + v2[2] + v3[2]
        return PVector(newX, newY, newZ) / 3
    def __repr__(self):
        return str(self.index1)