from maya import cmds
import maya.api.OpenMaya as om
import maya.OpenMayaUI as omui

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

############################
# UI
############################

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class TestDialog(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)
        
        self.setWindowTitle("Batch Renamer")
        self.setMinimumWidth(650)
        
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
    def create_widgets(self):
        self.name_le = QtWidgets.QLineEdit()
        
        self.prefix_le = QtWidgets.QLineEdit()
        self.suffix_le = QtWidgets.QLineEdit()
        self.autoSuffix_cb = QtWidgets.QCheckBox("Auto Suffix")
        self.padding_sb = QtWidgets.QSpinBox()
        self.padding_sb.setFixedWidth(80)
        self.padding_sb.setMinimum(1)
        self.padding_sb.setMaximum(6)
        
        self.rename_btn = QtWidgets.QPushButton("Rename")
        self.replace_btn = QtWidgets.QPushButton("Replace")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        
        self.counter = QtWidgets.QLabel(displayedAmount + " objects selected for renaming")
        
        self.selected_rb = QtWidgets.QRadioButton("Selected")
        self.selected_rb.setChecked(True)
        self.hierarchy_rb = QtWidgets.QRadioButton("Hierarchy")
        
        self.searchFor_le = QtWidgets.QLineEdit()
        self.replaceWith_le = QtWidgets.QLineEdit()

        
    def create_layouts(self):
        radio_btn_layout = QtWidgets.QHBoxLayout()
        radio_btn_layout.addWidget(self.selected_rb)
        radio_btn_layout.addWidget(self.hierarchy_rb)
        
        options_layout = QtWidgets.QHBoxLayout()
        options_layout.addWidget(self.prefix_le)
        options_layout.addWidget(self.suffix_le)
        options_layout.addWidget(self.autoSuffix_cb)
        options_layout.addWidget(self.padding_sb)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.rename_btn)
        button_layout.addWidget(self.replace_btn)
        button_layout.addWidget(self.cancel_btn)
        
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Method:", radio_btn_layout)
        form_layout.addRow("", self.counter)
        form_layout.addRow("Name:", self.name_le)
        form_layout.addRow("Prefix:", options_layout)
        form_layout.addRow("Search for:", self.searchFor_le) 
        form_layout.addRow("Replace with:", self.replaceWith_le) 
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        
    def create_connections(self):
        self.name_le.editingFinished.connect(self.name_data)
        
        self.autoSuffix_cb.toggled.connect(self.auto_suffix_data)
        
        self.cancel_btn.clicked.connect(self.close)
        
    def name_data(self):
        name = self.name_le.text()
        print("Hello {0}!".format(name))
        
    def auto_suffix_data(self):
        auto_suffix = self.autoSuffix_cb.isChecked()
        if auto_suffix:
            print("Auto Suffix Turned On")
        else: 
            print("Auto Suffix Not On")
        

        

#############################
# Backend
#############################

# User inputs
sel = cmds.ls(sl=True)


# Displays how many objects are selected with comma seperators
displayedAmount = (format(len(sel), ","))




# Makes sure user has selected objects for renaming
if not sel:
    om.MGlobal.displayError("Please select objects to rename")
        

def rename_objects(name, startsAt=1):
    # This function renames the selected objects
    counter = startsAt
    for i in sel:
        cmds.rename('%s_%s' % (name, counter))
        counter+=1
        
#def searchAndReplace():
    # This function searches the selected objects for a given string and replaces it with the user inputted string
    # counter = startsAt
    
if __name__ == '__main__':
    
    try:
        test_dialog.close() # pylint: disable=E0601
        test_dialog.deleteLater()
    except:
        pass
    
    test_dialog = TestDialog()
    test_dialog.show()
    
    

