Option Explicit

' Adds Manim Setup to electron-toolbar Launcher Panel (no Manim install).
' Progress: Manim Trial\wire-launcher.log

Dim fso, sh, root, ps1Path, cmd

Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
root = fso.GetParentFolderName(WScript.ScriptFullName)
ps1Path = fso.BuildPath(root, "wire-electron-toolbar-launcher.ps1")

cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File """ & ps1Path & """"

sh.Run cmd, 0, False
