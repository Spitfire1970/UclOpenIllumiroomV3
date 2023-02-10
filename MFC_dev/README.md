# MI_Multitouch_Settings_MFC
MFC C++ Settings application designed for Multitouch on Windows.

Author: Anelia Gaydardzhieva

### To Run:
Go into "MFC-UCL-MI3-Settings" folder and double click on the "MFC-UCL-MI3-Settings.exe" file

## For Developers

### Structure
The structure of this repository mimics integration with MotionInput v3.1 (MI_31),
with only essential for the MFC application files and folders copied from MI_31. 
This allows to run the MFC application in isolation and ensure intentional performance when integrated with MI_31. 

"data" folder stores "config.json" and "mode_controller" which are taken from MI_31. 
"configMFC.json" is a helper file which makes it possible to have MI_31 running while using the MFC app. MI_31 uses "config.json" intensively and it is therefore locked and cannot be modified while MI_31 is running. 
To resolve this problem and allow simultaneous execution of both applications several steps take place in the MFC application. Firstly, we make a copy of "config.json" and save it into "configMFC.json"; then we save all changes made by the user into "configMFC.json"; next we run the "quitMIapp.bat" which closes MI_31 app; then we copy "configMFC.json" over to "config.json"; and lastly, we run MI_31 again and the MFC application closes itself. 

"help.txt" is needed to open on "?" button click in the MFC app.

"packages" folder contains "nlohmann.json.3.10.5" which is the JSON library used to read and write into the JSON files. 

"MI3-Multitouch-3.1.exe" is a simple executable printing "Hello World!". It is placed as a structural reminder; however, it could serve as a test for basic interactions.


### Source code 
To access and run the source code please follow the steps below.

1. In case you have not done so already, install Visual Studio (preferrably v2022)
2. Open Visual Studio Intaller 
3. Select "Modify". If you have more than one version of VS installed, select "Modify" on the version you wish to access the code from. 
4. Select "Individual Components"
5. Find the box with the latest C++ MFC (e.g. "C++ MFC for latest v142 build tools (x86 & x64)")
6. If the box is not marked with a tick, select it and save
Then to modify the code simply open the "MFC-UCL-MI3-Settings.sln" file in Visual Studio 

### View/Modify Dialog box
Steps in VS: 
View->Resource View->Dialog file

### Access main file
View->Solution Explorer->Source Files->"MFC-UCL-MI3-SettingsDlg.cpp"

### Compile 
1. Change Solution Configurations from Debug to Release
2. Set option x64 or x86 and Build Solution
3. This will create a "Release" folder for x86 and "x64" folder with "Release" inside for x64
4. The compiled .exe file is in that folder
5. Copy the .exe file and Paste it into the "MFC-UCL-MI3-Settings" folder, replacing the previous .exe in this location
6. Go to MI_31 (or the latest MI version) and place the .exe file in the "MFC-UCL-MI3-Settings" folder there
7. Task completed! :)



