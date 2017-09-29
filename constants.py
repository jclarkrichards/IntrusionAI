
JSONFILE = "data.json"
#When adding a new machine append this to the data from the .json file
TEMPLATE = {"UID":0, "name":"", "local":True, "remote":"linux", "server":"", "ip":"", "port":"", 
             "password":"", "logpaths":[], "keywords":[], "winSystemKeywords":"", "winAppKeywords":"",
            "winSecurityKeywords":"", "systemcheck":True, "appcheck":True, "securitycheck":True}

#If no file is found then this is what we use initially in the file
BASE = {"machine":[], "email":""}

WINLOGO = "Images/windowslogo.png"
LINUXLOGO = "Images/linuxlogo.png"
RUNONCELOGO = "Images/runbuttonlogo.jpg"
SCHEDULELOGO = "Images/rerunbuttonlogo.png"
REMOVELOGO = "Images/x.png"
GRAPHLOGO = "Images/graphbuttonlogo.png"
AILOGO = "Images/test.png"
COPYLOGO = "Images/copybuttonlogo.jpg"
STATUSGOOD = "Images/statusgood.png"
CANCELSMALL = "Images/cancel_small.jpeg"

#Colors
LG = "#e3f7eb" #Light Green
TEXTCOLOR = "#5eed5c"
BUTTONCOLOR = "#576357"
RC = "#f2baab" #Color for entries that are required (redish color)
BLACK = "#ffffff"
