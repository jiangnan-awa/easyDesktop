@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo 开始执行打包脚本
echo ========================================
echo.

:: 记录脚本所在目录
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: 步骤1: 运行第一个PyInstaller命令
echo [步骤1/5] 正在使用PyInstaller打包easyDesktop.py...
pyinstaller -w -i favicon.ico easyDesktop.py --add-data "ed/Lib/site-packages/pythonnet/runtime;pythonnet/runtime" --hidden-import "clr" --hidden-import "tkinter" --hidden-import "System" --hidden-import "System.Runtime" --hidden-import=webview.platforms.win32 --hidden-import=webview

if %errorlevel% neq 0 (
    echo [错误] PyInstaller打包失败，错误代码: %errorlevel%
    pause
    exit /b %errorlevel%
)
echo [成功] PyInstaller打包完成
echo.

:: 步骤2: 创建目标目录（如果不存在）
echo [步骤2/5] 准备目标目录...
if not exist "dist\easyDesktop\_internal" (
    mkdir "dist\easyDesktop\_internal" 2>nul
)
echo [成功] 目录准备完成
echo.

:: 步骤3: 复制文件和文件夹
echo [步骤3/5] 开始复制文件...

:: 复制/resources文件夹
if exist "resources" (
    xcopy /E /I /Y "resources" "dist\easyDesktop\_internal\resources"
    if !errorlevel! neq 0 (
        echo [警告] 复制resources文件夹时出现问题
    ) else (
        echo [成功] 已复制 resources 文件夹
    )
) else (
    echo [警告] 找不到 resources 文件夹，跳过
)

:: 复制/theme文件夹
if exist "theme" (
    xcopy /E /I /Y "theme" "dist\easyDesktop\_internal\theme"
    if !errorlevel! neq 0 (
        echo [警告] 复制theme文件夹时出现问题
    ) else (
        echo [成功] 已复制 theme 文件夹
    )
) else (
    echo [警告] 找不到 theme 文件夹，跳过
)

:: 复制 easyFileDesk.html
if exist "easyFileDesk.html" (
    copy /Y "easyFileDesk.html" "dist\easyDesktop\_internal\"
    echo [成功] 已复制 easyFileDesk.html
) else (
    echo [警告] 找不到 easyFileDesk.html，跳过
)

:: 复制 ed_logo.png 到 _internal 目录
if exist "ed_logo.png" (
    copy /Y "ed_logo.png" "dist\easyDesktop\_internal\"
    echo [成功] 已复制 ed_logo.png 到 _internal 目录
) else (
    echo [警告] 找不到 ed_logo.png，跳过
)

:: 复制 favicon.ico 到 _internal 目录
if exist "favicon.ico" (
    copy /Y "favicon.ico" "dist\easyDesktop\_internal\"
    echo [成功] 已复制 favicon.ico 到 _internal 目录
) else (
    echo [警告] 找不到 favicon.ico，跳过
)

:: 单独复制 ed_logo.png 到 /dist/easyDesktop 目录
if exist "ed_logo.png" (
    copy /Y "ed_logo.png" "dist\easyDesktop\"
    echo [成功] 已复制 ed_logo.png 到 easyDesktop 根目录
) else (
    echo [警告] 找不到 ed_logo.png，跳过
)

echo.
echo [步骤3/5] 文件复制完成
echo.

:: 步骤4: 打包成ZIP
echo [步骤4/5] 正在打包为ZIP文件...

:: 创建res目录（如果不存在）
if not exist "res" (
    mkdir "res"
    echo [信息] 已创建 res 目录
)

:: 删除已存在的zip文件（避免冲突）
if exist "res\easyDesktop.zip" (
    del /F /Q "res\easyDesktop.zip"
    echo [信息] 已删除旧的 easyDesktop.zip
)

:: 使用PowerShell压缩（Windows原生支持）
set "source_path=%SCRIPT_DIR%dist\easyDesktop"
set "dest_path=%SCRIPT_DIR%res\easyDesktop.zip"

PowerShell -Command "& { Compress-Archive -Path '%source_path%' -DestinationPath '%dest_path%' -Force; if ($?) { exit 0 } else { exit 1 } }"

if %errorlevel% neq 0 (
    echo [错误] 打包ZIP失败
    pause
    exit /b %errorlevel%
)

echo [成功] 已创建压缩包: res\easyDesktop.zip
echo.

:: 步骤5: 运行第二个PyInstaller命令
echo [步骤5/5] 正在使用PyInstaller打包easyDesktop_Installer.py...
pyinstaller -F -w -i favicon.ico --add-data "res;res" easyDesktop_Installer.py

if %errorlevel% neq 0 (
    echo [错误] PyInstaller打包安装程序失败，错误代码: %errorlevel%
    pause
    exit /b %errorlevel%
)
echo [成功] 安装程序打包完成
echo.

:: 完成
echo ========================================
echo 所有步骤执行完成！
echo ========================================
echo.
echo 生成的文件位置：
echo - 程序文件: dist\easyDesktop\
echo - 压缩包: res\easyDesktop.zip
echo - 安装程序: dist\easyDesktop_Installer.exe
echo.

pause