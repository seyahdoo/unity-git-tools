
Remove-Item -Path "dist" -Recurse

pyinstaller --onefile main.py --name yo

