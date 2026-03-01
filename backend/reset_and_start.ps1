cd d:\code\3d-ai-platform\backend

# 使用虚拟环境的Python删除旧表并重新创建
Write-Host "正在删除旧表并重新创建..." -ForegroundColor Green
.\venv-clean\Scripts\python.exe scripts/create_tables.py

# 使用虚拟环境的Python启动后端服务器
Write-Host "正在启动后端服务器..." -ForegroundColor Green
.\venv-clean\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
