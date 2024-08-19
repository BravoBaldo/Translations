Italian translations of [cs249r_book](https://github.com/harvard-edge/cs249r_book) or [On Line Version](https://mlsysbook.ai/)

# Status
*	Translation In progress.
*	Waiting Author agreement

# ToDo:
*	How to change name of "_quarto.yml" or insert language specific commands/variables
*	How to change name of "index.qmd"
*	How to apply native localization
*	How to have pdf in A4 format (European)

# Batch:
```
git clone https://github.com/harvard-edge/cs249r_book.git
cd cs249r_book
rename _quarto.yml _quarto_org.yml
rename index.qmd   index_org.qmd
copy ..\cs249r_book_it\_quarto.yml .
copy ..\cs249r_book_it\index.qmd .

copy "..\cs249r_book_it\contents\dedication_it.qmd"                         ".\contents\"
copy "..\cs249r_book_it\contents\contributors_it.qmd"                       ".\contents\"
copy "..\cs249r_book_it\contents\copyright_it.qmd"                          ".\contents\"
copy "..\cs249r_book_it\contents\about_it.qmd"                              ".\contents\"
copy "..\cs249r_book_it\contents\acknowledgements\acknowledgements_it.qmd"  ".\contents\acknowledgements\"
copy "..\cs249r_book_it\contents\introduction\introduction_it.qmd"          ".\contents\introduction\"
copy "..\cs249r_book_it\contents\ml_systems\ml_systems_it.qmd"              ".\contents\ml_systems\"
copy "..\cs249r_book_it\contents\dl_primer\dl_primer_it.qmd"                ".\contents\dl_primer\"
copy "..\cs249r_book_it\contents\workflow\workflow_it.qmd"                  ".\contents\workflow\"
copy "..\cs249r_book_it\contents\data_engineering\data_engineering_it.qmd"  ".\contents\data_engineering\"
copy "..\cs249r_book_it\contents\frameworks\frameworks_it.qmd"              ".\contents\frameworks\"
copy "..\cs249r_book_it\contents\training\training_it.qmd"                  ".\contents\training\"
copy "..\cs249r_book_it\contents\efficient_ai\efficient_ai_it.qmd"          ".\contents\efficient_ai\"
...
quarto render	
```
That's all for now ;)
