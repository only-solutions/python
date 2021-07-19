import os
import time
from multiprocessing import Process, Queue
from collections import deque

# Copyright: S. Nagi 2020
# All Rights Reserved

#Notes:
#RLock might not be required
#key to making it work was adding time.sleep(0.001) to give main thread time to run
#lock = RLock()

def gendata(dq, kq, usekey,filekeysize, filedatasize):
    #time.sleep(1)  # give producer/main thread an opportunity to add first items to queue (like C yield)
    print('filesizes: ' + str(filedatasize) + ' ' + str(filekeysize))
    keyadjmax = usekey[0]
    #    print('keyadjmax: ' + str(keyadjmax))
    useq = dq
    otherq = kq
    kprocessed = 0
    dprocessed = 0
    with open("testout.dat", "wb") as h:
        tryq = 0
        while True:
            #            print('kq.qsize: '+str(kq.qsize())+' dq.qsize: '+str(dq.qsize()))
            #time.sleep(0)  # give producer/main thread an opportunity to add to queue (like C yield)
            # if stops working try 0.001
            if keyadjmax == 0:
                newl = deque(usekey)
                newl.rotate(-1)
                usekey = list(newl)
                keyadjmax = usekey[0]
                #            print('keyadjmax: ' + str(keyadjmax))
                if useq == dq:
                    useq = kq
                    otherq = dq
                else:
                    useq = dq
                    otherq = kq
            try:
                if useq.qsize() > 0:
                    #with lock:
                    databytes = useq.get()  # parameters might be unnecessary - added just in case
                    #dataval = databytes.decode("utf-8")
                    #print('type is '+str(type(databytes)))
                    #print('read in '+dataval)
                    h.write(databytes)
                    #h.flush()
                    if useq == kq: kprocessed = kprocessed + 1
                    if useq == dq: dprocessed = dprocessed + 1
                    #print('kprocess: '+str(kprocessed)+' dprocess: '+str(dprocessed))
                    #print("data: " + dataval)
                    #                print("qid: "+str(id(useq)))
                    # someval = useq.get()
                    keyadjmax = keyadjmax - 1
                    #queue has no elements, but it could be because the producer thread is still reading the file
                    #so only switch to other queue if we read this file in completely
                    if (useq.qsize() == 0) and ((useq == kq and kprocessed == filekeysize) or
                                                (useq == dq and dprocessed == filedatasize) ):
                        keyadjmax = 0
                    #with lock:
                if useq.qsize() == 0 and keyadjmax != 0:
                    keyadjmax = 0
                if kprocessed == filekeysize and dprocessed == filedatasize:
                    #print('break out of loop - required to write output file')
                    break

            except Exception as e:
                print('ERROR: ' + str(e))


dataq = Queue(0)
keyq = Queue(0)
testkey = [3, 1, 2, 1, 4, 1]
reversekey = list(testkey)
reversekey.reverse()
testkey.extend(reversekey)
print('key is:')
print(testkey)

filedata = "test.dat"
filekey = "test2.dat"

filedatasize = os.stat(filedata).st_size
filekeysize = os.stat(filekey).st_size

genDataProcess = Process(target=gendata, args=(dataq, keyq, testkey,filekeysize,filedatasize,))
genDataProcess.daemon = True
genDataProcess.start()  # must populate queues first before starting consumer/worker thread

loopcnt = 1
#note: this did not help performance
#with open(filedata, "rb", buffering=(2<<16) + 8) as f, open("test2.dat", "rb",  buffering=(2<<16) + 8) as g:
with open(filedata, "rb") as f, open("test2.dat", "rb") as g:
    dbytes = f.read()
    kbytes = g.read()
    while dbytes:
        # dataval = bytes.decode("utf-8")
        #with lock:
#logic assumes both files are same size
        for db_q in dbytes: dataq.put(b'%c' % db_q)
        for kb_q in kbytes: keyq.put(b'%c' % kb_q)
        dbytes = f.read()
        kbytes = g.read()
#        print('loopcnt '+str(loopcnt))
#        loopcnt = loopcnt + 1

#      print(tmpl, end ="")

genDataProcess.join()

#if __name__ == '__main__':
#    app.run()

