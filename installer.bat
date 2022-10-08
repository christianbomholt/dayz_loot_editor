SET PATH_TO_PROJECT=%~dp0
REM cd "%PATH_TO_PROJECT%\compiled"

pyinstaller --clean --noupx --name DayZ_LootEditor --hidden-import=loguru --hidden-import FileDialog --log-level=DEBUG --distpath "%PATH_TO_PROJECT%\compiled" --path "C:\Windows\WinSxS\x86_microsoft-windows-m..namespace-downlevel_31bf3856ad364e35_10.0.15063.0_none_7c5a1866018b960d" --onefile --icon="%PATH_TO_PROJECT%\data\LootEditor.ico" --clean "%PATH_TO_PROJECT%\app.py"
pause