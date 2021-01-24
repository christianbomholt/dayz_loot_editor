SET PATH_TO_PROJECT=%~dp0
cd "%PATH_TO_PROJECT%\compiled"

pyinstaller --clean --noupx --hidden-import decimal --name DayZ_LootEditor --distpath "%PATH_TO_PROJECT%\compiled" --path "C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64" --onefile --icon="%PATH_TO_PROJECT%\data\miniLogo.ico" --clean "%PATH_TO_PROJECT%\app.py"

