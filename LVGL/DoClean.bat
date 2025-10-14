Echo OFF
Echo ****************************************
Echo To Run before publish on git
Echo ****************************************

REM This is so as not to erase myself!
IF NOT EXIST ".\LVGL\lvgl\" (
rmdir /S /Q lvgl
rmdir /S /Q Sphinx_LVGL
rmdir /S /Q .\LVGL_Italiano\gettext
move .\LVGL_Italiano\latex\it\LVGL_*.pdf .\LVGL_Italiano\latex\
rmdir /S /Q .\LVGL_Italiano\latex\it

rmdir /S /Q Tools\.idea

move .\LVGL_Italiano\epub\it\LVGL_*.epub .\LVGL_Italiano\epub\
rmdir /S /Q .\LVGL_Italiano\epub\it

copy .\LVGL_TradIta\target\README.md             .\LVGL_Italiano\README_it.md
copy .\LVGL_TradIta\target\CODE_OF_CONDUCT.md    .\LVGL_Italiano\CODE_OF_CONDUCT_it.md

del /S /Q   .\LVGL_TradIta\omegat\*.bak
del /S /Q   .\LVGL_TradIta\*.bak
del /S /Q   .\LVGL_TradIta\target\it\LC_MESSAGES\*.mo
)
Echo ********************
Echo * Ready for commit *
Echo ********************
