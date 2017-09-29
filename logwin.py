import win32evtlog
import win32evtlogutil
import codecs
import os
import sys
import time
import traceback
import win32con
import winerror

def filterByDateTime(the_time, trimdate):
    ct = time.localtime()
    if trimdate == "5 min":
        time_check = 5*60
    elif trimdate == "1 hour":
        time_check = 60*60
    elif trimdate == "12 hours":
        time_check = 12*60*60
    elif trimdate == "1 day":
        time_check = 24*60*60
    elif trimdate == "1 week":
        time_check = 7*24*60*60
    elif trimdate == "1 month":
        time_check = 4*7*24*60*60
    else:
        return True

    date, dt = the_time.split(" ")
    month = int(date.split("/")[0])
    day = int(date.split("/")[1])
    hour = int(dt.split(":")[0])
    minute = int(dt.split(":")[1])
    second = int(dt.split(":")[2])
    seconds = second + 60 * (minute + 60 * (hour + 24 * (day + 30 * month)))
    
    month_now = ct.tm_mon
    day_now = ct.tm_mday
    hour_now = ct.tm_hour
    min_now = ct.tm_min
    sec_now = ct.tm_sec
    seconds_now = sec_now + 60 * (min_now + 60 * (hour_now + 24 * (day_now + 30 * month_now)))
    time_dif = seconds_now - seconds
    if time_dif <= time_check:
        return True
    return False

def getEventLogs(server, logtype, logPath, keywords, trimdate):
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
                if filterByDateTime(the_time, trimdate):    
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



def getAllEvents(server, logtypes, basePath, keywords, uid, trimdate):    
    #if not server:
    #    serverName = "localhost"
    #else:
    #    serverName = server
    for i, logtype in enumerate(logtypes):
        path = getPath(basePath, server, logtype, uid)
        print path
        #path = os.path.join(basePath, "%s_%s_hack.log" % (serverName, logtype))
        getEventLogs(server, logtype, path, keywords[i], trimdate)



