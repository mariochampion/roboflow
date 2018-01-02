-----------------------------------------
## RoboFlow: HELP
-----------------------------------------
This Roboflow guide assumes you have at least passing familiarity with TensorFlow:<br>
https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/<br>
https://www.tensorflow.org/tutorials/image_retraining

## HOW TO USE:
### Guided usage:
```
python roboflow.py
```
### Advanced usage:
```
python roboflow.py [basetag] [imagequantity] [searchtag] [optional flowsteps]
```
for example:
```
python roboflow.py robots 200 robotart download
```

### PARAMETERS:<br>
* basetag: the master classification tag or theme ('robots' or 'birds' or whatever)<br>
* imagequantity: an integer between 0 and the {imgnum_maxpercycle} var from the config file, to not hammer other people's servers<br>
* searchtag: the searchterm, such as 'robot' or 'robotart' etc<br>
* flowsteps: OPTIONAL parameter to determine which stages to implement of --<br>
 ** 'download' - only downloads the tagged images<br>
 ** 'classify' (default, if blank) - download, classify/sort images w/model of your choice<br>
 ** 'classify_top' - download, classify with TOP accuracy model (skips setup),<br>
 ** 'retrain' - download, classify, and retrain (w/optional harvest) a new <br>
  classifier with images from training_photos/{basetag}<br>
 ** 'retrain_defaults' (as in 'robots 0 0 retrain_defaults') will skip the retrain SETUP,<br>
  using values from config file setup.


### BOOTSTRAP NOTE
Quality initial labeling/sorting makes ALLL the difference!<br>
When starting, you must manually sort a minimum number of images to allow the first retraining to create the first classifier. After that, downloading, classifying/auto-sorting, and harvesting to retrain to make a better classifier is waaaaay more automated.


## Keeping reading the extensive detailed help for useful and important advice.


