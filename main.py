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
    algorithm       = input("Which algorithm should be used? ([bnb]: Branch and Bound, [nn]: Nearest Neighbor, [hk]: Held-Karp): ")
    weightFactor    = input("Do you want to factor in weight in trip calculation? Y/N: ")
    '''
    startLocation   = "(0,0)"
    endLocation     = "(0,18)"
    order           = "33139, 33321, 34068, 35704, 35785"
    orderFile       = "warehouse-orders-v02-tabbed."
    orderOutputFile = "output2.txt"
    algorithm       = "bnb" 
    weightFactor    = "Y"    
    
    startLocation   = startLocation.strip("()").split(",")
    startLocation   = (int(startLocation[0]), int(startLocation[1]))
    endLocation     = endLocation.strip("()").split(",")
    endLocation     = (int(endLocation[0]), int(endLocation[1]))
    weightFactor    = True if weightFactor in "Yy" else False

    order = [int(i) for i in order.strip().split(",")]
    finder = ShelfFinder(startLocation, endLocation, algorithm, orderFile, orderOutputFile, weightFactor)
    
    t1 = time.time()
    res = finder.optimizedOrder(order)
    t2 = time.time()
  
    string = '''
            Original Cost: {}\n
            Original Effort: {:.2f}\n
            Optimal Cost: {}\n
            Optimal Path: {}\n
            Optimal Effort: {:.2f}\n
    '''.format(res[0], res[1], res[2], res[3], res[4])
    
    print(string)
    print("Time taken: {:.2f} secs".format(t2-t1))
    '''
    print("Please wait.....")
    if len(order) > 0: finder.batchOrder(order)
    finder.batchOrder()
    '''
    return 0


if __name__ == '__main__':
    sys.exit(main())