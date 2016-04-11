import c4d
import struct
import random
from c4d import gui, bitmaps
#Import MagicaVoxel .VOX files and MagicaVoxel .PNG Palette Files
#by @matesteinforth

def importVox(path):
    #parse file
    with open(path, 'rb') as f:
        
        #check filetype
        bytes = f.read(4)
        file_id = struct.unpack(">4s",  bytes)
        if file_id[0] == 'VOX ':
    
            #init material list
            matlist = [];
            BaseCube = c4d.BaseObject(c4d.Ocube)
            BaseCube[c4d.PRIM_CUBE_DOFILLET]=True
            BaseCube[c4d.PRIM_CUBE_FRAD]=8    
            BaseCube[c4d.PRIM_CUBE_SUBF]=1
            doc.InsertObject(BaseCube)
    
            #skip header
            f.seek(56)
            
            #read number of voxels, stuct.unpack parses binary data to variables
            bytes = f.read(4)
            numvoxels = struct.unpack('<I', bytes)
            
            #iterate through voxels
            for x in range(0, numvoxels[0]):
                
                #read voxels, ( each voxel : 1 byte x 4 : x, y, z, colorIndex ) x numVoxels
                bytes = f.read(4)
                voxel = struct.unpack('<bbbB', bytes)    
                
                #generate Cube and set position, change to 'Oinstance' for instances
                MyCube = c4d.BaseObject(c4d.Oinstance)
                MyCube[c4d.INSTANCEOBJECT_RENDERINSTANCE]=True
                MyCube[c4d.INSTANCEOBJECT_LINK]=BaseCube
                MyCube.SetAbsPos(c4d.Vector(-voxel[1]*200,voxel[2]*200,voxel[0]*200))
                
                #update material list, generate new material only if it isn't in the list yet
                matid = voxel[3]
                if matid not in matlist:
                    matlist.append(matid)
                    myMat = c4d.BaseMaterial(c4d.Mmaterial)
                    myMat.SetName(str(matid))
                    myMat[c4d.MATERIAL_COLOR_COLOR]=c4d.Vector(random.random(), random.random(), random.random())
                    doc.InsertMaterial(myMat)
                
                #assign material to voxel and insert everything into the scene
                mat = doc.SearchMaterial(str(matid))
                textag = c4d.TextureTag()
                textag.SetMaterial(mat)
                MyCube.InsertTag(textag)
                doc.InsertObject(MyCube)
                
        else:
            gui.MessageDialog('Not a .VOX file')
            
def importPalette(path):
    orig = bitmaps.BaseBitmap()
    if orig.InitWith(path)[0] != c4d.IMAGERESULT_OK:
        gui.MessageDialog("Cannot load image \"" + path + "\".")
        return
    
    width, height = orig.GetSize()
    
    if height != 1:
        gui.MessageDialog("This is not a MagicaVoxel .PNG Palette")
    else:
        for x in range(0, width):
            mat = doc.SearchMaterial(str(x+1))
            if mat:
                color = orig.GetPixel(x, 0)
                mat[c4d.MATERIAL_COLOR_COLOR]=c4d.Vector(float(color[0])/255, float(color[1])/255, float(color[2])/255)

def main():
    #stop all threads and clear console
    c4d.StopAllThreads()
    c4d.CallCommand(13957)

    #fileselector and execute main function
    myFile = c4d.storage.LoadDialog(title="Open MagicaVoxel .VOX Voxel File...")
    importVox(myFile)

    #fileselector and execute main function    
    myFile = c4d.storage.LoadDialog(title="Open MagicaVoxel .PNG Palette File...")
    importPalette(myFile)
    
    #update scene
    c4d.EventAdd()

if __name__=='__main__':
    main()
