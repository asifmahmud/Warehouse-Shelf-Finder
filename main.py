from ShelfFinder import ShelfFinder
import time
import sys

def main():
    '''
    startLocation   = input("Hello user, where is your worker?: ")
    endLocation     = input("Where is your worker's end location?: ")
    order           = input("What items would you like to pick?: ")
    orderFile       = input("Please list file of orders to be processed: ")
    orderOutputFile = input("Please list output file: ")
    '''
    startLocation   = "(0,0)"
    endLocation     = "(0,0)"
    #order           = "231434,286783,259538,348200,1101294,110,660042,54430,395701,236272"
    orderFile       = "warehouse-orders-v01.csv"
    orderOutputFile = "output.txt"

    startLocation   = startLocation.strip("()").split(",")
    startLocation   = (int(startLocation[0]), int(startLocation[1]))
    endLocation     = endLocation.strip("()").split(",")
    endLocation     = (int(endLocation[0]), int(endLocation[1]))

    #order = [int(i) for i in order.strip().split(",")]
    finder = ShelfFinder(startLocation, endLocation, orderFile, orderOutputFile)
    '''
    t1 = time.time()
    a,b = finder.optimizedOrder(order)
    t2 = time.time()
    print(a,b)
    print("Time taken: {:.2f} secs".format(t2-t1))
    '''
    print("Please wait.....")
    #if len(order) > 0: finder.batchOrder(order)
    finder.batchOrder()

    return 0


if __name__ == '__main__':
    sys.exit(main())