# Batch Renamer

This is a Batch Renaming tool created to help with the renaming of large scenes and characters. 

Its features are:
- Suffix and Prefix
- Auto-Suffix based on object type (object types can be added along with custom suffixes)
- Padding for numbering
- In line search and replace

# Installation

To install the Batch Renamer tool you must copy the downloaded "batchRenamer.py" file to your Maya scripts directory. 

It is usually found here:
```
C:\Users\<USER>\Documents\maya\<MAYA VERSION>\scripts
```
Now, in Maya, open the script editor and paste in this code: 
```
from batchRenamer import batchRenamerUi

batchRenamerUi.display()
```
You can save that code to a shelf button for ease of use by going to "File" in the Script Editor and then selecting "Save Script to Shelf..."
You can use then use the Shelf Editor to make changes to the button like assigning the custom icon. 

# Custom suffixes

With the feature to Auto Suffix based on the object type you can also easily change the type of object and what it's relative suffix should be by changing the dictionairy in the "batchRenamer.py" file.

Simply open the file in an editor of your choice and modify the dictionairy at the top of the file with the object type and the associated suffix in the same format as the existing entries. Note that Maya will need to be restarted for the new additions to the dictionairy to take effect.
