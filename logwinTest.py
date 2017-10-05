import win32evtlog
import win32evtlogutil
import codecs
import os
import sys
import time
import traceback
import win32con
import winerror


def getEventLogs(server, logtype, logPath, keywords):
    '''Get event logs from the server by logtype and save to path'''
    print "Logging %s events" % logtype
    log = codecs.open(logPath, encoding='utf-8', mode='w')
    line_break = '-' * 80

    log.write("\n%s Log of %s Events\n" % (server, logtype))
    log.write("Created: %s\n\n" % time.ctime())
    log.write("\n" + line_break + "\n")
    hand = win32evtlog.OpenEventLog(server, logtype)
    total = win32evtlog.GetNumberOfEventLogRecords(hand)
    print "Total events in %s = %s" % (logtype, total)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    events = win32evtlog.ReadEventLog(hand, flags, 0)
    evt_dict = {win32con.EVENTLOG_AUDIT_FAILURE: 'EVENTLOG_AUDIT_FAILURE',
                win32con.EVENTLOG_AUDIT_SUCCESS: 'EVENTLOG_AUDIT_SUCCESS',
                win32con.EVENTLOG_INFORMATION_TYPE:'EVENTLOG_INFORMATION_TYPE',
                win32con.EVENTLOG_WARNING_TYPE:'EVENTLOG_WARNING_TYPE',
                win32con.EVENTLOG_ERROR_TYPE:'EVENTLOG_ERROR_TYPE'}

    try:
        events = 1
        while events:
            events = win32evtlog.ReadEventLog(hand, flags, 0)
                
            for b, ev_obj in enumerate(events):
                the_time = ev_obj.TimeGenerated.Format()
                evt_id = str(winerror.HRESULT_CODE(ev_obj.EventID))
                computer = str(ev_obj.ComputerName)
                cat = ev_obj.EventCategory
                record = ev_obj.RecordNumber
                msg = win32evtlogutil.SafeFormatMessage(ev_obj, logtype)
                source = str(ev_obj.SourceName)
                if not ev_obj.EventType in evt_dict.keys():
                    evt_type = "unknown"
                else:
                    evt_type = str(evt_dict[ev_obj.EventType])
                #if b == 0:
                #    print the_time

                if len(keywords) > 0:
                    for keyword in keywords:
                        if keyword in msg:
                            log.write("Event Date/Time: %s\n" % the_time)
                            log.write("Event ID / Type: %s / %s\n" % (evt_id, evt_type))
                            log.write("Record #%s\n" % record)
                            log.write("Source: %s\n\n" % source)
                            log.write(msg)
                            log.write("\n\n")
                            log.write(line_break)
                            log.write("\n\n")
                            break
                else:
                    #print "Should not be in here"
                    log.write("Event Date/Time: %s\n" % the_time)
                    log.write("Event ID / Type: %s / %s\n" % (evt_id, evt_type))
                    log.write("Record #%s\n" % record)
                    log.write("Source: %s\n\n" % source)
                    log.write(msg)
                    log.write("\n\n")
                    log.write(line_break)
                    log.write("\n\n")
                
                            

    except:
        print traceback.print_exc(sys.exc_info())

    print "Log creation finished.  Location of log is %s" % logPath
    with open(logPath) as f:
        for line in f:
            print line
        
    
def getPath(basePath, serverName, logtype, uid):
    ct = time.localtime()
    if serverName is None:
        s = os.path.join(basePath, "Windows-"+logtype+"-"+str(uid)+"_"+str(ct.tm_year)+
                         "-"+str(ct.tm_mon).zfill(2)+ "-"+str(ct.tm_mday).zfill(2)+
                         "_"+str(ct.tm_hour).zfill(2)+ str(ct.tm_min).zfill(2)+ ".log")
    else:
        s = os.path.join(basePath, serverName+"-"+logtype+"-"+str(uid)+"_"+str(ct.tm_year)+
                         "-"+str(ct.tm_mon).zfill(2)+ "-"+str(ct.tm_mday).zfill(2)+
                         "_"+str(ct.tm_hour).zfill(2)+ str(ct.tm_min).zfill(2)+ ".log")

    
    return s



def getAllEvents(server, logtypes, keywords):    
    #if not server:
    #    serverName = "localhost"
    #else:
    #    serverName = server
    for i, logtype in enumerate(logtypes):
        #path = getPath(basePath, server, logtype, uid)
        #print path
        #path = os.path.join(basePath, "%s_%s_hack.log" % (serverName, logtype))
        path = "junkinthetrunk.txt"
        getEventLogs(server, logtype, path, keywords[i])


#def test():
if __name__ == "__main__":
    server = "localhost"
    logtypes = ["System"]
    keywords = [""]
    getAllEvents(server, logtypes, keywords)
