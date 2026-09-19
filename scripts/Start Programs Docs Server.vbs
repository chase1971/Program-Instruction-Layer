' Starts the Programs docs server (port 8765) with no visible console.
' Idempotent — does nothing if the server is already responding.
Option Explicit

Dim fso, sh, ps1Path, cmd

Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
ps1Path = fso.BuildPath(fso.GetParentFolderName(WScript.ScriptFullName), "ensure-programs-docs-server.ps1")

If Not fso.FileExists(ps1Path) Then
  MsgBox "Could not find ensure-programs-docs-server.ps1.", 16, "Programs Docs Server"
  WScript.Quit 1
End If

cmd = "powershell.exe -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File """ & ps1Path & """"
sh.Run cmd, 0, False
