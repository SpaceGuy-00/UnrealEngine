from unreal import AssetToolsHelpers, EditorAssetLibrary, AssetTools, Material, MaterialFactoryNew, MaterialEditingLibrary, MaterialExpressionTextureSampleParameter2D as TexSample2D, MaterialProperty, AssetImportTask, FbxImportUI #imports things needed from Unreal to Python
import os #allows for import of operating software
class UnrealUtility: #creates a new class that will be using tools from Unreal
    def __init__(self): #defines new objects
        self.substanceRooDir = '/game/Substance' #tells where the root directory will be
        self.substanceBaseMatName = 'M_SubstnaceBase' #sets material name
        self.substanceBaseMatPath = self.substanceRooDir + self.substanceBaseMatName #creates path to the Substance Painter's files
        self.substanceTempFolder = '/game/substance/temp' #tells where the temp folders will be
        self.baseColorName = "BaseColor" #sets Basecolor
        self.normalName = "Normal" #sets Normal
        self.occRoughnessMetalic = "OcclusionRoughnessMetalic" #sets Occlusion, Roughness, and Metalic

    def GetAssetTools(self) -> AssetTools: #defines the asset tools
        return AssetToolsHelpers.get_asset_tools() #returns the tools
    
    def ImportFromDir (self, dir): #defines the import from Directory
        for file in os.listdir(dir): #creates a loop that seraches for the files
            if ".fbx" in file: #checks for .fbx file
                self.LoadMeshFromPath(os.path.join(dir, file)) #loads the file

    def LoadMeshFromPath(self, meshPath): #defines loading the mesh from file path
        meshName = os.path.split(meshPath)[-1].replace(".fbx", "") #re-names the mesh
        importTask = AssetImportTask() #imports the tasks
        importTask.replace_existing = True # replaces old tasks; upadtes with new changes
        importTask.filename = meshPath # sets file path
        importTask.destination_path = '/game/' + meshName #sets the destination
        importTask.automated=True #auto-imports the task
        importTask.save=True #saves the task

        FbxImportOption = FbxImportUI() #creates Fbx Options to the FBX UI
        FbxImportOption.import_mesh=True #allows for mesh Import
        FbxImportOption.import_as_skeletal=False #does not allow for the meshes skeletal's to be imported
        FbxImportOption.import_materials=False #does not allow for the meshes material's to be imported
        FbxImportOption.skeletal_mesh_import_data.combine_meshes=True  #combines the mesh into one; if it's not already

        self.GetAssetTools().import_asset_tasks([importTask]) #imports the task
        return importTask.get_objects()[0] #returns task
        

    def FindOrBuildBaseMaterial(self): #defines wether to build or find the material
       if EditorAssetLibrary.does_asset_exist(self.substanceBaseMatPath): #if the material exists-
           return EditorAssetLibrary.load_asset(self.substanceBaseMatPath) #it'll load material
       
       baseMat = AssetToolsHelpers.get_asset_tools().create_asset(self.substanceBaseMatName, self.substanceRooDir, Material, MaterialFactoryNew()) #creates a new material; also setting the name and root directory for said material
       baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 0 ) #creates a Texture Sample2D with the value choosen
       baseColor.set_editor_property("parameter_name", self.baseColorName) #sets up the parameter name for the base color
       MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR) #conncects the property of the base color

       normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 400) #creates a Texture Sample2D with the value choosen
       normal.set_editor_property("parameter_name", self.normalName) #sets up the parameter name for the normal
       normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal")) #sets texture and loads the assets  
       MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL) #conncects the property of the normal

       occRoughnessMetalic = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 800)
       occRoughnessMetalic.set_editor_property("parameter_name", self.occRoughnessMetalic) #sets up the parameter name for the Occulssion, Roughness, and Metalic
       MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION) #sets up the property of Ambient Occlusion
       MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "G", MaterialProperty.MP_ROUGHNESS) #sets up the property of Roughness
       MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "B", MaterialProperty.MP_METALLIC) #sets up the property of Metallic

       EditorAssetLibrary.save_asset(baseMat.get_path_name()) #it'll save the materiaL
       return baseMat #returns the material 


       