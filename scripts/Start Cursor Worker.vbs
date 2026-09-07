Option Explicit

' Launches the Cloud Agent worker with no visible console. A detached cmd.exe window
' would steal focus on login and would kill the worker if it were ever closed.

Dim fso, sh, root, ps1Path, cmd

Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
root = fso.GetParentFolderName(WScript.ScriptFullName)
ps1Path = fso.BuildPath(root, "cursor-worker-start.ps1")

cmd = "powershell.exe -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File """ & ps1Path & """"

sh.Run cmd, 0, False
