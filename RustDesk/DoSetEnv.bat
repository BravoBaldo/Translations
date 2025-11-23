@echo off
cls
rmdir /S /Q doc.rustdesk.com > NUL
rmdir /S /Q RustDesk_Sphinx  > NUL
rmdir /S /Q RustDesk_Italiano & mkdir RustDesk_Italiano  > NUL

git clone https://github.com/rustdesk/doc.rustdesk.com.git

"%LOCALAPPDATA%\Apps\grepWin\grepWin.exe" /regex:no /searchfor:".jpg?v2"          /searchpath:"%~dp0doc.rustdesk.com\content" /replacewith:".jpg" /u:yes /filemask:"*.md"  /executereplace /k:no /closedialog
"%LOCALAPPDATA%\Apps\grepWin\grepWin.exe" /regex:no /searchfor:".jpg?width=300px" /searchpath:"%~dp0doc.rustdesk.com\content" /replacewith:".jpg" /u:yes /filemask:"*.md"  /executereplace /k:no /closedialog
"%LOCALAPPDATA%\Apps\grepWin\grepWin.exe" /regex:no /searchfor:".png?v2"          /searchpath:"%~dp0doc.rustdesk.com\content" /replacewith:".png" /u:yes /filemask:"*.md"  /executereplace /k:no /closedialog
"%LOCALAPPDATA%\Apps\grepWin\grepWin.exe" /regex:no /searchfor:".png?v3"          /searchpath:"%~dp0doc.rustdesk.com\content" /replacewith:".png" /u:yes /filemask:"*.md"  /executereplace /k:no /closedialog
"%LOCALAPPDATA%\Apps\grepWin\grepWin.exe" /regex:no /searchfor:".png?width=300px" /searchpath:"%~dp0doc.rustdesk.com\content" /replacewith:".png" /u:yes /filemask:"*.md"  /executereplace /k:no /closedialog
"%LOCALAPPDATA%\Apps\grepWin\grepWin.exe" /regex:no /searchfor:".png?width=700px" /searchpath:"%~dp0doc.rustdesk.com\content" /replacewith:".png" /u:yes /filemask:"*.md"  /executereplace /k:no /closedialog

mkdir RustDesk_Sphinx && cd RustDesk_Sphinx
sphinx-quickstart --sep -p "RustDesk" -a "RustDesk Community" -r "2025" -l "it" --extensions "myst_parser"
rmdir /s /Q build
mklink /D "build"      "..\RustDesk_Italiano"


echo version = '2025' >> "source\conf.py"
echo suppress_warnings = ('myst.xref_missing','myst.header','misc.highlighting_failure','toc.not_included','toc.not_readable','toc.no_title') >> "source\conf.py"


mkdir  .\source\docs\en\client
mkdir  .\source\docs\en\client\android
mkdir ".\source\docs\en\client\mac"
mkdir ".\source\docs\en\client\windows\windows-portable-elevation"
mkdir ".\source\docs\en\self-host\client-configuration"
mkdir ".\source\docs\en\self-host\client-configuration\advanced-settings"
mkdir ".\source\docs\en\self-host\nat-loopback-issues"
mkdir ".\source\docs\en\self-host\rustdesk-server-oss\install"
mkdir ".\source\docs\en\self-host\rustdesk-server-oss\synology\dsm-6"
mkdir ".\source\docs\en\self-host\rustdesk-server-oss\synology\dsm-7"
mkdir ".\source\docs\en\self-host\rustdesk-server-pro\2fa"
mkdir ".\source\docs\en\self-host\rustdesk-server-pro\console"
mkdir ".\source\docs\en\self-host\rustdesk-server-pro\faq"
mkdir ".\source\docs\en\self-host\rustdesk-server-pro\ldap"
mkdir ".\source\docs\en\self-host\rustdesk-server-pro\license"
mkdir ".\source\docs\en\self-host\rustdesk-server-pro\oidc\azure"
mkdir ".\source\docs\en\self-host\rustdesk-server-pro\permissions"
mkdir ".\source\docs\en\self-host\rustdesk-server-pro\strategy"
mkdir ".\source\docs\en\dev\build\windows"


mklink /D ".\source\docs\en\client\images"                                            "..\..\..\..\..\doc.rustdesk.com\content\client\images"
mklink /D ".\source\docs\en\client\android\images"                                    "..\..\..\..\..\..\doc.rustdesk.com\content\client\android\images"
mklink /D ".\source\docs\en\client\mac\images"                                        "..\..\..\..\..\..\doc.rustdesk.com\content\client\mac\images"
mklink /D ".\source\docs\en\client\windows\windows-portable-elevation\images"         "..\..\..\..\..\..\..\doc.rustdesk.com\content\client\windows\windows-portable-elevation\images"
mklink /D ".\source\docs\en\self-host\client-configuration\images"                    "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\client-configuration\images"
mklink /D ".\source\docs\en\self-host\client-configuration\advanced-settings\images"  "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\client-configuration\advanced-settings\images"
mklink /D ".\source\docs\en\self-host\nat-loopback-issues\images"                     "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\nat-loopback-issues\images"
mklink /D ".\source\docs\en\self-host\rustdesk-server-oss\install\images"             "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-oss\install\images"
mklink /D ".\source\docs\en\self-host\rustdesk-server-oss\synology\dsm-6\images"      "..\..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-oss\synology\dsm-6\images"
mklink /D ".\source\docs\en\self-host\rustdesk-server-oss\synology\dsm-7\images"      "..\..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-oss\synology\dsm-7\images"
mklink /D ".\source\docs\en\self-host\rustdesk-server-pro\2fa\images"                 "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\2fa\images"
mklink /D ".\source\docs\en\self-host\rustdesk-server-pro\console\images"             "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\console\images"
mklink /D ".\source\docs\en\self-host\rustdesk-server-pro\faq\images"                 "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\faq\images"
mklink /D ".\source\docs\en\self-host\rustdesk-server-pro\ldap\images"                "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\ldap\images"
mklink /D ".\source\docs\en\self-host\rustdesk-server-pro\license\images"             "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\license\images"
mklink /D ".\source\docs\en\self-host\rustdesk-server-pro\oidc\azure\images"          "..\..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\oidc\azure\images"
mklink /D ".\source\docs\en\self-host\rustdesk-server-pro\permissions\images"         "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\permissions\images"
mklink /D ".\source\docs\en\self-host\rustdesk-server-pro\strategy\images"            "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\strategy\images"
mklink /D ".\source\docs\en\dev\build\windows\images"                                 "..\..\..\..\..\..\..\doc.rustdesk.com\content\dev\build\windows\images"


mklink ".\source\LICENSE.md"                          "..\..\doc.rustdesk.com\LICENSE.md"
mklink ".\source\README.md"                           "..\..\doc.rustdesk.com\README.md"

mkdir .\source\content
mklink ".\source\content\_index.it.md"                    "..\..\..\doc.rustdesk.com\content\_index.it.md"

mkdir .\source\content\client
mklink    ".\source\content\client\_index.it.md"              "..\..\..\..\doc.rustdesk.com\content\client\_index.it.md"
mklink /D ".\source\content\client\images"                    "..\..\..\..\doc.rustdesk.com\content\client\images"

mkdir .\source\content\client\android\
mklink    ".\source\content\client\android\_index.it.md"       "..\..\..\..\..\doc.rustdesk.com\content\client\android\_index.it.md"
mklink /D ".\source\content\client\android\images"             "..\..\..\..\..\doc.rustdesk.com\content\client\android\images"

mkdir .\source\content\client\linux\
mklink    ".\source\content\client\linux\_index.it.md"       "..\..\..\..\..\doc.rustdesk.com\content\client\linux\_index.it.md"

mkdir .\source\content\client\mac\
mklink    ".\source\content\client\mac\_index.it.md"       "..\..\..\..\..\doc.rustdesk.com\content\client\mac\_index.it.md"
mklink /D ".\source\content\client\mac\images"             "..\..\..\..\..\doc.rustdesk.com\content\client\mac\images"

mkdir .\source\content\client\windows\
mklink    ".\source\content\client\windows\_index.it.md"       "..\..\..\..\..\doc.rustdesk.com\content\client\windows\_index.it.md"

mkdir .\source\content\client\windows\MSI
mklink    ".\source\content\client\windows\MSI\_index.it.md"       "..\..\..\..\..\..\doc.rustdesk.com\content\client\windows\MSI\_index.it.md"

mkdir .\source\content\client\windows\windows-portable-elevation
mklink    ".\source\content\client\windows\windows-portable-elevation\_index.it.md"       "..\..\..\..\..\..\doc.rustdesk.com\content\client\windows\windows-portable-elevation\_index.it.md"
mklink  /D  ".\source\content\client\windows\windows-portable-elevation\images"       "..\..\..\..\..\..\doc.rustdesk.com\content\client\windows\windows-portable-elevation\images"

mkdir .\source\content\self-host
mklink    ".\source\content\self-host\_index.it.md"              "..\..\..\..\doc.rustdesk.com\content\self-host\_index.it.md"

mkdir .\source\content\self-host\client-configuration
mklink    ".\source\content\self-host\client-configuration\_index.it.md"        "..\..\..\..\..\doc.rustdesk.com\content\self-host\client-configuration\_index.it.md"
mklink /D ".\source\content\self-host\client-configuration\images"              "..\..\..\..\..\doc.rustdesk.com\content\self-host\client-configuration\images"

mkdir .\source\content\self-host\client-configuration\advanced-settings
mklink    ".\source\content\self-host\client-configuration\advanced-settings\_index.it.md"        "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\client-configuration\advanced-settings\_index.it.md"
mklink /D ".\source\content\self-host\client-configuration\advanced-settings\images"              "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\client-configuration\advanced-settings\images"

mkdir .\source\content\self-host\client-deployment
mklink    ".\source\content\self-host\client-deployment\_index.it.md"        "..\..\..\..\..\doc.rustdesk.com\content\self-host\client-deployment\_index.it.md"

mkdir .\source\content\self-host\nat-loopback-issues
mklink    ".\source\content\self-host\nat-loopback-issues\_index.it.md"        "..\..\..\..\..\doc.rustdesk.com\content\self-host\nat-loopback-issues\_index.it.md"
mklink /D ".\source\content\self-host\nat-loopback-issues\images"              "..\..\..\..\..\doc.rustdesk.com\content\self-host\nat-loopback-issues\images"

mkdir .\source\content\self-host\rustdesk-server-oss
mklink    ".\source\content\self-host\rustdesk-server-oss\_index.it.md"        "..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-oss\_index.it.md"

mkdir .\source\content\self-host\rustdesk-server-oss\Docker
mklink    ".\source\content\self-host\rustdesk-server-oss\Docker\_index.it.md"  "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-oss\Docker\_index.it.md"

mkdir .\source\content\self-host\rustdesk-server-oss\install
mklink    ".\source\content\self-host\rustdesk-server-oss\install\_index.it.md"        "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-oss\install\_index.it.md"
mklink /D ".\source\content\self-host\rustdesk-server-oss\install\images"        "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-oss\install\images"

mkdir .\source\content\self-host\rustdesk-server-oss\synology
mklink    ".\source\content\self-host\rustdesk-server-oss\synology\_index.it.md"        "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-oss\synology\_index.it.md"

mkdir .\source\content\self-host\rustdesk-server-oss\synology\dsm-6
mklink    ".\source\content\self-host\rustdesk-server-oss\synology\dsm-6\_index.it.md"  "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-oss\synology\dsm-6\_index.it.md"
mklink /D ".\source\content\self-host\rustdesk-server-oss\synology\dsm-6\images"        "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-oss\synology\dsm-6\images"

mkdir .\source\content\self-host\rustdesk-server-oss\synology\dsm-7
mklink    ".\source\content\self-host\rustdesk-server-oss\synology\dsm-7\_index.it.md"  "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-oss\synology\dsm-7\_index.it.md"
mklink /D ".\source\content\self-host\rustdesk-server-oss\synology\dsm-7\images"        "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-oss\synology\dsm-7\images"

mkdir .\source\content\self-host\rustdesk-server-oss\windows
mklink    ".\source\content\self-host\rustdesk-server-oss\windows\_index.it.md"        "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-oss\windows\_index.it.md"

mkdir .\source\content\self-host\rustdesk-server-pro
mklink    ".\source\content\self-host\rustdesk-server-pro\_index.it.md"        "..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\_index.it.md"

mkdir .\source\content\self-host\rustdesk-server-pro\2fa
mklink    ".\source\content\self-host\rustdesk-server-pro\2fa\_index.it.md"  "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\2fa\_index.it.md"
mklink /D ".\source\content\self-host\rustdesk-server-pro\2fa\images"        "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\2fa\images"

mkdir .\source\content\self-host\rustdesk-server-pro\console
mklink    ".\source\content\self-host\rustdesk-server-pro\console\_index.it.md"  "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\console\_index.it.md"
mklink /D ".\source\content\self-host\rustdesk-server-pro\console\images"        "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\console\images"

mkdir .\source\content\self-host\rustdesk-server-pro\faq
mklink    ".\source\content\self-host\rustdesk-server-pro\faq\_index.it.md"  "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\faq\_index.it.md"
mklink /D ".\source\content\self-host\rustdesk-server-pro\faq\images"        "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\faq\images"

mkdir .\source\content\self-host\rustdesk-server-pro\installscript
mklink    ".\source\content\self-host\rustdesk-server-pro\installscript\_index.it.md"  "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\installscript\_index.it.md"

mkdir .\source\content\self-host\rustdesk-server-pro\installscript\Docker
mklink    ".\source\content\self-host\rustdesk-server-pro\installscript\Docker\_index.it.md"  "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\installscript\Docker\_index.it.md"

mkdir .\source\content\self-host\rustdesk-server-pro\installscript\Script
mklink    ".\source\content\self-host\rustdesk-server-pro\installscript\Script\_index.it.md"  "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\installscript\Script\_index.it.md"

mkdir .\source\content\self-host\rustdesk-server-pro\installscript\windows
mklink    ".\source\content\self-host\rustdesk-server-pro\installscript\windows\_index.it.md"  "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\installscript\windows\_index.it.md"


mkdir .\source\content\self-host\rustdesk-server-pro\ldap
mklink    ".\source\content\self-host\rustdesk-server-pro\ldap\_index.it.md"  "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\ldap\_index.it.md"
mklink /D ".\source\content\self-host\rustdesk-server-pro\ldap\images"        "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\ldap\images"

mkdir .\source\content\self-host\rustdesk-server-pro\license
mklink    ".\source\content\self-host\rustdesk-server-pro\license\_index.it.md"  "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\license\_index.it.md"
mklink /D ".\source\content\self-host\rustdesk-server-pro\license\images"        "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\license\images"

mkdir .\source\content\self-host\rustdesk-server-pro\oidc
mklink    ".\source\content\self-host\rustdesk-server-pro\oidc\_index.it.md"  "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\oidc\_index.it.md"

mkdir .\source\content\self-host\rustdesk-server-pro\oidc\azure
mklink    ".\source\content\self-host\rustdesk-server-pro\oidc\azure\_index.it.md"  "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\oidc\azure\_index.it.md"
mklink /D ".\source\content\self-host\rustdesk-server-pro\oidc\azure\images"        "..\..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\oidc\azure\images"

mkdir .\source\content\self-host\rustdesk-server-pro\permissions
mklink    ".\source\content\self-host\rustdesk-server-pro\permissions\_index.it.md"  "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\permissions\_index.it.md"
mklink /D ".\source\content\self-host\rustdesk-server-pro\permissions\images"        "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\permissions\images"

mkdir .\source\content\self-host\rustdesk-server-pro\relay
mklink    ".\source\content\self-host\rustdesk-server-pro\relay\_index.it.md"     "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\relay\_index.it.md"

mkdir .\source\content\self-host\rustdesk-server-pro\smtp
mklink    ".\source\content\self-host\rustdesk-server-pro\smtp\_index.it.md"      "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\smtp\_index.it.md"

mkdir .\source\content\self-host\rustdesk-server-pro\strategy
mklink    ".\source\content\self-host\rustdesk-server-pro\strategy\_index.it.md"  "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\strategy\_index.it.md"
mklink /D ".\source\content\self-host\rustdesk-server-pro\strategy\images"        "..\..\..\..\..\..\doc.rustdesk.com\content\self-host\rustdesk-server-pro\strategy\images"

mkdir .\source\content\videos
mklink    ".\source\content\videos\_index.it.md"              "..\..\..\..\doc.rustdesk.com\content\videos\_index.it.md"


mkdir      .\source\content\dev
mklink    ".\source\content\dev\_index.it.md"              "..\..\..\..\doc.rustdesk.com\content\dev\_index.it.md"

mkdir      .\source\content\dev\build
mklink    ".\source\content\dev\build\_index.it.md"       "..\..\..\..\..\doc.rustdesk.com\content\dev\build\_index.it.md"

mkdir      .\source\content\dev\build\faq
mklink    ".\source\content\dev\build\faq\_index.it.md"       "..\..\..\..\..\..\doc.rustdesk.com\content\dev\build\faq\_index.it.md"

mkdir      .\source\content\dev\build\linux
mklink    ".\source\content\dev\build\linux\_index.it.md"       "..\..\..\..\..\..\doc.rustdesk.com\content\dev\build\linux\_index.it.md"

mkdir      .\source\content\dev\build\osx
mklink    ".\source\content\dev\build\osx\_index.it.md"       "..\..\..\..\..\..\doc.rustdesk.com\content\dev\build\osx\_index.it.md"

mkdir      .\source\content\dev\build\windows
mklink    ".\source\content\dev\build\windows\_index.it.md"       "..\..\..\..\..\..\doc.rustdesk.com\content\dev\build\windows\_index.it.md"
mklink /D ".\source\content\dev\build\windows\images"             "..\..\..\..\..\..\doc.rustdesk.com\content\dev\build\windows\images"



CLS
call make clean
call make epub
Echo ****************************************
Echo For HTML see https://rustdesk.com/docs/it/
Echo ****************************************
REM call make latex			REM ToDo	
Echo.
Echo ****************************************
Echo Create pdf...This function is postponed
REM PUSHD .\build\latex
REM FOR /R  %%F in (RustDesk*.tex) do lualatex --interaction=nonstopmode %%~F
REM FOR /R  %%F in (RustDesk*.tex) do lualatex --interaction=nonstopmode %%~F
REM POPD
Echo ****************************************
Echo.

echo on
cls

cd ..

move .\RustDesk_Italiano\latex\RustDesk*.pdf .\RustDesk_Italiano
move .\RustDesk_Italiano\epub\RustDesk*.epub .\RustDesk_Italiano

rmdir /S /Q doc.rustdesk.com > NUL
rmdir /S /Q RustDesk_Sphinx  > NUL



rmdir /S /Q .\RustDesk_Italiano\doctrees
rmdir /S /Q .\RustDesk_Italiano\latex
rmdir /S /Q .\RustDesk_Italiano\epub


goto :eof
