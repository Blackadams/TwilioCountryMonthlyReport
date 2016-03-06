# TwilioCountryMonthlyReport

This script gets generates three outputs; one CSV file showing containing the log of calls made in the date period. the CSV headers are:
CallSID, CountryCode, NumberCalled, CallPrice, CallDuration

You can import this into excel and use pivot tables to do some analysis.

The second CSV file is an analysis file, it uses the log file to perform some basic analysis and outputs:
Country, MinutesUsed, TotalPrice, NumberOfCalls

The terminal also outputs a JSON feed of the data so that you can use this in any server scripts you have running.

You will need to install / update the Twilio Python Library, to do this, please run command: 

pip install twilio

