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

def checkIfFileNameIsEmpty(fileName, defaultFN):
    if(fileName == ""):
	return defaultFN
    else:
	return fileName

def checkIfFPandFexists(filePath, fileName):
    

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

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
		filePath: raw_input("Please enter a path to save the file, else is will be saved in BK folder from the current directory")
		checkIfFPandFexists(filePath, fileName)

		print "Sure, a moment please ..."

	# List does not exist
	else:
		print("Not in the choices, slect again or type -1 to exit!")











if __name__ == "__main__":
    main()
