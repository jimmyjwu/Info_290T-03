#!/usr/bin/python
"""Script can be used to calculate the Gini Index of a column in a CSV file.

Classes are strings."""

import fileinput
import csv
from collections import *

(
    CMTE_ID, AMNDT_IND, RPT_TP, TRANSACTION_PGI, IMAGE_NUM, TRANSACTION_TP,
    ENTITY_TP, NAME, CITY, STATE, ZIP_CODE, EMPLOYER, OCCUPATION,
    TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID, CAND_ID, TRAN_ID, FILE_NUM,
    MEMO_CD, MEMO_TEXT, SUB_ID
) = range(22)

CANDIDATES = {
    'P80003338': 'Obama',
    'P80003353': 'Romney',
}

############### Set up variables
# TODO: declare datastructures
contributions_by_zip_and_candidate = {}
contributions_by_candidate = {candidate: 0 for candidate in CANDIDATES.itervalues()}

############### Read through files
for row in csv.reader(fileinput.input(), delimiter='|'):
    candidate_id = row[CAND_ID]
    if candidate_id not in CANDIDATES:
        continue

    candidate_name = CANDIDATES[candidate_id]
    zip_code = row[ZIP_CODE]
    ###
    # TODO: save information to calculate Gini Index
    ##/
    contributions_by_zip_and_candidate.setdefault(zip_code, defaultdict(int))[candidate_name] += 1
    contributions_by_candidate[candidate_name] += 1

###
# TODO: calculate the values below:
gini = 0  # current Gini Index using candidate name as the class
split_gini = 0  # weighted average of the Gini Indexes using candidate names, split up by zip code
##/
def gini_index(values):
    total = float(sum(values))
    return 1 - sum([ (value / total) ** 2 for value in values])

# Gini index for all zip codes
gini = gini_index(contributions_by_candidate.values())

total_contributions = float(sum(contributions_by_candidate.itervalues()))
def zip_code_weight(contributions_by_candidate):
    return sum(contributions_by_candidate) / total_contributions

# Average Gini index over zip codes, weighted by number of records in that zip code
split_gini = sum([zip_code_weight(contributions_in_zip_by_candidate.values()) * gini_index(contributions_in_zip_by_candidate.values()) for contributions_in_zip_by_candidate in contributions_by_zip_and_candidate.itervalues()])

print "Gini Index: %s" % gini
print "Gini Index after split: %s" % split_gini

"""
OUTPUT:
Gini Index: 0.487709185938
Gini Index after split: 0.414381001914
"""
