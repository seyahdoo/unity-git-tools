
Remove-Item -Path "dist" -Recurse
Remove-Item -Path "setup\Output" -Recurse

pyinstaller --onefile main.py --name yo

setup\InnoSetup6\iscc.exe setup\setup-script.iss
