# $PSScriptRoot는 이 ps1 파일이 있는 현재 폴더 경로를 의미합니다.
# 즉, 이 파일과 같은 폴더에 있는 'main.py'를 지정합니다.
$ScriptPath = "$PSScriptRoot\main.py"

Write-Host "Executing Python script..." -ForegroundColor Cyan

# 파이썬 실행
python $ScriptPath

# 실행이 끝나고 창이 바로 꺼지는 것을 방지 (결과 확인용)
Write-Host "`nFinished." -ForegroundColor Green
Read-Host "Press Enter..."