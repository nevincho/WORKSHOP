; Inno Setup script for per-user installation. Requires validated Windows onedir build.
#define MyAppName "WORKSHOP Desktop V1"
#define MyAppVersion "0.1.0"
#define MyAppExeName "WORKSHOPDesktopV1.exe"

[Setup]
AppId={{A8B6C74F-81E1-4A20-9A33-DBA2B1C64901}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={localappdata}\Programs\WORKSHOPDesktopV1
DefaultGroupName={#MyAppName}
PrivilegesRequired=lowest
OutputDir=installer-output
OutputBaseFilename=WORKSHOPDesktopV1-Setup
Compression=lzma
SolidCompression=yes
UninstallDisplayIcon={app}\{#MyAppExeName}

[Files]
Source: "dist\WORKSHOPDesktopV1\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{userdesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; Flags: unchecked

[UninstallRun]
Filename: "{app}\WORKSHOPDesktopV1.exe"; Parameters: "--revoke-credentials"; Flags: runhidden waituntilterminated
