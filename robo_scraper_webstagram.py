#!/usr/bin/env python
'''
robo_scraper_webstagram contains the WEBSTAGRAM specific versions of the scraping functions:
-getimagesmaster()
-getnexturl()
-getcursorandimgsrcs()

'''
## ===================================================================
## ROBOFLOW - LICENSE AND CREDITS
## This app/collection of scripts at https://github.com/mariochampion/roboflow
## released under the Apache License 2.0. (http://www.apache.org/licenses/LICENSE-2.0)
## and depends on many contributions from the internets, stackexchange, twilio, 
## and of course and especially the Google TensorFlow for Poets codelab:
##     tutorials: https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/ 
##     code: https://github.com/googlecodelabs/tensorflow-for-poets-2
## 
## ROBOFLOW scripts were  written by mario champion (mariochampion.com) as an exercise to learn 
## more python(2.7) file/dir manipulations, in a commandline driven app, and to better understand
## Google's TensorFlow image classification elements and hyperparameter effects.
##
## please open issues and pull requests,
## thanks and always remember: this robot loves you. 
## boop boop!
## ===================================================================

import os, sys
import robo_config as cfg
import robo_support as robo 


print cfg.color.green
print "+++++++++++++++++++++++++++++++++++++"
print "     WEBSTAGRAM FUNCTIONS LOADED"
print "+++++++++++++++++++++++++++++++++++++"
print cfg.color.white

##################################	  
###  hey, have some functions  ###	  
##################################

#################################
def getcursorandimgsrcs(webfile, imgnum_needed):
  robo.whereami(sys._getframe().f_code.co_name)
  
  imgsrc_list = []
  img2url_dict = {}
  cursor = None	
  
  for line in webfile:
    match = ""
    img_match = ""
    url_match = ""
    match = re.search('cursor=([\S]+)"', line)
    img_match =  re.search(r'addthis:media="(.+\.jpg)', line)
    url_match =  re.search(r'addthis:url="(.+) addthis:media', line)
    if match:
      cursorz = match.group()
      cursor = cursorz.replace('"',"") #trim off rare trailing double-quotes
  
    #scrape webfiles for the img srcs
    if img_match:
      rawimg = img_match.group()
      if len(imgsrc_list) < imgnum_needed:
        imgsrc_list.append( rawimg.replace('addthis:media="', '') )
        if url_match:
          rawurl = url_match.group()
          imgmatch_url = rawurl.replace('" addthis:media', '').replace('addthis:url="', '')
          img2url_dict[rawimg.replace('addthis:media="', '')] = [imgmatch_url]
        
  cursor_and_imgs = [cursor, imgsrc_list, img2url_dict]
  
  if len(imgsrc_list) < 1:
    print "================================="
    print "       ***** WARNING *****"
    print "     no images found online! "
    print "================================="
    
  return cursor_and_imgs
  
