Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c java -jar camera.jar"
oShell.Run strArgs, 0, false