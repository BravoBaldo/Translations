Rem Step 1: Prepare Environment
Call DoSetEnv.bat
if  errorlevel 1 goto ERROR

Rem Step 2: Translate with OmegaT

Rem Step 3: Make Html, epub, pdf etc. 
Call ..\DoTranslate.bat
goto :EOF


:ERROR
exit /b 1



:EOF 