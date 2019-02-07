import multiprocessing
import time
import os
import psutil

def func1(sharedQueue, sharedLock,affinity):
    print("Process 1 started ", os.getpid())
    #os.system("taskset -p 0xFFFFFFFF %d" % os.getpid())
    proc = psutil.Process()
    proc.cpu_affinity(affinity)

    i=0
    while 1:
        #sharedLock.acquire()
        if not sharedQueue.empty():
            value = sharedQueue.get()
            print(">>>>>total values processed ", i)
            print("")
            i+=1
            #sharedLock.release()
            if value == None:
                break
        #else:
            #sharedLock.release()


def func2(sharedQueue, sharedLock, affinity):
    proc = psutil.Process()
    proc.cpu_affinity(affinity)
    print("Process 2 started ", os.getpid())
    #os.system("taskset -p 0xFFFFFFFF %d" % os.getpid())
    i=0
    #while(1):
    for i in range(0, 100000):
        #sharedLock.acquire()
        sharedQueue.put(i)
        print("......... inserted ", i)
        i+=1
        #time.sleep(0.25)
        #sharedLock.release()
    #sharedLock.acquire()
    sharedQueue.put(None)
    #sharedLock.release()

    return


sharedQueue = multiprocessing.Queue()
sharedLock = multiprocessing.Lock()

affinity = [0]
d=dict(affinity=affinity)
p1 = multiprocessing.Process(target=func1, args=[sharedQueue, sharedLock], kwargs=d)
affinity = [0]
d=dict(affinity=affinity)
p2 = multiprocessing.Process(target=func2, args=[sharedQueue, sharedLock], kwargs=d)
p1.start()
p2.start()
allpcs = []
allpcs.append(p1)
allpcs.append(p2)
print(multiprocessing.cpu_count())
print(len(allpcs))

for pc in allpcs:
    if pc is not None:
        pc.join()

