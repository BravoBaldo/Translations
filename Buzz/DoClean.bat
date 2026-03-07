Echo OFF
Echo ****************************************
Echo To Run before publish on git
Echo ****************************************

REM This is so as not to erase myself!
REM IF NOT EXIST ".\Buzz\buzz\" (
rmdir /S /Q buzz
rmdir /S /Q Buzz_Sphinx
rmdir /S /Q .\Buzz_Italiano\gettext
move .\Buzz_Italiano\latex\it\*.pdf .\Buzz_Italiano\latex\
rmdir /S /Q .\Buzz_Italiano\latex\it

rmdir /S /Q Tools\.idea

move .\Buzz_Italiano\epub\it\*.epub .\Buzz_Italiano\epub\
rmdir /S /Q .\Buzz_Italiano\epub\it

del /S /Q   .\Buzz_OmegaT\omegat\*.bak
del /S /Q   .\Buzz_OmegaT\*.bak
del /S /Q   .\Buzz_OmegaT\target\it\LC_MESSAGES\*.mo
REM )
Echo ********************
Echo * Ready for commit *
Echo ********************
