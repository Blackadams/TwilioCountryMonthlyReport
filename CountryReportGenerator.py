#!/usr/bin/python3

"""
This script gets generates three outputs; one CSV file showing containing the log of calls made in the date period. the CSV headers are:
CallSID, CountryCode, NumberCalled, CallPrice, CallDuration

You can import this into excel and use pivot tables to do some analysis.

The second CSV file is an analysis file, it uses the log file to perform some basic analysis and outputs:
Country, MinutesUsed, TotalPrice, NumberOfCalls

The terminal also outputs a JSON feed of the data so that you can use this in any server scripts you have running.

"""

__author__ = "Mathew Jenkinson"
__copyright__ = "Copyright 2016, Mathew Jenkinson"
__credits__ = ["Mathew Jenkinson"]
__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Mathew Jenkinson"
__status__ = "Prototype"

import datetime
import csv
import os
import gc
from twilio.rest import TwilioRestClient
from twilio.rest.lookups import TwilioLookupsClient

ACCT = "" # Put your accountsid here
AUTH = "" # Put your authToken here

# Date Range input, we need to know what date range we are making this report for.
From_Date_Input = "2016-02-01" # Example 1st Feb
To_Date_Input = "2016-02-02" # Example 1st March - this will give us the month of Feb data

client = TwilioRestClient(ACCT, AUTH)
lookupclient = TwilioLookupsClient(ACCT, AUTH)

CalledStatistics = {}

with open("TwilioCallLog.csv", "w") as csvfile:
    csvfile.write("CallSID, CountryCode, NumberCalled, CallPrice, CallDuration\n")
    # If the to / From is blank or is a client we can skip the writing to
    # the file as we only want phone numbers.
                                      
    for call in client.calls.iter(page_size=1000, started_after=From_Date_Input, started_before=To_Date_Input):
        if call.direction == "outbound-dial":
            if call.to.startswith("+"):
                # if the row starts with a + it means its an E.164 number and that we need to use lookup to workout the country code, the end row will look like:
                # US,+1987654321,price
                try:
                    number = lookupclient.phone_numbers.get(call.to)
                    callCountryCode = number.country_code
                except:
                    callCountryCode = "UNKNOWN"


                if call.price:
                    call_price = call.price.replace("-","")
                else:
                    call_price = "0"
                
                if callCountryCode not in CalledStatistics:
                    CalledStatistics[callCountryCode] = {'CallDuration' : int(call.duration),'CallPrice' : float(call_price), 'Frequency' : 1}
                else:
                    CalledStatistics[callCountryCode]['CallDuration'] += int(call.duration)
                    CalledStatistics[callCountryCode]['CallPrice'] += float(call_price)
                    CalledStatistics[callCountryCode]['Frequency'] += 1
        
                callRowInformation = str(call.sid)+","+str(callCountryCode)+","+str(call.to)+","+str(call.price)+","+str(call.duration)+"\n"
                csvfile.write(callRowInformation)
gc.collect()
print("Got the call log data for the dates specified. The file is called: TwilioCallLog.csv Beginning Analysis...")
print(CalledStatistics)

# Now we have the call data both in a CSV and in a dict we can look to analise and present back file of statistics on this call.
with open("TwilioCallAnalysis.csv", "w") as analysisFile:
    analysisFile.write("Country, MinutesUsed, TotalPrice, NumberOfCalls\n")

    for CountryCodeKey in CalledStatistics:
        countryInformationRow = CountryCodeKey+","+str(CalledStatistics[CountryCodeKey]['CallDuration'])+","+str(CalledStatistics[CountryCodeKey]['CallPrice'])+","+str(CalledStatistics[CountryCodeKey]['Frequency'])+"\n"
        analysisFile.write(countryInformationRow)
