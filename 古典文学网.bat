@echo off
chcp 936 >nul
title 古典文学网 - 控制台
setlocal

rem ============================================================
rem  古典文学网 · 统一控制台
rem
rem  【生产 8088】Apache 跑 cls_clt\dist + waitress 后端
rem  【开发 5173】Vite 热更新 + Flask run.py 自动重载
rem  两条链共用后端端口 5382，同一时间只能跑一种
rem
rem  启动/停止 Windows 服务需要管理员权限，脚本自动提权一次
rem ============================================================

rem ---------------- 管理员权限自检 ----------------
net session >nul 2>&1
if errorlevel 1 (
    echo 正在请求管理员权限，请在弹窗中点击「是」 ...
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs" 2>nul
    if errorlevel 1 (
        echo.
        echo [失败] 自动提权未成功，请右键本文件 -^> 以管理员身份运行
        pause
    )
    exit /b
)

set "APACHE_HOME=D:\System\Apache24"
set "PROJECT=D:\高级网页设计\cls_svr"
set "CLT=D:\高级网页设计\cls_clt"
set "MYSQL_ERR=D:\System\MySQL server\mysql84.err"
set "VCTOOLS=C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC"
set "WEB_PROD=http://localhost:8088"
set "WEB_DEV=http://localhost:5173"

:menu
cls
echo ============================================================
echo   古典文学网 . 控制台
echo ------------------------------------------------------------
echo   [生产 8088]  Apache 跑 dist + waitress 后端
echo     1. 启动生产     MySQL 3306 + 后端 5382 + Apache 8088
echo     2. 停止生产     Apache + 后端 + MySQL
echo.
echo   [开发 5173]   Vite 热更新 + Flask 自动重载
echo     3. 启动开发     MySQL 3306 + 后端 5382 + Vite 5173
echo     4. 停止开发     后端 + Vite + MySQL
echo.
echo   [维护]
echo     5. 仅启动 MySQL
echo     6. 仅重启 Apache
echo     7. 查看运行状态
echo     8. 启用 mod_wsgi（一次性部署，耗时较长）
echo.
echo     0. 退出
echo ============================================================
choice /C 123456780 /N /M "请选择："
set "SEL=%errorlevel%"

if "%SEL%"=="1" goto :start_prod
if "%SEL%"=="2" goto :stop_prod
if "%SEL%"=="3" goto :start_dev
if "%SEL%"=="4" goto :stop_dev
if "%SEL%"=="5" goto :start_mysql
if "%SEL%"=="6" goto :restart_apache
if "%SEL%"=="7" goto :status
if "%SEL%"=="8" goto :modwsgi
if "%SEL%"=="9" goto :end
goto :menu

rem ==================== 1. 启动生产 8088 ====================
:start_prod
cls
echo ============================================================
echo   启动生产环境   %WEB_PROD%
echo   MySQL 3306  +  后端 5382 (run_prod.py)  +  Apache 8088
echo ============================================================
echo.
echo [1/3] MySQL 3306 ...
netstat -ano | findstr ":3306" | findstr "LISTENING" >nul
if errorlevel 1 (
    net start MySQL84
    if errorlevel 1 (
        echo     [失败] 见 %MYSQL_ERR%
    ) else (
        echo     MySQL 已启动
    )
) else (
    echo     MySQL 已在运行，跳过
)

echo [2/3] 后端 5382（waitress，无热重载）...
call :stop_backend_quiet
start "cls_svr 生产 5382" cmd /k "cd /d %PROJECT% && .venv\Scripts\python.exe run_prod.py"
timeout /t 3 >nul
netstat -ano | findstr ":5382" | findstr "LISTENING" >nul
if errorlevel 1 (
    echo     [警告] 5382 未监听，看后端窗口报错
) else (
    echo     后端已就绪
)

echo [3/3] Apache 8088 ...
call :ensure_apache

echo.
echo 打开 %WEB_PROD%
start "" %WEB_PROD%
goto :done

rem ==================== 2. 停止生产 ====================
:stop_prod
cls
echo ============================================================
echo   停止生产环境
echo ============================================================
echo.
echo [1/3] Apache ...
call :stop_apache

echo [2/3] 后端 5382 ...
call :stop_backend

echo [3/3] MySQL84 ...
net stop MySQL84 >nul 2>&1
if errorlevel 1 (
    echo     未运行或停止失败
) else (
    echo     MySQL 已停止
)

echo.
echo 已停止。页面还是旧的按 Ctrl+F5。
goto :done

rem ==================== 3. 启动开发 5173 ====================
:start_dev
cls
echo ============================================================
echo   启动开发环境   %WEB_DEV%
echo   MySQL 3306  +  后端 5382 (run.py 自动重载)  +  Vite 5173
echo ============================================================
echo.
echo 注意：生产环境的后端也占 5382，启动开发会先结束它。
echo.
echo [1/3] MySQL 3306 ...
netstat -ano | findstr ":3306" | findstr "LISTENING" >nul
if errorlevel 1 (
    net start MySQL84
    if errorlevel 1 (
        echo     [失败] 见 %MYSQL_ERR%
    ) else (
        echo     MySQL 已启动
    )
) else (
    echo     MySQL 已在运行，跳过
)

echo [2/3] 后端 5382（Flask debug，改代码自动重载）...
call :stop_backend_quiet
start "cls_svr 开发 5382" cmd /k "cd /d %PROJECT% && .venv\Scripts\python.exe run.py"
timeout /t 3 >nul
netstat -ano | findstr ":5382" | findstr "LISTENING" >nul
if errorlevel 1 (
    echo     [警告] 5382 未监听，看后端窗口报错
) else (
    echo     后端已就绪
)

echo [3/3] Vite 5173 ...
netstat -ano | findstr ":5173" | findstr "LISTENING" >nul
if not errorlevel 1 (
    echo     Vite 已在运行，跳过
    goto :dev_ready
)
start "cls_clt Vite 5173" cmd /k "cd /d %CLT% && npm run dev"
set "WAIT=0"
:wait_vite
timeout /t 1 >nul
netstat -ano | findstr ":5173" | findstr "LISTENING" >nul
if not errorlevel 1 goto :dev_ready
set /a WAIT+=1
if %WAIT% lss 20 goto :wait_vite
echo     [警告] 20 秒内 5173 未监听，看 Vite 窗口报错
goto :done

:dev_ready
echo     Vite 已就绪
echo.
echo 打开 %WEB_DEV%
start "" %WEB_DEV%
goto :done

rem ==================== 4. 停止开发 ====================
:stop_dev
cls
echo ============================================================
echo   停止开发环境
echo ============================================================
echo.
echo [1/3] Vite 5173 ...
set "FOUND="
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5173" ^| findstr "LISTENING"') do (
    taskkill /PID %%a /T /F >nul 2>&1
    set "FOUND=1"
    echo     已结束 PID %%a
)
if not defined FOUND echo     未运行

echo [2/3] 后端 5382 ...
call :stop_backend

echo [3/3] MySQL84 ...
net stop MySQL84 >nul 2>&1
if errorlevel 1 (
    echo     未运行或停止失败
) else (
    echo     MySQL 已停止
)

echo.
echo 已停止。
goto :done

rem ==================== 5. 仅启动 MySQL ====================
:start_mysql
cls
echo ============================================================
echo   MySQL 3306
echo ============================================================
echo.
netstat -ano | findstr ":3306" | findstr "LISTENING" >nul
if not errorlevel 1 (
    echo [1/2] 已在监听，跳过启动
    goto :mysql_report
)

echo [1/2] 启动服务 MySQL84 ...
net start MySQL84
if errorlevel 1 (
    echo.
    echo [失败] 服务未能启动，按以下顺序排查：
    echo   1. 残留进程： tasklist ^| findstr mysqld
    echo   2. 错误日志： %MYSQL_ERR%
    echo   3. 配置文件： D:\System\MySQL server\my.ini
    echo   4. 数据目录： D:\Cache\MySQL84_Data
    goto :done
)

:mysql_report
echo [2/2] 检查端口 3306 ...
timeout /t 2 >nul
netstat -ano | findstr ":3306" | findstr "LISTENING" >nul
if errorlevel 1 (
    echo [警告] 服务已启动但 3306 未监听，请查看 %MYSQL_ERR%
) else (
    echo [成功] 127.0.0.1:3306 已就绪
)
echo.
echo 数据库：classicsdb    账号：root
echo MySQL 在后台常驻，关闭本窗口不影响运行
goto :done

rem ==================== 6. 仅重启 Apache ====================
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

rem ==================== 7. 查看状态 ====================
:status
cls
echo ============================================================
echo   运行状态
echo ============================================================
echo.
echo --- 端口 ---
netstat -ano | findstr ":3306" | findstr "LISTENING" >nul
if errorlevel 1 (echo   3306  MySQL       未监听) else (echo   3306  MySQL       正常)
netstat -ano | findstr ":5382" | findstr "LISTENING" >nul
if errorlevel 1 (echo   5382  后端        未监听) else (echo   5382  后端        正常)
netstat -ano | findstr ":8088" | findstr "LISTENING" >nul
if errorlevel 1 (echo   8088  Apache生产  未监听) else (echo   8088  Apache生产  正常)
netstat -ano | findstr ":5173" | findstr "LISTENING" >nul
if errorlevel 1 (echo   5173  Vite开发    未监听) else (echo   5173  Vite开发    正常)

echo.
echo --- 5382 占用 ---
netstat -ano | findstr ":5382" | findstr "LISTENING" >nul
if errorlevel 1 (
    echo   后端未运行
) else (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5382" ^| findstr "LISTENING"') do (
        echo   PID = %%a
    )
)

echo.
echo --- 服务 ---
sc query MySQL84 | findstr "STATE"
sc query apache2.4 | findstr "STATE"

echo.
echo --- 接口自检 ---
curl -s -o nul -w "   5382/api      HTTP %%{http_code}\n" http://127.0.0.1:5382/api/classics/get-classictypes
curl -s -o nul -w "   8088/svr/api  HTTP %%{http_code}\n" http://127.0.0.1:8088/svr/api/classics/get-classictypes
goto :done

rem ==================== 8. 启用 mod_wsgi ====================
:modwsgi
cls
echo ============================================================
echo   启用 mod_wsgi（教材 9.3.2 / 9.3.3）
echo   装 VS 生成工具 - 编译 mod_wsgi - 改 httpd.conf - 重启 Apache
echo ============================================================
echo.
echo 注意：切换后后端由 Apache 直接加载，run_prod.py 与 run.py 都不再需要。
echo       回退： cls_svr\.venv\Scripts\python.exe cls_svr\deploy\switch_to_mod_wsgi.py --revert
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
        echo     [错误] 安装失败。可手动安装：https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/
        echo            勾选「使用 C++ 的桌面开发」，装完重新运行本脚本。
        goto :done
    )
    echo     安装完成
)

echo [2/4] 编译安装 mod_wsgi ...
set MOD_WSGI_APACHE_ROOTDIR=%APACHE_HOME%
"%PROJECT%\.venv\Scripts\python.exe" -m pip install mod_wsgi
if errorlevel 1 (
    echo     [错误] mod_wsgi 编译失败，请把上面的报错发出来
    goto :done
)

echo [3/4] 修改 httpd.conf ...
"%PROJECT%\.venv\Scripts\python.exe" "%PROJECT%\deploy\switch_to_mod_wsgi.py"
if errorlevel 1 (
    echo     [错误] 配置切换失败，回滚： deploy\switch_to_mod_wsgi.py --revert
    goto :done
)

echo [4/4] 重启 Apache 服务 ...
"%APACHE_HOME%\bin\httpd.exe" -k restart -n "apache2.4"
if errorlevel 1 (
    echo     服务未运行，尝试启动 ...
    "%APACHE_HOME%\bin\httpd.exe" -k start -n "apache2.4"
)
timeout /t 3 >nul

echo.
echo 验证接口：
curl -s -o nul -w "   8088 /api = %%{http_code}\n" http://127.0.0.1:8088/svr/api/classics/get-classictypes
echo.
echo 完成。若接口正常返回 JSON，说明 mod_wsgi 已生效。
goto :done

rem ==================== 子过程：后端 ====================
:stop_backend_quiet
netstat -ano | findstr ":5382" | findstr "LISTENING" >nul
if errorlevel 1 goto :eof
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5382" ^| findstr "LISTENING"') do (
    taskkill /PID %%a /T /F >nul 2>&1
)
timeout /t 2 >nul
goto :eof

:stop_backend
set "FOUND="
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5382" ^| findstr "LISTENING"') do (
    taskkill /PID %%a /T /F >nul 2>&1
    set "FOUND=1"
    echo     已结束 PID %%a
)
timeout /t 2 >nul
rem 复检：Flask debug 的 reloader 会重新拉起子进程
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5382" ^| findstr "LISTENING"') do (
    taskkill /PID %%a /T /F >nul 2>&1
    echo     已结束重启的 PID %%a
)
if not defined FOUND echo     未运行
goto :eof

rem ==================== 子过程：Apache ====================
:ensure_apache
netstat -ano | findstr ":8088" | findstr "LISTENING" >nul
if not errorlevel 1 (
    echo     Apache 已在运行，跳过
    goto :eof
)
sc query apache2.4 2>nul | findstr /I "RUNNING" >nul
if not errorlevel 1 (
    echo     服务已运行但 8088 未监听，重启服务 ...
    "%APACHE_HOME%\bin\httpd.exe" -k restart -n "apache2.4"
    timeout /t 2 >nul
    goto :eof
)
sc query apache2.4 >nul 2>&1
if errorlevel 1 (
    start "Apache 8088" cmd /k "cd /d %APACHE_HOME%\bin && httpd.exe -D FOREGROUND"
    echo     Apache 前台启动（新窗口，未安装服务）
) else (
    net start apache2.4 >nul
    echo     Apache 服务已启动
)
timeout /t 2 >nul
netstat -ano | findstr ":8088" | findstr "LISTENING" >nul
if errorlevel 1 (
    echo     [警告] 8088 仍未监听，检查 httpd.conf 与错误日志
) else (
    echo     [成功] 8088 已就绪
)
goto :eof

:stop_apache
sc query apache2.4 >nul 2>&1
if errorlevel 1 (
    tasklist /FI "IMAGENAME eq httpd.exe" 2>nul | find /I "httpd.exe" >nul
    if errorlevel 1 (
        echo     Apache 未在运行
    ) else (
        taskkill /IM httpd.exe /F >nul 2>&1
        echo     已结束后台 httpd 进程
    )
) else (
    net stop apache2.4 >nul 2>&1
    if errorlevel 1 (
        echo     [提示] apache2.4 停止失败或本就未运行
    ) else (
        echo     服务 apache2.4 已停止
    )
)
goto :eof

rem ==================== 结束 ====================
:done
echo.
echo ------------------------------------------------------------
pause
goto :menu

:end
endlocal
exit /b 0
