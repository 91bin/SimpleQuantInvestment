# $PSScriptRoot는 이 ps1 파일이 있는 현재 폴더 경로를 의미합니다.
# 즉, 이 파일과 같은 폴더에 있는 'main.py'를 지정합니다.
$ScriptPath = "$PSScriptRoot\main.py"

Write-Host "Python 스크립트를 실행합니다..." -ForegroundColor Cyan

# 파이썬 실행
python $ScriptPath

# 실행이 끝나고 창이 바로 꺼지는 것을 방지 (결과 확인용)
Write-Host "`n실행이 완료되었습니다." -ForegroundColor Green
Read-Host "종료하려면 Enter 키를 누르세요..."