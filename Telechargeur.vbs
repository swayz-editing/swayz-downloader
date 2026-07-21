' Lance SWΛYZ sans afficher de fenêtre de console
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = scriptDir
shell.Run "pythonw """ & scriptDir & "\app.py""", 0, False
