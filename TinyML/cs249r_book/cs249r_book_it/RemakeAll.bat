git clone https://github.com/harvard-edge/cs249r_book.git
cd cs249r_book
Echo "Rendering English Version in '_book'"
quarto render

SET SRCDIR=..\cs249r_book_it\

rename _quarto.yml _quarto_org.yml
rename index.qmd   index_org.qmd

copy "%SRCDIR%_quarto.yml"                                                                              "."
copy "%SRCDIR%index.qmd"                                                                                "."
copy "%SRCDIR%references.it.qmd"                                                                        "."
copy "%SRCDIR%Italian-reference-doc.docx"                                                               "."

copy "%SRCDIR%contents\dedication.it.qmd"                                                               ".\contents\"
copy "%SRCDIR%contents\contributors.it.qmd"                                                             ".\contents\"
copy "%SRCDIR%contents\copyright.it.qmd"                                                                ".\contents\"
copy "%SRCDIR%contents\about.it.qmd"                                                                    ".\contents\"
Rem copy "%SRCDIR%contents\conventions.it.qmd"                                                              ".\contents\"

copy "%SRCDIR%contents\core\acknowledgements\acknowledgements.it.qmd"                                   ".\contents\core\acknowledgements\"
copy "%SRCDIR%contents\core\introduction\introduction.it.qmd"                                           ".\contents\core\introduction\"
copy "%SRCDIR%contents\core\ml_systems\ml_systems.it.qmd"                                               ".\contents\core\ml_systems\"
copy "%SRCDIR%contents\core\dl_primer\dl_primer.it.qmd"                                                 ".\contents\core\dl_primer\"
copy "%SRCDIR%contents\core\workflow\workflow.it.qmd"                                                   ".\contents\core\workflow\"
copy "%SRCDIR%contents\core\data_engineering\data_engineering.it.qmd"                                   ".\contents\core\data_engineering\"
copy "%SRCDIR%contents\core\frameworks\frameworks.it.qmd"                                               ".\contents\core\frameworks\"
copy "%SRCDIR%contents\core\training\training.it.qmd"                                                   ".\contents\core\training\"
copy "%SRCDIR%contents\core\efficient_ai\efficient_ai.it.qmd"                                           ".\contents\core\efficient_ai\"
copy "%SRCDIR%contents\core\optimizations\optimizations.it.qmd"                                         ".\contents\core\optimizations\"
copy "%SRCDIR%contents\core\hw_acceleration\hw_acceleration.it.qmd"                                     ".\contents\core\hw_acceleration\"
copy "%SRCDIR%contents\core\benchmarking\benchmarking.it.qmd"                                           ".\contents\core\benchmarking\"
copy "%SRCDIR%contents\core\ondevice_learning\ondevice_learning.it.qmd"                                 ".\contents\core\ondevice_learning\"
copy "%SRCDIR%contents\core\ops\ops.it.qmd"                                                             ".\contents\core\ops\"
copy "%SRCDIR%contents\core\privacy_security\privacy_security.it.qmd"                                   ".\contents\core\privacy_security\"
copy "%SRCDIR%contents\core\responsible_ai\responsible_ai.it.qmd"                                       ".\contents\core\responsible_ai\"
copy "%SRCDIR%contents\core\sustainable_ai\sustainable_ai.it.qmd"                                       ".\contents\core\sustainable_ai\"
copy "%SRCDIR%contents\core\robust_ai\robust_ai.it.qmd"                                                 ".\contents\core\robust_ai\"
copy "%SRCDIR%contents\core\generative_ai\generative_ai.it.qmd"                                         ".\contents\core\generative_ai\"
copy "%SRCDIR%contents\core\ai_for_good\ai_for_good.it.qmd"                                             ".\contents\core\ai_for_good\"
copy "%SRCDIR%contents\core\conclusion\conclusion.it.qmd"                                               ".\contents\core\conclusion\"

copy "%SRCDIR%contents\labs\labs.it.qmd"                                                                ".\contents\labs\"
copy "%SRCDIR%contents\labs\overview.it.qmd"                                                            ".\contents\labs\"
copy "%SRCDIR%contents\labs\getting_started.it.qmd"                                                     ".\contents\labs\"

copy "%SRCDIR%contents\labs\arduino\nicla_vision\nicla_vision.it.qmd"                                   ".\contents\labs\arduino\nicla_vision\"
copy "%SRCDIR%contents\labs\arduino\nicla_vision\setup\setup.it.qmd"                                    ".\contents\labs\arduino\nicla_vision\setup\"
copy "%SRCDIR%contents\labs\arduino\nicla_vision\image_classification\image_classification.it.qmd"      ".\contents\labs\arduino\nicla_vision\image_classification\"
copy "%SRCDIR%contents\labs\arduino\nicla_vision\object_detection\object_detection.it.qmd"              ".\contents\labs\arduino\nicla_vision\object_detection\"
copy "%SRCDIR%contents\labs\arduino\nicla_vision\kws\kws.it.qmd"                                        ".\contents\labs\arduino\nicla_vision\kws\"
copy "%SRCDIR%contents\labs\arduino\nicla_vision\motion_classification\motion_classification.it.qmd"    ".\contents\labs\arduino\nicla_vision\motion_classification\"

copy "%SRCDIR%contents\labs\seeed\xiao_esp32s3\xiao_esp32s3.it.qmd"                                     ".\contents\labs\seeed\xiao_esp32s3\"
copy "%SRCDIR%contents\labs\seeed\xiao_esp32s3\setup\setup.it.qmd"                                      ".\contents\labs\seeed\xiao_esp32s3\setup\"
copy "%SRCDIR%contents\labs\seeed\xiao_esp32s3\image_classification\image_classification.it.qmd"        ".\contents\labs\seeed\xiao_esp32s3\image_classification\"
copy "%SRCDIR%contents\labs\seeed\xiao_esp32s3\object_detection\object_detection.it.qmd"                ".\contents\labs\seeed\xiao_esp32s3\object_detection\"
copy "%SRCDIR%contents\labs\seeed\xiao_esp32s3\kws\kws.it.qmd"                                          ".\contents\labs\seeed\xiao_esp32s3\kws\"
copy "%SRCDIR%contents\labs\seeed\xiao_esp32s3\motion_classification\motion_classification.it.qmd"      ".\contents\labs\seeed\xiao_esp32s3\motion_classification\"

copy "%SRCDIR%contents\labs\raspi\raspi.it.qmd"                                                         ".\contents\labs\raspi\"
copy "%SRCDIR%contents\labs\raspi\setup\setup.it.qmd"                                                   ".\contents\labs\raspi\setup\"
copy "%SRCDIR%contents\labs\raspi\image_classification\image_classification.it.qmd"                     ".\contents\labs\raspi\image_classification\"
copy "%SRCDIR%contents\labs\raspi\object_detection\object_detection.it.qmd"                             ".\contents\labs\raspi\object_detection\"
copy "%SRCDIR%contents\labs\raspi\llm\llm.it.qmd"                                                       ".\contents\labs\raspi\llm\"

copy "%SRCDIR%contents\labs\shared\shared.it.qmd"                                                       ".\contents\labs\shared\"
copy "%SRCDIR%contents\labs\shared\kws_feature_eng\kws_feature_eng.it.qmd"                              ".\contents\labs\shared\kws_feature_eng\"
copy "%SRCDIR%contents\labs\shared\dsp_spectral_features_block\dsp_spectral_features_block.it.qmd"      ".\contents\labs\shared\dsp_spectral_features_block\"

Rem copy "%SRCDIR%contents\tools.it.qmd"                                                                    ".\contents\"
Rem copy "%SRCDIR%contents\zoo_datasets.it.qmd"                                                             ".\contents\"
Rem copy "%SRCDIR%contents\zoo_models.it.qmd"                                                               ".\contents\"
Rem copy "%SRCDIR%contents\learning_resources.it.qmd"                                                       ".\contents\"
Rem copy "%SRCDIR%contents\community.it.qmd"                                                                ".\contents\"
Rem copy "%SRCDIR%contents\case_studies.it.qmd"                                                             ".\contents\"

copy "%SRCDIR%part_LABS.it.qmd"                                             ".\contents\labs\"
copy "%SRCDIR%part_nicla_vision.it.qmd"                                     ".\contents\labs\arduino\nicla_vision\"
copy "%SRCDIR%part_xiao_esp32s3.it.qmd"                                     ".\contents\labs\seeed\xiao_esp32s3\"
copy "%SRCDIR%part_raspi.it.qmd"                                            ".\contents\labs\raspi\"
copy "%SRCDIR%part_shared.it.qmd"                                           ".\contents\labs\shared\"

Echo "Rendering della versione italiana in '_book_it'"
quarto render