####################################
# Maya Batch Renamer by Rassoul Edji
# Version 1.0
####################################

from maya import cmds
import maya.api.OpenMaya as om

# Suffix dictionairy
SUFFIXES = {
    "mesh": "GEO",
    "joint": "JNT",
    "camera": None,
    "ambientLight": "LGT",
    "directionalLight": "LGT",
    "pointLight": "LGT",
    "spotLight": "LGT",
}

DEFAULT_SUFFIX = "GRP"

class batchRenamerUi(object):

    WINDOW_NAME = "batchRenamerUi"
    APP_NAME = "Batch Renamer"
    
    @classmethod
    def display(cls):
        cls.delete()

        main_window = cmds.window(cls.WINDOW_NAME,
                                  title="Batch Renamer",
                                  sizeable=True,
                                  menuBar=True)

        main_layout = cmds.columnLayout(adjustableColumn=True, parent=main_window)

        # Method UI
        method_layout = cmds.formLayout(parent=main_layout)

        cls.method = cmds.radioButtonGrp(numberOfRadioButtons=2,
                                            label="Method: ",
                                            columnWidth=(1, 75),
                                            h=(27),
                                            w=512,
                                            sl=1,
                                            labelArray2=("Selected", "Hierarchy"),
                                            parent=method_layout)

        cmds.formLayout(method_layout, e=True, af=(cls.method, "top", 0))

        # Rename UI
        rename_layout = cmds.frameLayout(label="Rename", parent=main_layout, bgs=True)
        rename_form_layout = cmds.formLayout(parent=rename_layout, h=60)
        
        cls.name_tfg = cmds.textFieldGrp(label="Name: ",                                               
                                                columnWidth=(1, 75),
                                                columnWidth2=(2, 426),
                                                editable=True,
                                                parent=rename_form_layout)
        cls.prefix_tfg = cmds.textFieldGrp(label="Prefix: ",
                                                columnWidth=(1, 75),
                                                columnWidth2=(2, 100),
                                                editable=True,
                                                parent=rename_form_layout)
        cls.suffix_tfg = cmds.textFieldGrp(label="Suffix: ",
                                                columnWidth=(1, 35),
                                                columnWidth2=(2, 100),
                                                editable=True,
                                                parent=rename_form_layout)
        cls.autoSuffix_cbg = cmds.checkBoxGrp(numberOfCheckBoxes=1,
                                               label="Auto Suffix: ",
                                               columnWidth=(1, 60),
                                               io=False,
                                               changeCommand=cls.toggleSuffixField,
                                               parent=rename_form_layout)
        padding_label = cmds.text("Padding: ", align="right", width=50, parent=rename_form_layout)
        cls.padding = cmds.intField(width=50,
                                            value=1,
                                            minValue=1,
                                            maxValue=6,
                                            step=1,
                                            parent=rename_form_layout)

        cmds.formLayout(rename_form_layout, e=True, af=(cls.name_tfg, "top", 6))
        cmds.formLayout(rename_form_layout, e=True, af=(cls.name_tfg, "left", 0))
        cmds.formLayout(rename_form_layout, e=True, ac=(cls.prefix_tfg, "top", 3, cls.name_tfg))
        cmds.formLayout(rename_form_layout, e=True, ac=(cls.suffix_tfg, "top", 3, cls.name_tfg))
        cmds.formLayout(rename_form_layout, e=True, ac=(cls.suffix_tfg, "left", 0, cls.prefix_tfg))
        cmds.formLayout(rename_form_layout, e=True, ac=(cls.autoSuffix_cbg, "top", 6, cls.name_tfg))
        cmds.formLayout(rename_form_layout, e=True, ac=(cls.autoSuffix_cbg, "left", 0, cls.suffix_tfg))
        cmds.formLayout(rename_form_layout, e=True, ac=(padding_label, "top", 6, cls.name_tfg))
        cmds.formLayout(rename_form_layout, e=True, ac=(padding_label, "left", 0, cls.autoSuffix_cbg))
        cmds.formLayout(rename_form_layout, e=True, ac=(cls.padding, "top", 3, cls.name_tfg))
        cmds.formLayout(rename_form_layout, e=True, ac=(cls.padding, "left", 0, padding_label))

        # Search and Replace UI
        replace_layout = cmds.frameLayout(label="Search and Replace", parent=main_layout, bgs=True)

        replace_form_layout = cmds.formLayout(parent=replace_layout, h=65)

        cls.searchFor_tfg = cmds.textFieldGrp(label="Search For: ",
                                                columnWidth=(1, 75),
                                                columnWidth2=(2, 426),
                                                editable=True,
                                                parent=replace_form_layout)
        cls.replaceWith_tfg = cmds.textFieldGrp(label="Replace With: ",
                                                columnWidth=(1, 75),
                                                columnWidth2=(2, 426),
                                                editable=True,
                                                parent=replace_form_layout)

        cmds.formLayout(replace_form_layout, e=True, af=(cls.searchFor_tfg, "top", 6))
        cmds.formLayout(replace_form_layout, e=True, af=(cls.searchFor_tfg, "left", 0))
        cmds.formLayout(replace_form_layout, e=True, ac=(cls.replaceWith_tfg, "top", 3, cls.searchFor_tfg))

        # Buttons UI
        button_layout = cmds.flowLayout(parent=main_layout)
        rename_btn = cmds.button(label="Rename",
                                 width=170,
                                 height=28,
                                 command= "batchRenamerUi.rename_objects()",
                                 parent=button_layout)
        replace_btn = cmds.button(label="Replace",
                                 width=170,
                                 height=28,
                                 command= "batchRenamerUi.replace_objects()",
                                 parent=button_layout)
        replace_btn = cmds.button(label="Cancel",
                                 width=170,
                                 height=28,
                                 command="batchRenamerUi.delete()",
                                 parent=button_layout)

        cmds.window(main_window, e=True, w=200, h=150)
        cmds.window(main_window, e=True, sizeable=True)
        cmds.window(main_window, e=True, rtf=True)

        cmds.showWindow(main_window)

    @classmethod
    def delete(cls):
        if cmds.window(cls.WINDOW_NAME, exists=True):
            cmds.deleteUI(cls.WINDOW_NAME, window=True)

    # This function checks if Auto Suffix is enabled and disables the Suffix input field if so
    @classmethod
    def toggleSuffixField(cls, value):
        if value:
            cmds.textFieldGrp(cls.suffix_tfg, e=1, en=0)
        else:
            cmds.textFieldGrp(cls.suffix_tfg, e=1, en=1)
            
    # This function renames the selected objects using the given values
    @classmethod
    def rename_objects(cls):

        rename_data = cmds.textFieldGrp(cls.name_tfg, query=True, text=True)
        prefix_data = cmds.textFieldGrp(cls.prefix_tfg, query=True, text=True)
        padding_data = cmds.intField(cls.padding, query=True, value=True)
        hierarchy_data = cmds.radioButtonGrp(cls.method, query=True, select=True)
        counter = 1 

        # Determines the selection
        if hierarchy_data == 2:
            sel = cmds.ls(sl=True, tr=True)
            children = cmds.listRelatives(sel, ad=True, type='transform')
            cmds.select(children, add=True)
            sel = cmds.ls(sl=True)
        else: 
            sel = cmds.ls(sl=True)

        if len(sel) < 1:
            raise RuntimeError("Please select at least one object to rename")
        else:
            for obj in sel:
                if cmds.checkBoxGrp(cls.autoSuffix_cbg, query=True, value1=True):
                    objType = cmds.objectType(obj)

                    if objType == "transform":
                        children = cmds.listRelatives(obj, children=True, ni=True)[0]
                        objType = cmds.objectType(children)
                    suffix_data = "_" + SUFFIXES.get(objType, DEFAULT_SUFFIX)
                else:
                    suffix_data = cmds.textFieldGrp(cls.suffix_tfg, query=True, text=True)

                cmds.rename("{0}{1}{2}{3}".format(prefix_data, rename_data, str(counter).zfill(padding_data), suffix_data))
                counter+=1

        # Prints how many objects were renamed and deselects everything 
        print("Renamed {0} Objects".format(len(sel)))
        cmds.select(cl=True)
        
    # This function searches for a given string and replaces it with another given string
    @classmethod
    def replace_objects(cls):

        searchFor_data = cmds.textFieldGrp(cls.searchFor_tfg, query=True, text=True)
        replaceWith_data = cmds.textFieldGrp(cls.replaceWith_tfg, query=True, text=True)
        hierarchy_data = cmds.radioButtonGrp(cls.method, query=True, select=True)
        
        # Determines the selection
        if hierarchy_data == 2:
            sel = cmds.ls(sl=True, tr=True)
            children = cmds.listRelatives(sel, ad=True, type='transform')
            cmds.select(children, add=True)
            sel = cmds.ls(sl=True)
        else: 
            sel = cmds.ls(sl=True)

        if len(sel) < 1:
            raise RuntimeError("Please select at least one object to replace")
        elif searchFor_data == "":
            raise RuntimeError("Please enter a name to search for")
        elif replaceWith_data == "":
            raise RuntimeError("Please enter a name to replace with")
        else:
            for i in sel:
                if searchFor_data in i:
                    renamedString = i.replace(searchFor_data, replaceWith_data)
                    cmds.rename(i, renamedString)

if __name__ == "__main__":
    
    batchRenamerUi.display()
