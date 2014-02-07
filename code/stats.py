#!/usr/bin/python
"""This script can be used to analyze data in the 2012 Presidential Campaign,
available from ftp://ftp.fec.gov/FEC/2012/pas212.zip - data dictionary is at
http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionstoCandidates.shtml
"""

import fileinput
import csv

def calculate_median(values):
    values = sorted(values)
    if len(values) % 2 == 1:
        return values[len(values) / 2]
    else:
        return (values[len(values) / 2] + values[len(values) / 2 + 1]) / 2

def calculate_standard_deviation(values, mean):
    return ( sum([abs(value - mean) ** 2 for value in transaction_amounts]) / len(transaction_amounts) ) ** 0.5


rows = [row for row in csv.reader(fileinput.input(), delimiter='|') if not fileinput.isfirstline()]

transaction_amounts = [float(row[14]) for row in rows]
candidate_IDs = set([row[16] for row in rows])

total = sum(transaction_amounts)
minimum = min(transaction_amounts)
maximum = max(transaction_amounts)
mean = total / len(transaction_amounts)
median = calculate_median(transaction_amounts)
standard_deviation = calculate_standard_deviation(transaction_amounts, mean)


##### Print out the stats
print "Total: " + str(total)
print "Minimum: " + str(minimum)
print "Maximum: " + str(maximum)
print "Mean: " + str(mean)
print "Median: " + str(median)
print "Standard Deviation: " + str(standard_deviation)

##### Comma separated list of unique candidate ID numbers
print "Candidates: " + ', '.join(candidate_IDs)
print '\n'

def minmax_normalize(value):
    """Takes a donation amount and returns a normalized value between 0-1. The
    normalization should use the min and max amounts from the full dataset"""
    ###
    # TODO: replace line below with the actual calculations
    # norm = value
    ###/
    return (value - minimum) / (maximum - minimum)

##### Normalize some sample values
print "Min-max normalized values: %r" % map(minmax_normalize, [2500, 50, 250, 35, 8, 100, 19])
