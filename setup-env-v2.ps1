# 创建新的虚拟环境
Write-Host "正在创建虚拟环境..." -ForegroundColor Green
python -m venv d:\code\3d-ai-platform\backend\venv-new

# 激活虚拟环境
Write-Host "正在激活虚拟环境..." -ForegroundColor Green
& d:\code\3d-ai-platform\backend\venv-new\Scripts\Activate.ps1

# 升级pip
Write-Host "正在升级pip..." -ForegroundColor Green
python -m pip install --upgrade pip

# 安装依赖
Write-Host "正在安装依赖..." -ForegroundColor Green
pip install fastapi==0.104.1 uvicorn==0.24.0 sqlalchemy==2.0.23 pymysql==1.1.0 pymongo==4.5.0 minio==7.1.16 redis==5.0.1 celery==5.3.4 python-jose==3.3.0 passlib==1.7.4 python-multipart==0.0.6 alembic==1.12.1 pydantic==2.5.0 pydantic-settings==2.1.0 requests==2.31.0 aiofiles==23.2.1 openai==1.3.0 pillow==10.1.0 numpy==1.24.3 scipy==1.11.4 python-dotenv==1.0.0 bcrypt==4.1.0

Write-Host "虚拟环境配置完成！" -ForegroundColor Green
Write-Host "使用以下命令启动后端服务器：" -ForegroundColor Yellow
Write-Host "d:\code\3d-ai-platform\backend\venv-new\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "cd d:\code\3d-ai-platform\backend" -ForegroundColor Cyan
Write-Host "python -m uvicorn app.main:app --reload" -ForegroundColor Cyan
