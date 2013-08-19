# -*- coding: cp1252 -*-
from __future__ import division
import sys

coin_holder = {"1.00":10,
               "0.50":10,
               "0.20":10,
               "0.10":10,
               "0.05":10,
               "0.02":10,
               "0.01":10}
               

coins = [100,50,20,10,5,2,1]



def average(values):
    """Computes the arithmetic mean of a list of numbers.

    >>> print average([20, 30, 70])
    40.0
    """
    return sum(values, 0.0) / len(values)


def calc_change(change,verbose):
    total_coins = 0
    index = 0
    
    if verbose: print "Change Needed:£%.2f" % (change/100)
    while (change > 0):
        amount =int( change / coins[index])
        #amount = change / coins[index]
        #print "int(",change,"/", coins[index], ")=", amount
        if amount:
            #print "Index: %d" % index
            change -= (coins[index]*amount)
            total_coins += amount
        if verbose:  print "Change Needed:£%.2f  %d x £%.2f" % (change/100,amount,coins[index]/100)
        index = index + 1
        if index > (len(coins)-1):
            change = 0
    if verbose: print "Totals Coins: %d" % (total_coins)

    return total_coins

if __name__ == "__main__":

    data = []
    max_coins = 0
    change = 0
    while change < 100:
        nocoins = calc_change(change,1)
        change += 1
        data.append(nocoins)
        
    print "Average: ", average(data)
    print "Max: ", max(data)
    print "Min: ", min(data)
    #print calc_change(15)
    
