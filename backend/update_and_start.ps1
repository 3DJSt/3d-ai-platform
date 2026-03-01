cd d:\code\3d-ai-platform\backend

# 激活虚拟环境
.\venv-clean\Scripts\Activate.ps1

# 更新数据库表结构（删除旧表并重新创建）
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  更新数据库表结构" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
python scripts/create_tables.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "数据库表结构更新失败" -ForegroundColor Red
    exit 1
}

# 创建示例数据
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  创建示例数据" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
python scripts/create_sample_data.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "创建示例数据失败" -ForegroundColor Red
    exit 1
}

# 启动后端服务器
Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  启动后端服务器" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
