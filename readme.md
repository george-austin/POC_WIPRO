# Object detection for book damage - WIPRO

## Description
Code for the WIPRO project "Schadenserkennung bei Büchern mit Hilfe von Machine Learning" at HSLU HS 2023

## Important files
* [train.py](https://github.com/george-austin/POC_WIPRO/blob/main/train.py) - Used to train the model. The training data should be located in the following datasets directory
* [test.py](https://github.com/george-austin/POC_WIPRO/blob/main/test.py) - Used to run the model to detect damage
* [wipro_gui.py](https://github.com/george-austin/POC_WIPRO/blob/main/wipro_gui.py) - analysis tool - used to rate damage the model detected and then retrain the model. Options: TP / FP

## Explanation of directories
* [datasets](https://github.com/george-austin/POC_WIPRO/tree/main/datasets) - the training dataset
    * train - the data used to train the model
      * images - the images used to train the model
      * label - the labels with the same names as the images
    * valid - the data used to validate the model performance during training
      * images - the images used to validate the model
      * label - the labels with the same names as the images
    * test - test data, all the unlabeled data you want the model to run against
* [data_analysis](https://github.com/george-austin/POC_WIPRO/tree/main/data_analysis) - contains the scripts used during initial analysis of the data
* [data_augmentation](https://github.com/george-austin/POC_WIPRO/tree/main/data_augmentation) - contains the scripts used to change training data in any way
* [runs/detect](https://github.com/george-austin/POC_WIPRO/tree/main/runs/detect) - contains the trained models mentioned in the project document
  * binarized_model/weights - the model trained after transforming the labels from categoric (mold, water damage, ...) to binary (no damage / damage) - 14.1% recall
  * segmentation_model/weights - the model trained after segmenting the images around damage instances - 2.1% recall
  * segmentation_model_wo_dirt/weights - the model using segmentation data but excluding dirt instances - 3.5% recall
  * own_labels_model/weights - the model trained after we decided to label the images on our own - 20% recall
  * analysis_tool_model/weights - the model trained after correcting the output of own_labels_model in analysis tool - 21.8% recall

## Authors and acknowledgment
- Samuel Nussbaumer
- Austin George