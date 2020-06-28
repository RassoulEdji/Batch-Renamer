# Batch Renamer
![Header Image](https://pro2-bar-s3-cdn-cf3.myportfolio.com/f9f32fafec8469ded945bb426cf75684/4f9700a5-736c-4be0-901c-7c2d5b335351_rw_1920.jpg?h=10c045a1d83ebbff4f1c54ce71fe8558)
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
Now, in Maya, open the script editor and paste in this code into a Python executer: 
```
from batchRenamer import batchRenamerUi

batchRenamerUi.display()
```
You can save that code to a shelf button for ease of use by going to "File" in the Script Editor and then selecting "Save Script to Shelf..."
You can use then use the Shelf Editor to make changes to the button like assigning the custom icon. 

# Custom suffixes

With the feature to Auto Suffix based on the object type you can also easily change the type of object and what it's relative suffix should be by editing the dictionairy in the "batchRenamer.py" file. Below is the default suffix dictionairy found with the Batch Renamer. 
```
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
```


Simply open the file in an editor of your choice and modify the dictionairy at the top of the file with the object type and the associated suffix in the same format as the existing entries above. Note that Maya will need to be restarted for the new additions to the dictionairy to take effect.

