@echo off
chcp 936 >nul
title 古典文学网 - 控制台
setlocal

rem ============================================================
rem  古典文学网 · 控制台
rem  开发：MySQL 3306 + 后端 5382 + Vite 5173
rem  Apache 8088 只在需要看生产效果时用，目前用不上
rem ============================================================

rem ---------------- 管理员权限自检 ----------------
net session >nul 2>&1
if errorlevel 1 (
    echo 正在请求管理员权限，请在弹窗中点击「是」 ...
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs" 2>nul
    exit /b
)

set "APACHE_HOME=D:\System\Apache24"
set "PROJECT=D:\高级网页设计\cls_svr"
set "CLT=D:\高级网页设计\cls_clt"
set "MYSQL_ERR=D:\System\MySQL server\mysql84.err"
set "VCTOOLS=C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC"

:menu
cls
echo ============================================================
echo   古典文学网 . 控制台
echo ------------------------------------------------------------
echo   1. 启动开发环境    MySQL 3306 + 后端 5382 + Vite 5173
echo   2. 停止开发环境
echo.
echo   3. 仅启动 MySQL
echo   4. 仅重启 Apache（部署用，暂时不需要）
echo   5. 查看运行状态
echo   6. 启用 mod_wsgi（一次性部署）
echo.
echo   0. 退出
echo ============================================================
choice /C 1234560 /N /M "请选择："
set "SEL=%errorlevel%"

if "%SEL%"=="1" goto :start_dev
if "%SEL%"=="2" goto :stop_dev
if "%SEL%"=="3" goto :start_mysql
if "%SEL%"=="4" goto :restart_apache
if "%SEL%"=="5" goto :status
if "%SEL%"=="6" goto :modwsgi
if "%SEL%"=="7" goto :end
goto :menu

rem ==================== 1. 启动开发环境 ====================
:start_dev
cls
echo ============================================================
echo   启动开发环境
echo ============================================================
echo.
echo [1/3] MySQL 3306 ...
netstat -ano | findstr ":3306" | findstr "LISTENING" >nul
if errorlevel 1 (
    net start MySQL84
    if errorlevel 1 (
        echo     [失败] 见 %MYSQL_ERR%
    ) else (
        echo     已启动
    )
) else (
    echo     已在运行，跳过
)

echo [2/3] 后端 5382 ...
netstat -ano | findstr ":5382" | findstr "LISTENING" >nul
if not errorlevel 1 (
    echo     已在运行，跳过
    goto :dev_vite
)
start "cls_svr 后端 5382" cmd /k "cd /d %PROJECT% && .venv\Scripts\python.exe run.py"
timeout /t 4 >nul
netstat -ano | findstr ":5382" | findstr "LISTENING" >nul
if errorlevel 1 (
    echo     [警告] 5382 未监听，看后端窗口里的报错
) else (
    echo     已就绪
)

:dev_vite
echo [3/3] Vite 5173 ...
netstat -ano | findstr ":5173" | findstr "LISTENING" >nul
if not errorlevel 1 (
    echo     已在运行，跳过
    goto :dev_open
)
start "cls_clt Vite 5173" cmd /k "cd /d %CLT% && npm run dev"
set "WAIT=0"
:wait_vite
timeout /t 1 >nul
netstat -ano | findstr ":5173" | findstr "LISTENING" >nul
if not errorlevel 1 goto :dev_open
set /a WAIT+=1
if %WAIT% lss 20 goto :wait_vite
echo     [警告] 20 秒内 5173 未监听，看 Vite 窗口里的报错

:dev_open
echo.
echo 打开 http://localhost:5173
start "" http://localhost:5173
goto :done

rem ==================== 2. 停止开发环境 ====================
:stop_dev
cls
echo ============================================================
echo   停止开发环境
echo ============================================================
echo.
echo [1/3] Vite 5173 ...
set "F1="
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5173" ^| findstr "LISTENING"') do (
    taskkill /PID %%a /T /F >nul 2>&1
    set "F1=1"
    echo     已结束 PID %%a
)
if not defined F1 echo     未运行

echo [2/3] 后端 5382 ...
set "F2="
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5382" ^| findstr "LISTENING"') do (
    taskkill /PID %%a /T /F >nul 2>&1
    set "F2=1"
    echo     已结束 PID %%a
)
timeout /t 2 >nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5382" ^| findstr "LISTENING"') do (
    taskkill /PID %%a /T /F >nul 2>&1
    echo     已结束重启的 PID %%a
)
if not defined F2 echo     未运行

echo [3/3] MySQL84 ...
net stop MySQL84 >nul 2>&1
if errorlevel 1 (
    echo     未运行或停止失败
) else (
    echo     已停止
)

echo.
echo 已停止。后端和 Vite 那两个窗口现在可以关掉了。
goto :done

rem ==================== 3. 仅启动 MySQL ====================
:start_mysql
cls
echo ============================================================
echo   MySQL 3306
echo ============================================================
echo.
netstat -ano | findstr ":3306" | findstr "LISTENING" >nul
if not errorlevel 1 (
    echo 已在运行：127.0.0.1:3306
    goto :done
)

net start MySQL84
if errorlevel 1 (
    echo.
    echo [失败] 服务未能启动，按顺序排查：
    echo   1. 残留进程： tasklist ^| findstr mysqld
    echo   2. 错误日志： %MYSQL_ERR%
    echo   3. 配置文件： D:\System\MySQL server\my.ini
    goto :done
)

timeout /t 2 >nul
netstat -ano | findstr ":3306" | findstr "LISTENING" >nul
if errorlevel 1 (
    echo [警告] 服务已启动但 3306 未监听，看 %MYSQL_ERR%
) else (
    echo [成功] 127.0.0.1:3306 已就绪
)
echo.
echo 数据库：classicsdb    账号：root
goto :done

rem ==================== 4. 仅重启 Apache ====================
:restart_apache
cls
echo ============================================================
echo   重启 Apache 8088
echo ============================================================
echo.
sc query apache2.4 >nul 2>&1
if errorlevel 1 (
    echo 未安装 apache2.4 服务，改为结束前台进程后重启 ...
    taskkill /IM httpd.exe /F >nul 2>&1
    timeout /t 1 >nul
    start "Apache 8088" cmd /k "cd /d %APACHE_HOME%\bin && httpd.exe -D FOREGROUND"
) else (
    "%APACHE_HOME%\bin\httpd.exe" -k restart -n "apache2.4"
    if errorlevel 1 (
        echo 服务未运行，尝试启动 ...
        net start apache2.4
    )
)
timeout /t 3 >nul
netstat -ano | findstr ":8088" | findstr "LISTENING" >nul
if errorlevel 1 (
    echo [警告] 8088 未监听，检查 httpd.conf 与错误日志
) else (
    echo [成功] 8088 已监听
)
goto :done

rem ==================== 5. 查看状态 ====================
:status
cls
echo ============================================================
echo   运行状态
echo ============================================================
echo.
netstat -ano | findstr ":3306" | findstr "LISTENING" >nul
if errorlevel 1 (echo   3306  MySQL    未监听) else (echo   3306  MySQL    正常)
netstat -ano | findstr ":5382" | findstr "LISTENING" >nul
if errorlevel 1 (echo   5382  后端     未监听) else (echo   5382  后端     正常)
netstat -ano | findstr ":5173" | findstr "LISTENING" >nul
if errorlevel 1 (echo   5173  Vite     未监听) else (echo   5173  Vite     正常)
netstat -ano | findstr ":8088" | findstr "LISTENING" >nul
if errorlevel 1 (echo   8088  Apache   未监听) else (echo   8088  Apache   正常)

echo.
echo --- 服务 ---
sc query MySQL84 | findstr "STATE"
sc query apache2.4 | findstr "STATE"

echo.
echo --- 接口自检 ---
curl -s -o nul -w "   5382/api      HTTP %%{http_code}\n" http://127.0.0.1:5382/api/classics/get-classictypes
curl -s -o nul -w "   8088/svr/api  HTTP %%{http_code}\n" http://127.0.0.1:8088/svr/api/classics/get-classictypes
goto :done

rem ==================== 6. 启用 mod_wsgi ====================
:modwsgi
cls
echo ============================================================
echo   启用 mod_wsgi（教材 9.3.2 / 9.3.3）
echo ============================================================
echo.
echo 切换后后端由 Apache 直接加载，run.py 与 run_prod.py 都不再需要。
echo 回退： cls_svr\.venv\Scripts\python.exe cls_svr\deploy\switch_to_mod_wsgi.py --revert
echo.
choice /C YN /N /M "确认继续？(Y/N)："
if errorlevel 2 goto :done

echo.
echo [1/4] 检查 Microsoft C++ 生成工具 ...
if exist "%VCTOOLS%" (
    echo     已安装，跳过
) else (
    echo     未安装，开始下载安装（约 3GB，耗时较长）...
    winget install --id Microsoft.VisualStudio.2022.BuildTools ^
        --accept-package-agreements --accept-source-agreements ^
        --override "--quiet --wait --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
    if errorlevel 1 (
        echo     [错误] 安装失败。可手动装：https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/
        goto :done
    )
)

echo [2/4] 编译安装 mod_wsgi ...
set MOD_WSGI_APACHE_ROOTDIR=%APACHE_HOME%
"%PROJECT%\.venv\Scripts\python.exe" -m pip install mod_wsgi
if errorlevel 1 (
    echo     [错误] 编译失败，把上面的报错发出来
    goto :done
)

echo [3/4] 修改 httpd.conf ...
"%PROJECT%\.venv\Scripts\python.exe" "%PROJECT%\deploy\switch_to_mod_wsgi.py"
if errorlevel 1 (
    echo     [错误] 切换失败，回滚： deploy\switch_to_mod_wsgi.py --revert
    goto :done
)

echo [4/4] 重启 Apache ...
"%APACHE_HOME%\bin\httpd.exe" -k restart -n "apache2.4"
if errorlevel 1 (
    "%APACHE_HOME%\bin\httpd.exe" -k start -n "apache2.4"
)
timeout /t 3 >nul
echo.
curl -s -o nul -w "   8088 /api = %%{http_code}\n" http://127.0.0.1:8088/svr/api/classics/get-classictypes
goto :done

rem ==================== 结束 ====================
:done
echo.
echo ------------------------------------------------------------
pause
goto :menu

:end
endlocal
exit /b 0
