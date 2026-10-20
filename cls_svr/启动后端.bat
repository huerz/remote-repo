@echo off
chcp 65001 >nul
cd /d %~dp0
title cls_svr 后端（端口 5382）

echo ============================================
echo  古典文学网 后端服务
echo  地址: http://127.0.0.1:5382
echo  停止: 按 Ctrl+C
echo ============================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [错误] 找不到项目虚拟环境 .venv\Scripts\python.exe
    echo 请先在本目录执行：
    echo     python -m venv .venv
    echo     .venv\Scripts\python.exe -m pip install -r requirements.txt
    pause
    exit /b 1
)

".venv\Scripts\python.exe" run.py

echo.
echo 服务已停止。
pause
