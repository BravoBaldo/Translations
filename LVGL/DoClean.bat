ECHO To Run before publish on git
REM This is so as not to erase myself!
IF NOT EXIST ".\LVGL\lvgl\" (
rmdir /S /Q lvgl
rmdir /S /Q Sphinx_LVGL
rmdir /S /Q .\LVGL_Italiano\gettext
move .\LVGL_Italiano\latex\it\LVGL_*.pdf .\LVGL_Italiano\latex\
rmdir /S /Q .\LVGL_Italiano\latex\it

move .\LVGL_Italiano\epub\it\LVGL_*.epub .\LVGL_Italiano\epub\
rmdir /S /Q .\LVGL_Italiano\epub\it

del /S /Q   .\LVGL_TradIta\omegat\*.bak
del /S /Q   .\LVGL_TradIta\*.bak
del /S /Q   .\LVGL_TradIta\target\it\LC_MESSAGES\*.mo
)
