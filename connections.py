from Tkinter import *
from tkMessageBox import *
import os
from subprocess import PIPE, Popen
from window import WindowABC
import time
import platform
if platform.system() == "Windows":
    import logwin
import emailer


class Connections(object):
    def __init__(self):
        self.platform = platform.system()
        self.server = ""
        self.ip = ""
        self.port = ""
        self.logpaths = []
        self.keywords = []
        self.password = ""
        self.trimdate = None
        self.UID = 0
        self.savepath = os.getcwd()
        self.email = ""

    def runLogReporter(self, data, index, password):
        '''Choose which connection to use based on the data'''
        self.email = data["email"]
        self.sendemail = data["sendemail"] #True or False
        data = data["machine"][index]
        self.data = data
        print data
        #print data["local"]
        #print data["remote"]
        self.ip = data["ip"]
        self.logpaths = data["logpaths"]
        self.keywords = self.formatKeywords(data["keywords"])
        self.server = data["server"]
        self.port = data["port"]
        self.password = password
        self.UID = data["UID"]
        
        
        if data["local"]:
            if self.platform == "Windows":
                self.Windows2Self()
            else:
                self.Linux2Self()
        else:
            if self.platform == "Windows":
                if data["remote"] == "Windows":
                    self.Windows2Windows()
                else:
                    self.Windows2Linux()
            else:
                if data["remote"] == "Windows":
                    self.Linux2Windows()
                else:
                    self.Linux2Linux()
            

    # Connecting Linux -> Self, Linux, Windows
    def Linux2Self(self):
        print "Connecting Linux to Self"
        result = []
        for i, path in enumerate(self.logpaths):
            if path[0] != "":
                contents = open(path[0], "r").readlines()
                #print len(contents)
                result.append("\n\n" + path[0] + "\n\n")
                #print len(contents)
                temp = self.trimResultsByKeywords(contents, i)
                #print len(temp)
                result.append(self.trimResultsByDate(temp))
        #print result

        self.saveReport(result)
        #reported = self.trimResults(result)
        #print type(reported)
        #if reported:
            #if self.frequencyVal is None:
        #    showinfo("Saved", "Report has been saved!")
        #else:
        #    showinfo("Empty", "Nothing to report")
        #if self.frequencyVal is not None:
        #    self.timer = self.root.after(self.frequencyVal, self.Linux2Self)

    
    def Linux2Linux(self):
        '''Connect to server, read log file and return contents.  Ultimately want to loop through all machines'''
        print "Connecting Linux to Linux"
        command = ""
        result = []
        for i, path in enumerate(self.logpaths):
            if path[0] != "":
                command = command + "echo " + "\""+path[0]+"\"" +"; cat " + path[0] + "; echo"
                #command = command + "echo"

                if self.port == "":
                    cmd = ["sshpass", "-p", self.password, "ssh", "-X", 
                           self.server+"@"+self.ip, command]
                else:
                    cmd = ["sshpass", "-p", self.password, "ssh", "-X", 
                           self.server+"@"+self.ip, "-p", self.port, command]
            
                ssh = Popen(cmd, stdout=PIPE, stderr=PIPE)
                contents = ssh.stdout.readlines()
                result.append("\n\n" + path[0] + "\n\n")
                if len(contents) > 0:
                    temp = self.trimResultsByKeywords(contents, i)
                    result.append(self.trimResultsByDate(temp))

        self.saveReport(result)

            #if reported:
            #    if self.frequencyVal is None:
            #        showinfo("Saved", "Report Saved at "+ self.savepath)
            #else:
            #    showinfo("Empty", "Nothing to report")
            #if self.frequencyVal is not None:
            #    self.timer = self.root.after(self.frequencyVal, self.Linux2Linux)


    
    def Linux2Windows(self):
        print "Connecting Linux to Windows"
        
            

    # Connect Windows -> Self, Linux, Windows
    def Windows2Self(self):
        '''Connect to the 3 main Windows logs automatically, plus any user-specified ones'''
        print "Connecting Windows to Self"
        if self.server == "":
            server = None
        else:
            server = self.server
        #logTypes = ["System", "Application", "Security"]
        logTypes = []
        keywords = []
        #temp = self.keywordBoxes[0].get()
        #print "VARIOUS THINGS TO CHECK"
        #print self.email
        #print self.sendemail
        #print self.logpaths
        #print self.keywords
        if "systemcheck" in self.data.keys():
            if self.data["systemcheck"]:
                logTypes.append("System")
                keywords.append(self.expandKeywordChoices(self.data["winSystemKeywords"]))
                #keywords.append(self.data["winSystemKeywords"].split(","))
                
        if "appcheck" in self.data.keys():
            if self.data["appcheck"]:
                logTypes.append("Application")
                keywords.append(self.expandKeywordChoices(self.data["winAppKeywords"]))
                #keywords.append(self.data["winAppKeywords"].split(","))
                
        if "securitycheck" in self.data.keys():
            if self.data["securitycheck"]:
                logTypes.append("Security")
                keywords.append(self.expandKeywordChoices(self.data["winSecurityKeywords"]))
                #keywords.append(self.data["winSecurityKeywords"].split(","))
                
        print "\nWindows Keywords"
        print keywords
        print logTypes
        #print self.data["systemcheck"], self.data["winSystemKeywords"]
        #print self.data["appcheck"], self.data["winAppKeywords"]
        #print self.data["securitycheck"], self.data["winSecurityKeywords"]
        #keywords = temp.split(", ")
        print self.savepath
        savefolder = self.getSaveFolderWindows()
        print savefolder
        print self.data["UID"]
        logwin.getAllEvents(server, logTypes, savefolder, keywords, self.data["UID"], self.trimdate)
        
    """
    def Windows2Linux(self):
        print "Connecting Windows to Linux"
        name = self.serverBox.get()
        ipaddress = self.ipBox.get()
        password = self.passwordBox.get()

        paths = []
        for path in self.pathBoxes:
            paths.append(path.get())

        command = ""
        for path in paths:
            command = command + "echo " + "\""+path+"\"" +"; cat " + path + "; "
        command = command + "echo"

        cmd = ["plink.exe", name+"@"+ipaddress, "-pw", password, "-C", command]
        #print cmd
        ssh = Popen(cmd, stdout=PIPE, stderr=PIPE)
        result = ssh.stdout.readlines()
        #print len(result)
        if len(result) > 0:
            reported = self.trimResults(result)
            if reported:
                if self.frequencyVal is None:
                    showinfo("Saved", "Windows Report Saved at "+ self.savepath)
            else:
                showinfo("Empty", "Nothing to report")
            if self.frequencyVal is not None:
                self.timer = self.root.after(self.frequencyVal, self.Windows2Linux)
        
    def Windows2Windows(self):
        print "Connecting Windows to Windows"
        '''Method for connecting to a server while on a Windows platform'''
        #Connect to server.  Testing on local machine.
        pass
    """
    
    def getSaveFolderWindows(self):
        '''Get the folder we need to save the results in when on Windows platform'''
        if "Records" not in os.listdir(self.savepath):
            os.mkdir(self.savepath+"/Records")
        return self.savepath+"\Records"


    def expandKeywordChoices(self, keywordString):
        '''Take a string of keywords separated by commas, and return a list of all possibilities'''
        keywordsOut = []
        if len(keywordString) > 0:
            keywordList = keywordString.split(",")
            for keyword in keywordList:
                word = keyword.strip()
                word1 = word.upper()
                word2 = word.lower()
                word3 = word[0].upper()+word2[1:]
                wordlist = [word, word1, word2, word3]
                wordlist = list(set(wordlist))
                keywordsOut += wordlist
        return keywordsOut
        
    def trimResultsByKeywords(self, contents, index):
        '''Trim the results according to the keywords. Input result is a list of strings'''
        result = []
        for i, line in enumerate(contents):
            if self.keywords[index][0] != "":
                keywordlist = self.keywords[index]
                for keyword in keywordlist:
                    key1 = keyword.upper()
                    key2 = keyword.lower()
                    key3 = keyword[0].upper()+key2[1:]
                    if keyword in line or key1 in line or key2 in line or key3 in line:
                        result.append(line)
            else:
                result.append(line)
        return result

    def trimResultsByDate(self, contents):
        '''Trim the contents by the date and time'''
        result = []
        currentTime = time.localtime()
        for i, line in enumerate(contents):
            writeline = self.filterViaTime(line, currentTime)
            if writeline:
                result.append(line)
        return result

    def saveReport(self, result):
        '''Save the report in the Records directory'''
        filename = self.generateFilename()
        if "Records" not in os.listdir(self.savepath):
            os.mkdir(self.savepath+"/Records")
        
        f = open(self.savepath+"/Records/"+filename, "w+")
        for line in result:
            if isinstance(line, list):
                for subline in line:
                    f.write(subline)
            else:
                f.write(line)
        f.close()
        #Send out an email of report if it is set
        if self.sendemail and self.email != "":
            print "Reading generated mesage"
            message = open(self.savepath+"/Records/"+filename).read()
            #print message, len(message)
            emailer.sendEmail(message, self.email)
            print "Finished emailing message"

    def generateFilename(self):
        '''Generate the filename for the report'''
        ct = time.localtime()
        name = self.platform
        if self.server == "":
            server = "local"
        return name+"-"+server+"-"+str(self.UID)+"_"+str(ct.tm_year)+"-"+str(ct.tm_mon).zfill(2)+"-"+str(ct.tm_mday).zfill(2)+"_"+str(ct.tm_hour).zfill(2)+str(ct.tm_min).zfill(2)+".txt"
        
        
    def filterViaTime(self, line, current_time):
        '''Assuming all lines start with a time in the format of:  Mmm dd hh:mm:ss'''        
        month = line[:3]
        day = int(line[4:6])
        hour = int(line[7:9])
        minute = int(line[10:12])
        second = int(line[13:15])
        monthDict = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, 
                     "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
        month = monthDict[month]

        #print month, day, hour, minute, second
        #seconds = second + minute * 60 + hour * 3600 + day * 86400
        seconds = second + 60 * (minute + 60 * (hour + 24 * (day + 30 * month)))
        month_now = current_time.tm_mon
        day_now = current_time.tm_mday
        hour_now = current_time.tm_hour
        min_now = current_time.tm_min
        sec_now = current_time.tm_sec
        #seconds_now = sec_now + min_now * 60 + hour_now*3600 + day_now*86400
        seconds_now = sec_now + 60 * (min_now + 60 * (hour_now + 24 * (day_now + 30 * month_now)))
        time_dif = seconds_now - seconds
        time_check = 0
        #print "TRIM DATE"
        #print self.trimdate
        #print "END TRIM DATE"
        if self.trimdate == "5 min":
            time_check = 5*60
        elif self.trimdate == "10 min":
            time_check = 10*60
        elif self.trimdate == "30 min":
            time_check = 30*60
        elif self.trimdate == "1 hour":
            time_check = 60*60
        elif self.trimdate == "1 day":
            time_check = 24*60*60
        elif self.trimdate == "1 week":
            time_check = 7*24*60*60
        elif self.trimdate == "1 month":
            time_check = 30*24*60*60
        else:
            return True
        #print time_dif, time_check
        if time_dif <= time_check:
            return True
        return False

    """
    def stop(self):
        #print self.timer
        self.root.after_cancel(self.timer)
        showinfo("Stopped!", "Scheduler has been stopped!")

    def scheduleMachine(self):
        #self.test()
        #needs to be in milliseconds
        if self.frequency == "2 Min":
            freq = 2*60*1000
        elif self.frequency == "hourly":
            freq = 60*60*1000
        elif self.frequency == "Every 6 hours":
            freq = 60*60*6*1000
        elif self.frequency == "Every 12 hours":
            freq = 60*60*12*1000
        elif self.frequency == "daily":
            freq = 60*60*24*1000
        elif self.frequency == "weekly":
            freq = 60*60*24*7*1000
        elif self.frequency == "monthly":
            freq = 60*60*24*30*1000
        else:
            freq = None

        self.frequencyVal = freq
        if self.platform == "Linux":
            self.Linux2Linux()
        elif self.platform == "Windows":
            self.Windows2Linux()
        #print self.frequency
    """

    def formatKeywords(self, keywords):
        '''The keyword list will always be a 2d array with one string per entry.
        Each entry may be empty.  Need to split each entry using comma as separator'''
        temp = []
        print "Formatting Keywords"
        print keywords
        for junk in keywords:
            entry = junk[0]
            sublist = entry.split(",")
            for i in range(len(sublist)):
                sublist[i] = sublist[i].strip()
            temp.append(sublist)
        print temp
        print ""
        return temp
                
