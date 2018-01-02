## RoboFlow: HELP
-----------------------------------------
This Roboflow guide assumes you have at least passing familiarity with TensorFlow:
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

###PARAMETERS:
basetag: \tthe master classification tag or theme ('robots' or 'birds' or whatever)'''
imagequantity:\tan integer between 0 and "+str(cfg.imgnum_maxpercycle)+", to not hammer other people's servers"
searchtag:\tthe searchterm, such as 'robot' or 'robotart' etc
flowsteps:\tOPTIONAL parameter to determine which stages to implement of --
\t\t'download' - only downloads the tagged images
\t\t'classify' (default, if blank) - download, classify/sort images w/model of your choice
\t\t'classify_top' - download, classify with TOP accuracy model (skips setup),
\t\t'retrain' - download, classify, and retrain (w/optional harvest) a new 
\t\t classifier with images from training_photos/{basetag}
\t\t'retrain_defaults' (as in 'robots 0 0 retrain_defaults') will skip the retrain SETUP,
\t\t using values from config file setup.


###BOOTSTRAP NOTE
Quality initial labeling/sorting makes ALLL the difference!
When starting, you must manually sort a minimum number of images to allow the first 
retraining to create the first classifier. After that, downloading, classifying/auto-sorting, 
and harvesting to retrain to make a better classifier is waaaaay more automated.


## Keeping reading the extensive detailed help for useful and important advice.


