# Create Game Installers – Basic Guide

## 1. Install Inno Setup

* Download and install Inno Setup https://jrsoftware.org/
* Open **Inno Setup Compiler**

---

## 2. Create a Script

* Use the **Script Wizard** OR create a `.iss` file manually
* This defines how your installer works

---

## 3. Define App Info (Top of Script)

```ini
#define MyAppName "My App"
#define MyAppVersion "1.0"
#define MyAppPublisher "My Company"
```

---

## 4. Configure Setup Section

```ini
[Setup]
AppId={{YOUR-GUID-HERE}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\{#MyAppName}
OutputBaseFilename={#MyAppName}
Compression=none
```

* `AppId` must be unique (generate in Tools → Generate GUID)
* `DefaultDirName` = install location

---

## 5. Add Files

```ini
[Files]
Source: "C:\Path\To\YourApp\*"; DestDir: "{app}"; Flags: recursesubdirs
```

* Copies your app files into the install directory

---

## 6. Create Shortcuts

```ini
[Icons]
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\MyApp.exe"
```

---

## 7. (Optional) Modify Config Files

```ini
[INI]
Filename: "{app}\config.ini"; Section: "settings"; Key: "example"; String: "value"
```

---

## 8. Add User Input (Player Name)

* Prompt the user to enter a player name during install
* Alternatively, allow it to be passed in silently via command line
* Store this value and use it in config files
* See example files for code

---

## 9. Build Installer

* Press **F9 (Compile)**
* Output `.exe` will be created in the output folder

---

## 10. Test

* Run installer
* Check:

  * Files installed
  * Shortcuts work
  * Config changes applied
  * Create games.yaml entry and install from the user interface

---