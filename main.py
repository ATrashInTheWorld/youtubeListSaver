#!/usr/bin/python

# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

#Link for playlists :::: https://developers.google.com/youtube/v3/docs/playlistItems/list

import os
from datetime import date

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube"]

#Check if Filename is not empty
def checkIfFileNameIsEmpty(fileName, defaultFN):
    if(fileName == ""):
	return defaultFN
    else:
	return fileName+".txt"

#Checkif Path and file name are ok
def checkIfFPandFexists(filePath, fileName):
   pathOk = False
   fileOK = False

	#Path
   if(filePath==""):
	filePath = "./BK"

   elif(os.path.isdir(filePath) == False):
	while os.path.isdir(filePath) == False:
		filePath = raw_input("Path Not valid, please enter a valid Path -> ")

	# check If file does not already in the selected directory
   if(os.path.isfile(str(filePath+"/"+fileName)) == True):
	while os.path.isfile(str(filePath+"/"+fileName)) == True:
		filePath = raw_input("A file with the same name already exists in the selected directory! \n Plese enter another path -> ")

	#If everyting OK
   return filePath

#retrieve Videos Id from the requested PL
def getVideosID(plID):
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=50,
        playlistId= plID
    )
    response = request.execute()
    videosIDArr = {}
    for videosID in response["items"]:
	videosIDArr[videosID["snippet"]["position"]+1] = videosID["contentDetails"]["videoId"]

    sortedVideosIDArr = {}
    for k in sorted(videosIDArr.keys()):
	sortedVideosIDArr[k] = videosIDArr[k]

    return sortedVideosIDArr

#Retrieve Vidoes Infos from MY OWN created plylist
def retrieveVideosFromPL(plID, file):
    videosIDs = getVideosID(plID)
    #allInfosPerVi = {}
    for videoP in videosIDs:
	position = videoP
	videoID = videosIDs[position]
	#print("VID -> "+videoID)
	#API to retrieve videos infos
	request = youtube.videos().list(
        	part="snippet,contentDetails",
        	id= videoID
    	)
	response = request.execute()

	title = response["snippet"]
	# ok print a bunch of stuff like only snippet and items AND itmes/snippet
	channel = response["items"]["snippet"]["channelTitle"]
	duration = response["items"]["contentDetails"]["duration"]

	file.write(str(position)+". "+title+" -> "+channel+" %> "+duration+" \#> "+videoID)


#Retrieves from my LIKED PL
#https://developers.google.com/youtube/v3/docs/videos/list?refresh=1
#def retrieveFromLiked():

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    global youtube

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "csf2.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)

    credentials = flow.run_console()

	# API preparation
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

	#API receiving lists 
    request = youtube.playlists().list(
        part="snippet",
        maxResults=25,
	mine=True
    )
    response = request.execute()
 # the response contains the list infos ^^

	# seting up list
    availableListsDico = {"Liked Videos": "LL", "Watch Later":"WL"}

    for element in response["items"]:
	availableListsDico[str(element["snippet"]["title"])] = str(element["id"])
    
    ### Entering the big loop of chooices
    sel = 9999 # infinit choice
    maxChoices = len(availableListsDico)
    #print maxChoices
    while sel != -1:
	listCounter = 1
	print("\n Select the play list (as a number) from the selection below or type -1 to exit \n")
	#displaying choices
	for key, value in availableListsDico.items():
		print (str(listCounter)+". "+key)
		listCounter += 1
	print "-1. Exit \n"
	sel = input("Playlist -> ")

	# EXIT
	if(sel == -1):
		print("Program EXITED")

	# Lists exists
	elif(sel <= maxChoices and sel >= 1):
		
		#file Name
		defaultFileName = availableListsDico.keys()[sel-1]+"_"+str(date.today())+".txt"
		print("Please the file Name, DEFAULT:"+defaultFileName+" (press enter)")
		fileName = checkIfFileNameIsEmpty(str(raw_input("File name -> ")), str(defaultFileName))
		
		#file Path
		filePath = checkIfFPandFexists(raw_input("Please enter a path to save the file with no '/' at the end \n (DEFAULT: ./BK) -> "), fileName)

		# Real Deal, not i does the core of the idea
		print "Sure, a moment please ..."

		# create the empty file
		file = open(filePath+"/"+fileName, 'a')
		file.write(availableListsDico.keys()[sel-1]+"\n PO. Title -> OriginateChanel  %> Duration  \#> videoID ")

		# copies the playlist in the file with the infos
		retrieveVideosFromPL(availableListsDico.values()[sel-1], file)
		file.close()

	# List does not exist
	else:
		print("Not in the choices, slect again or type -1 to exit!")











if __name__ == "__main__":
    main()
