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
    return

def consumer(num):
    global avgQueue, idle, cumDept
    i, k, busy = 0, 0, 0
    while k < num:
        if not busy and not q.empty():
            item = q.get()
            busy = item[1]
        time.sleep(1/SPEEDUP)
        i += 1
        if busy:
            busy -= 1
            if busy == 0:
                cumDept.append(i - item[0])
                k += 1
        else:
            idle += 1
        avgQueue += q.qsize()
        printf('Tick: {:03d}, Queue: {}, Busy: {}, Served: {}/{}', i, q.qsize(), int(busy > 0), k, num)
    avgQueue /= i
    return

def getInput(filename='input.txt'):
    customers = []
    arrival = 0
    with open(filename) as f:
        t, = inp(f)
        for _ in range(t):
            customer = inp(f)
            arrival += customer[0]
            customers.append((arrival, customer[1], _))
    return customers

if __name__ == '__main__':
    cumDept = []
    idle = 0
    avgQueue = 0
    customers = getInput()
    p = threading.Thread(target=producer, args=(customers,))
    c = threading.Thread(target=consumer, args=(len(customers),))
    p.start(), c.start()
    p.join(),  c.join()
    print('Departure Times:', cumDept)
    print('Avg Queue Length:', avgQueue)
    print('Idle Time:', idle)
