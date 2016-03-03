#!/usr/bin/env python

"""
This script gets generates a CSV File showing; price, number of calls and countries called for a specified date range. 

Example is:
Price(USD), Calls, Country
0.4, 2, Costa Rica

At the end of the script it saves this file as CallReport.CSV
"""

__author__ = "Mathew Jenkinson"
__copyright__ = "Copyright 2016, Mathew Jenkinson"
__credits__ = ["Mathew Jenkinson"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Mathew Jenkinson"
__status__ = "Prototype"

import datetime
import csv
import os
import gc
from twilio.rest import TwilioRestClient

ACCT = os.environ['TWILIO_ACCOUNT_SID'] # Put your accountsid here
AUTH = os.environ['TWILIO_AUTH_TOKEN'] # Put your authToken here

# Date Range input, we need to know what date range we are making this report for.
print("Whats the date range for this report? ")
From_Date_Input = raw_input("When are we collecting from? Please type in the date to start from in YYYY-MM-DD format: ")
To_Date_Input = raw_input("When are we collecting to? Please type in the date to start from in YYYY-MM-DD format: ")

client = TwilioRestClient(ACCT, AUTH)

with open("TwilioCallLog.csv", "w") as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    # If the to / From is blank or is a client we can skip the writing to
    # the file as we only want phone numbers.
    for call in client.calls.iter(page_size=1000,
                                  started_after=START_AFTER_DATE):
                                      
    for call in client.calls.iter(page_size=1000, 
                                    started_after=START_AFTER_DATE, 
                                    started_before=STOP_Date):
        if call.to.startswith("+"):
            writer.writerow([call.to.strip("+")])
        if call.from_.startswith("+"):
            writer.writerow([call.from_.strip("+")])
gc.collect()
