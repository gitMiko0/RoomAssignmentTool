# ==========================================
# Script: build.ps1
# Purpose: Build Room Assignment Tool as .exe
# ==========================================

$mainScript = "src\room_assign_tool.py"
$exeName = "room_assign_tool"

Write-Host "`n=== Building Executable ==="
pyinstaller --onefile --distpath dist --name $exeName $mainScript
Write-Host "`n Build succeeded. Output: dist\$exeName.exe"

