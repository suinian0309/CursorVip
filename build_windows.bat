@echo off
echo ===================================
echo Cursorvip Windows Builder
echo ===================================

:: 检查Python环境
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python未安装，请先安装Python 3.x
    exit /b 1
)

:: 检查并安装依赖
echo 正在检查并安装依赖...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

:: 获取版本号
for /f "tokens=2 delims==" %%a in ('type .env ^| findstr VERSION') do set VERSION=%%a
echo 当前版本: %VERSION%

:: 清理旧的构建文件
echo 清理旧的构建文件...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__

:: 开始构建
echo 开始构建Windows版本...
pyinstaller @build.spec

:: 检查构建结果
if exist "dist\CursorVIP_%VERSION%_windows.exe" (
    echo ===================================
    echo 构建成功！
    echo 输出文件: dist\CursorVIP_%VERSION%_windows.exe
    echo ===================================
) else (
    echo 构建失败，请检查错误信息
)

pause
