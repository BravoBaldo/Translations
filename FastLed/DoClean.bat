Echo OFF
Echo ****************************************
Echo To Run before publish on git
Echo ****************************************

REM This is so as not to erase myself!
IF NOT EXIST ".\FastLed\FastLED\" (
rmdir /S /Q FastLED
rmdir /S /Q FastLED_Sphinx
rmdir /S /Q .\FastLED_Italiano\gettext
move .\FastLED_Italiano\latex\it\*.pdf .\FastLED_Italiano\latex\
rmdir /S /Q .\FastLED_Italiano\latex\it

move .\FastLED_Italiano\epub\it\*.epub .\FastLED_Italiano\epub\
rmdir /S /Q .\FastLED_Italiano\epub\it

REM copy .\FastLED_OmegaT\target\README.md             .\FastLED_Italiano\README_it.md
REM copy .\FastLED_OmegaT\target\CODE_OF_CONDUCT.md    .\FastLED_Italiano\CODE_OF_CONDUCT_it.md

del /S /Q   .\FastLED_OmegaT\omegat\*.bak
del /S /Q   .\FastLED_OmegaT\*.bak
del /S /Q   .\FastLED_OmegaT\target\FastLED\it\LC_MESSAGES\*.mo
)
Echo ********************
Echo * Ready for commit *
Echo ********************
