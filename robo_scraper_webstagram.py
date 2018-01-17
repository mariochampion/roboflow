#!/usr/bin/env python
'''
robo_scraper_imgur contains the WEBSTAGRAM specific versions of the scraping functions:
- getimagesmaster()
- getnexturl()
- getcursorandimgsrcs()
- urlbuild()
- webfileprep()

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

import os, sys, re, json
from urllib2 import Request, urlopen
import robo_config as cfg
import robo_support as robo 

# SPECIFIC 'GLOBAL' VARS FOR THIS SCRAPER
scrapeurl = "https//web.stagram.com/tag" # no colon as it breaks this file. added JIT
imgdlfile_url_prefix = None
imgdlfile_url_suffix = ".jpg"
scrapefile_prefix = "__webstagram_"
scrapefile_suffix = ".txt" # sep name for max flex of diff later needs
scrape_sort = None
scrapeurl_pagenum = None



print cfg.color.green
print "+++++++++++++++++++++++++++++++++++++"
print "     WEBSTAGRAM FUNCTIONS LOADED"
print "+++++++++++++++++++++++++++++++++++++"
print cfg.color.white




##################################	  
###  hey, have some functions  ###	  
##################################

#################################
def getcursorandimgsrcs(webfile_prepped, imgnum_needed, progressdata):
  robo.whereami(sys._getframe().f_code.co_name)
  
  imgsrc_list = []
  img2url_dict = {}
  cursor = None	
  
  #build a list of images for de-dupe. with a refactor, i would make a single list of 
  # imgnum_needed urls and pass that to a download module... for now i ll check the logfile
  imgs_existing = robo.imgs_existing_build(progressdata["img2url_file"])
  
  for line in webfile_prepped:
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
        imgdlfile_url = rawimg.replace('addthis:media="', '')
        if imgdlfile_url not in imgs_existing: #prevent dupes
          imgsrc_list.append(imgdlfile_url)
        
        if url_match:
          rawurl = url_match.group()
          imgmatch_url = rawurl.replace('" addthis:media', '').replace('addthis:url="', '')
          img2url_dict[rawimg.replace('addthis:media="', '')] = [imgmatch_url]
        
  cursor_and_imgs = [cursor, imgsrc_list, img2url_dict]
  
  if len(imgsrc_list) < 1:
    print cfg.color.yellow + '''
=================================
       ***** WARNING *****
   no JPG images found online! 
================================='''
    print cfg.color.white
    
  return cursor_and_imgs
  


#################################
def urlbuild(vars_dict):
  robo.whereami(sys._getframe().f_code.co_name)
  
  thistag = vars_dict["thistag"]
  scrapeurl_pagenum = vars_dict["scrapeurl_pagenum"]
  url_built_ending = scrape_sort + cfg.dd + str(scrapeurl_pagenum)
  
  url_built = scrapeurl.replace("https","https:") + cfg.dd + thistag + cfg.dd + url_built_ending
  vars_dict["scrapeurl_pagenum"] += 1
  
  vars_dict["url_built"] = url_built
  return vars_dict



#################################
def getwebfile(webfileurl):
  robo.whereami(sys._getframe().f_code.co_name)
  
  print "API for:", webfileurl
  imgur_client_id = 'Client-ID '+os.environ.get('IMGURAPI_ID')    
  req = Request(webfileurl)
  req.add_header('Authorization', imgur_client_id)
    
  try:
    webfile = urlopen(req)
    return webfile
  except:
    print cfg.color.red
    print "doh, probably 'urllib2.HTTPError: HTTP Error 500: Internal Server Error'"
    print "(something wrong with imgur API. happens all the time. try again in a min.)"
    print cfg.color.white
    robo.goodbye()
    
  sys.exit(1) #shouldnt get here, but for safety 



#################################
def webfile_prep(fwebname):
  robo.whereami(sys._getframe().f_code.co_name)
  
  with open(fwebname, "r") as webfile_local:
    try:
      webfile_prepped = json.load(webfile_local)
      return webfile_prepped
    except:
      print cfg.color.yellow
      print "Hmm, Unable to load JSON from IMGUR API response."
      print "(usually, the tag has no images. so check  the txt file above, and give it a look online.)"
      print cfg.color.white
      robo.goodbye()

  sys.exit(1) #shouldnt get here, but for safety 


#################################
def getnexturl(vars_dict):
  
  robo.whereami(sys._getframe().f_code.co_name)

  with open(vars_dict["localurlfile"], "rU") as f:
    urls_list = [line for line in f]
    
  #should have format like: https://api.imgur.com/3/gallery/t/robot/time/3
  # get/increment number at end, and update scrapeurl_pagenum
  nexturl_raw= urls_list[ (len(urls_list)-1)]
  nexturl_parts = nexturl_raw.replace("\n","").split("/")
  nexturl_increment = nexturl_parts[-1] 
  nexturl_increment_added = str(int(nexturl_increment)+1)
  nexturl_ending = scrape_sort + cfg.dd + nexturl_increment_added
  nexturl = scrapeurl.replace("https","https:") + cfg.dd + vars_dict["thistag"] + cfg.dd + nexturl_ending
  vars_dict["nexturl"]  = nexturl
  vars_dict["scrapeurl_pagenum"]  = int(nexturl_increment_added)
  
  if nexturl == cfg.nomoreurls: iscomplete(progressdata)
  
  return vars_dict










