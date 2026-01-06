# zuse_handwriting_semantic_digital_libraries
The repository contains a collection of material for a Transkribus project, which trained a HTR-model for the transcription of Konrad Zuse's handwriting. The project was part of the course 'Semantic Digital Libraries' at Università di Bologna.

The results of the project are four different HTR-models.

Model I – Zuse handwritten - From scratch: https://app.transkribus.org/models/text/459125
Model II – Zuse handwritten - tuned basemodel: https://app.transkribus.org/models/text/459305
Model III – Zuse handwritten - From scratch without line polygons: https://app.transkribus.org/models/text/464445
Model IV – Zuse handwritten - tuned basemodel without line polygons (best performing): https://app.transkribus.org/models/text/463085

In detail the repository contains the following items:
- A detailed [project report](Zuse_Trascribus_project_report_eng.pdf)
- A [detailed list of Zuse's documents and material](DMA_Zuse_material_listing/NL_207_Zuse.pdf) managed by the Archive of the Deutsches Museum (Munich)
- The [exported transcripted documents](export_job_20571304) from the annotation campaign, which were used as training material
- The [TCER and VCER curves](training_curves_pngs) from all model trainings
- A [python script](zuse_sample_analysis_script.py) which analyzed the training sample in detail
- a [plantuml-file](classes_zuse_handwriting_project.plantuml) to describe the TrainingSampleAnalyser class structure of the python file and the corresponding [png-file](TrainingSampleAnalyser_uml_class_diagram.png)
- The [results of training sample analysis](quantity_analysis_results_xlsx_png) by the python script (quantity of different signs, percentage)
