#!/usr/bin/python
"""This script can be used to analyze data in the 2012 Presidential Campaign,
available from ftp://ftp.fec.gov/FEC/2012/pas212.zip - data dictionary is at
http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionstoCandidates.shtml
"""

import fileinput
import csv



##### PROCESSING SECTION #####

def calculate_median(values):
    values = sorted(values)
    if len(values) % 2 == 1:
        return values[len(values) / 2]
    else:
        return (values[len(values) / 2 - 1] + values[len(values) / 2]) / 2

def calculate_standard_deviation(values, mean):
    return ( sum([abs(value - mean) ** 2 for value in values]) / len(values) ) ** 0.5

# Build mapping:
# candidate ID --> list of contributions to candidate
contributions_by_candidate_ID = {}
[contributions_by_candidate_ID.setdefault(row[16], []).append(float(row[14])) for row in csv.reader(fileinput.input(), delimiter='|') if not fileinput.isfirstline()]

# Build mapping:
# candidate ID --> dictionary of statistics on candidate
statistics_by_candidate_ID = {}
for candidate_ID, contributions in contributions_by_candidate_ID.iteritems():
    total = sum(contributions)
    minimum = min(contributions)
    maximum = max(contributions)
    mean = total / len(contributions)
    median = calculate_median(contributions)
    standard_deviation = calculate_standard_deviation(contributions, mean)

    statistics_by_candidate_ID[candidate_ID] = {
        'Total': total,
        'Min': minimum,
        'Max': maximum,
        'Mean': mean,
        'Median': median,
        'Std dev': standard_deviation,
    }

# Calculate statistics across all candidates
contributions = [contribution for contributions in contributions_by_candidate_ID.values() for contribution in contributions]
total = sum(contributions)
minimum = min(contributions)
maximum = max(contributions)
mean = total / len(contributions)
median = calculate_median(contributions)
standard_deviation = calculate_standard_deviation(contributions, mean)



##### OUTPUT SECTION #####

# Print stats for individual candidates
print 'STATISTICS FOR INDIVIDUAL CANDIDATES:'
for candidate_ID, statistics in statistics_by_candidate_ID.iteritems():
    print 'Candidate ID: ' + candidate_ID
    for statistic_type, statistic_value in statistics.iteritems():
        print '   ' + statistic_type + ': ' + '%.1f' % statistic_value,
    print ''

# Print global stats (across all candidates)
print '\nGLOBAL STATISTICS (ACROSS ALL CANDIDATES):'
print "Total: " + str(total)
print "Minimum: " + str(minimum)
print "Maximum: " + str(maximum)
print "Mean: " + str(mean)
print "Median: " + str(median)
print "Standard Deviation: " + str(standard_deviation)
print ''

##### Comma separated list of unique candidate ID numbers
# Note: instead of printing this, I print the candidate ID numbers above
# along with each one's individual stats.

def minmax_normalize(value):
    """Takes a donation amount and returns a normalized value between 0-1. The
    normalization should use the min and max amounts from the full dataset"""
    return (value - minimum) / (maximum - minimum)

##### Normalize some sample values
print "Min-max normalized values: %r" % map(minmax_normalize, [2500, 50, 250, 35, 8, 100, 19])
