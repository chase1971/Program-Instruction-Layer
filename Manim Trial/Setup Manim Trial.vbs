Option Explicit

' One-click laptop setup: installs FFmpeg, MiKTeX, uv deps, and runs verify render.
' No visible console — check Manim Trial/media/videos/verify_render/ for output.

Dim fso, sh, root, ps1Path, cmd

Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
root = fso.GetParentFolderName(WScript.ScriptFullName)
ps1Path = fso.BuildPath(root, "setup.ps1")

cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File """ & ps1Path & """"

sh.Run cmd, 0, False
