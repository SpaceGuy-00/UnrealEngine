import tkinter.filedialog #allows for access files of the 'Tkinter'
from unreal import ToolMenuContext, ToolMenus, uclass , ufunction, ToolMenuEntryScript #imports things needed from Unreal to Python

import os #allows for import of operating software
import importlib #allows for importing others python modules
import sys #allows for variables to be imported
import tkinter #allows for us to create GUI elements

SrcPath = os.path.dirname(os.path.abspath(__file__)) # The Absolute path of the directory  
if SrcPath not in sys.path: # If the directory path is not on system path- 
    sys.path.append(SrcPath) # it'll add the directory path to it

import UnrealUtilities #allows for tools in Unreal to used in Python
importlib.reload(UnrealUtilities) #reloads whenever changes are made

@uclass() #marks class in code to a Uclass 
class BuildBaseMaterialEntryScript(ToolMenuEntryScript): #creates new class that uses 'ToolMenuEntryScript'
    @ufunction(override=True) #allows to exectue  
    def execute(self, context: ToolMenuContext) -> None: #defines execute
        UnrealUtilities.UnrealUtility().FindOrBuildBaseMaterial() #allows for the use of 'FindOrBuildBaseMaterial'

@uclass() #marks class in code to a Uclass 
class LoadMeshEntryScript(ToolMenuEntryScript): #creates new class that uses 'ToolMenuEntryScript'
    @ufunction (override=True) #allows to exectue  
    def execute(self, context) -> None: #defines execute
        Window = tkinter.Tk() #creates window for GUI
        Window.withdraw() #makes invsible 
        importDir = tkinter.filedialog.askdirectory() #alows for us to choose directory
        Window.destroy() #closes widnow after we pick directory
        UnrealUtilities.UnrealUtility.ImportFromDir(importDir) #imports the information from said diectory
        

class UnrealSubstancePlugin: #creates new class
    def __init__(self): #defines new objects
        self.submenuName = "UnrealSubstancePlugin" #names the sub menu
        self.submeunLabel = "Unreal Substnace Plugin" #labels the sub menu
        self.CreateMenu() #creates the sub menu

    def CreateMenu(self): #defines the sub menu
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu") #find the main menu using 'Tool Menus"

        existing = ToolMenus.get().find_menu(f"LevelEditor.MainMenu.{self.submenuName}") #checks for exisitng sub menu
        if existing: #if it finds it'll-
            print (f"deleting previous menu: {existing}") #prints the deleting menu
            ToolMenus.get().remove_menu(existing.menu_name) #deletes the sub menu

        self.submenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", self.submenuName, self.submeunLabel) #adds a new sub menu
        self.AddEntryScript("BuildBaseMaterial", "Build Base Material", BuildBaseMaterialEntryScript()) #adds the 'BuildBaseMaterialEntryScript' to the new menu
        self.AddEntryScript("LoadFromDirectory", "Load From Directory", LoadMeshEntryScript) #adds 'LoadMeshEntryScript' to the new menu
        ToolMenus.get().refresh_all_widgets() #saves changes to the sub menu

    def AddEntryScript(self, name, Label, script: ToolMenuEntryScript): #defines adding the entry script to the sub meuns
        script.init_entry(self.submenu.menu_name, self.submenu.menu_name, "", name, Label) #creates meun
        script.register_menu_entry() #registers menu to the tool menus

UnrealSubstancePlugin() #plays the code 