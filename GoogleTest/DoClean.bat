Echo OFF
Echo ****************************************
Echo To Run before publish on git
Echo ****************************************

REM This is so as not to erase myself!
REM IF NOT EXIST ".\\GoogleTest\googletest\" (
rmdir /S /Q googletest
rmdir /S /Q GoogleTest_Sphinx
rmdir /S /Q .\GoogleTest_Italiano\gettext
move .\GoogleTest_Italiano\latex\it\GoogleTest_*.pdf .\GoogleTest_Italiano\latex\
rmdir /S /Q .\GoogleTest_Italiano\latex\it

move .\GoogleTest_Italiano\epub\it\GoogleTest_*.epub .\GoogleTest_Italiano\epub\
rmdir /S /Q .\GoogleTest_Italiano\epub\it

del /S /Q   .\GoogleTest_OmegaT\omegat\*.bak
del /S /Q   .\GoogleTest_OmegaT\*.bak
del /S /Q   .\GoogleTest_OmegaT\target\it\LC_MESSAGES\*.mo
REM )
Echo ********************
Echo * Ready for commit *
Echo ********************
