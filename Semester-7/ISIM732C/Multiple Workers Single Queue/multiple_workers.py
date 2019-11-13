import queue as Queue
import threading
import time

inp = lambda f, cast=int: [cast(x) for x in f.readline().split()]
printf = lambda s='', *args, **kwargs: print(str(s).format(*args), flush=True, **kwargs)

SPEEDUP = 50
q = Queue.Queue(10)

def producer(customers):
    i, k = 0, 0
    while k < len(customers):
        while customers[k][0] == i:
            if not q.full():
                item = customers[k]
                q.put(item)
                k += 1
                if k == len(customers): break
        time.sleep(1/SPEEDUP)
        i += 1

def consumer(cId, num, numConsumers):
    global avgQueue, idle, cumDept, waiting, cnt, busyMask
    i, busy = 0, 0
    while len(cumDept) < num:
        if not busy and not q.empty():
            item = q.get()
            busy = item[1]
        i += 1
        if busy:
            busy -= 1
            if busy == 0:
                cumDept.append((i - item[0]))
                waiting.append((i - item[0] - item[1]))
            with lock:
                busyMask = busyMask | (1 << cId) if busy else busyMask & ~(1 << cId)
        else:
            idle[cId] += 1
        with lock:
            cnt = (cnt+1)%numConsumers
        if cnt == 0 or len(cumDept) == num:
            avgQueue += q.qsize()
            printf('Tick: {:03d}, Queue: {}, Busy Mask: {:0{}b}, Served: {}/{}', 
                i, q.qsize(), busyMask, numConsumers, len(cumDept), num)
            if len(cumDept) == num:
                avgQueue /= i
        time.sleep(1/SPEEDUP)

def getInput(filename='input.txt'):
    customers = []
    arrival = 0
    with open(filename) as f:
        numConsumers, t = inp(f)
        for _ in range(t):
            customer = inp(f)
            arrival += customer[0]
            customers.append((arrival, customer[1], _))
    return numConsumers, customers

if __name__ == '__main__':    
    
    numConsumers, customers = getInput()
    p = threading.Thread(target=producer, args=(customers,))
    consumers = []
    for _ in range(numConsumers):
        consumers.append(threading.Thread(target=consumer, args=(_, len(customers), numConsumers)))
    
    lock = threading.Lock()
    cumDept = []
    waiting = []
    idle = [0] * numConsumers
    avgQueue, cnt, busyMask = 0, 0, 0

    p.start()
    for consumer in consumers:
        consumer.start()
    p.join()
    for consumer in consumers:
        consumer.join()

    print('Departure Times:', cumDept)
    print('Waiting Times:', waiting)
    print('Average Waiting Time: ', sum(waiting)/len(customers))
    print('Avg Queue Length:', avgQueue)
    print('Idle Time:', idle)
