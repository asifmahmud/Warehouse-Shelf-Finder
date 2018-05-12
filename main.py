from ShelfFinder import ShelfFinder
import time
import sys

def main():
    startLocation   = input("Hello user, where is your worker?: ")
    endLocation     = input("Where is your worker's end location?: ")
    order           = input("What items would you like to pick?: ")
    orderFile       = input("Please list file of orders to be processed: ")
    orderOutputFile = input("Please list output file: ")
    algorithm       = input("Which algorithm should be used? ([bnb]: Branch and Bound, [nn]: Nearest Neighbor, [hk]: Held-Karp)")
    '''
    startLocation   = "(0,0)"
    endLocation     = "(0,0)"
    order           = "281610,342706,111873,198029,366109,287261,76283,254489,258540,286457"
    orderFile       = "warehouse-orders-v01.csv"
    orderOutputFile = "output2.txt"
    algorithm       = "bnb" 
    '''

    startLocation   = startLocation.strip("()").split(",")
    startLocation   = (int(startLocation[0]), int(startLocation[1]))
    endLocation     = endLocation.strip("()").split(",")
    endLocation     = (int(endLocation[0]), int(endLocation[1]))

    order = [int(i) for i in order.strip().split(",")]
    finder = ShelfFinder(startLocation, endLocation, algorithm, orderFile, orderOutputFile)
    '''
    t1 = time.time()
    a,b,c = finder.optimizedOrder(order)
    t2 = time.time()
    print(a,b,c)
    print("Time taken: {:.2f} secs".format(t2-t1))
    '''
    print("Please wait.....")
    if len(order) > 0: finder.batchOrder(order)
    finder.batchOrder()
    return 0


if __name__ == '__main__':
    sys.exit(main())