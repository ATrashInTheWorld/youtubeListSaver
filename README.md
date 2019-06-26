Youtube Playlists saver


Purpose:

The purpose of this application is to save your youtube playlist in a .txt file. It was mainly created in order to have a backup of our saved videos in case youtube decides to set them private or delete them.


How to install:
1. Download the git project.
2. Create a directory/folder called "BK". Called otherwise could cause a problem.
3. Set up a Google API for youtube as in this links: https://developers.google.com/youtube/v3/getting-started
   Once you finish you should have an API key and an OAuth 2.0 client ID 
4. Click on the file from OAuth 2.0 client ID, download the JSON file and put it in the project folder
5. Rename the OAuth 2.0 client ID file as "csf2.json", else it won't work.
6. DONE!!


How to use:
1. Once the set up is done and you try to run the main.py file, a huge link will be displaying. Below, you will have to enter    a code. Don't worry, it is only google confirming that you want to use your API. Therefore:

    1.1 Enter your Google account credentials.
    
    1.2 It might then redirect you to a page saying that your API is not secure. Don't worry, click on "Advance" (below the           message) and then click on "Go to ... (unsafe)".
    
    1.3 Allow everything.
    
    1.4 Once done copy the code given by Google and paste it in the terminal.
    
2. Once you entered the code, below should appear all your playlists, select the number of the wanted one.
3. Enter a name for the file (without the txt extension) and press enter, or just press enter to let the default one
4. Enter the path where you want to save the file (full path: C://User/user1... or /home/user1/...) or just press enter to      save it in the created "BK" directory/folder.
5. Wait, the list is being copied.
6. Once done, select another list to save or press -1 to exit.



Potential problem:

If you ever encounter a problem such as "IndexError: list index out of range", it would mean that a video has been deleted or set to private. Either way, you can no longer access. For now, just delete all the unavailable videos from the playlists and it should avoid a crash. I am currently working on the issue.



To becoming:

 -> Ensure that the user is connected to the internet
 
 -> Get information about the playlist selected
 
 -> Allow to rename the file or change the directory of the file already exists in the selected directory
 
 -> Note which videos are deleted/set private and no longer available
 
 -> Ensure no crash happens on an unavailable video.
 
 -> Give the choice to print each line or not
 
 
 
 
 Feel free to leave a message for any reason. 
 
 Also, feel free to use the code as you please.
