Italian translations of [cs249r_book](https://github.com/harvard-edge/cs249r_book) or [On Line Version](https://mlsysbook.ai/)

# Status
*	Translation In progress.

# ToDo:
*	How to have pdf in A4 format (European)
*	Apply localization to pdf too


# Batch:
```
git clone https://github.com/harvard-edge/cs249r_book.git
cd cs249r_book
Echo "Rendering English Version in '_book'"
Rem quarto render

rename _quarto.yml _quarto_org.yml
rename index.qmd   index_org.qmd

copy ..\cs249r_book_it\_quarto.yml .
copy ..\cs249r_book_it\index.qmd .

copy "..\cs249r_book_it\contents\dedication.it.qmd"                           ".\contents\"
copy "..\cs249r_book_it\contents\contributors.it.qmd"                         ".\contents\"
copy "..\cs249r_book_it\contents\copyright.it.qmd"                            ".\contents\"
copy "..\cs249r_book_it\contents\about.it.qmd"                                ".\contents\"
copy "..\cs249r_book_it\contents\acknowledgements\acknowledgements.it.qmd"    ".\contents\acknowledgements\"
copy "..\cs249r_book_it\contents\introduction\introduction.it.qmd"            ".\contents\introduction\"
copy "..\cs249r_book_it\contents\ml_systems\ml_systems.it.qmd"                ".\contents\ml_systems\"
copy "..\cs249r_book_it\contents\dl_primer\dl_primer.it.qmd"                  ".\contents\dl_primer\"
copy "..\cs249r_book_it\contents\workflow\workflow.it.qmd"                    ".\contents\workflow\"
copy "..\cs249r_book_it\contents\data_engineering\data_engineering.it.qmd"    ".\contents\data_engineering\"
copy "..\cs249r_book_it\contents\frameworks\frameworks.it.qmd"                ".\contents\frameworks\"
copy "..\cs249r_book_it\contents\training\training.it.qmd"                    ".\contents\training\"
copy "..\cs249r_book_it\contents\efficient_ai\efficient_ai.it.qmd"            ".\contents\efficient_ai\"
copy "..\cs249r_book_it\contents\optimizations\optimizations.it.qmd"          ".\contents\optimizations\"
copy "..\cs249r_book_it\contents\hw_acceleration\hw_acceleration.it.qmd"      ".\contents\hw_acceleration\"
copy "..\cs249r_book_it\contents\benchmarking\benchmarking.it.qmd"            ".\contents\benchmarking\"
copy "..\cs249r_book_it\contents\ondevice_learning\ondevice_learning.it.qmd"  ".\contents\ondevice_learning\"
copy "..\cs249r_book_it\contents\ops\ops.it.qmd"                              ".\contents\ops\"
copy "..\cs249r_book_it\contents\privacy_security\privacy_security.it.qmd"    ".\contents\privacy_security\"
copy "..\cs249r_book_it\contents\responsible_ai\responsible_ai.it.qmd"        ".\contents\responsible_ai\"
copy "..\cs249r_book_it\contents\sustainable_ai\sustainable_ai.it.qmd"        ".\contents\sustainable_ai\"
copy "..\cs249r_book_it\contents\robust_ai\robust_ai.it.qmd"                  ".\contents\robust_ai\"

...
Echo "Rendering della versione italiana in '_book_it'"
quarto render	
```
That's all for now ;)
