Echo OFF
Echo ****************************************
Echo To Run before publish on git
Echo ****************************************

rmdir /S /Q tdd-ebook
rmdir /S /Q TddEbook_Sphinx
rmdir /S /Q .\TddEbook_Italiano\gettext
move .\TddEbook_Italiano\latex\it\*.pdf .\TddEbook_Italiano\latex\
rmdir /S /Q .\TddEbook_Italiano\latex\it

move .\TddEbook_Italiano\epub\it\*.epub .\TddEbook_Italiano\epub\
rmdir /S /Q .\TddEbook_Italiano\epub\it

del /S /Q   .\TddEbook_OmegaT\omegat\*.bak
del /S /Q   .\TddEbook_OmegaT\*.bak
del /S /Q   .\TddEbook_OmegaT\target\it\LC_MESSAGES\*.mo

Echo ********************
Echo * Ready for commit *
Echo ********************
