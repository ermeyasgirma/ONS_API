# ONS_API


This repository contains the code for a REST API get request

When given a CASE_ID the API returns a json (stored in output.json) which contains the relevant Mortgage information for the Case

The API looks up the mortgage information for indiviuals in the region based on postcode and returns the approriate information from a csv file to make 
a decision about mortgage affordability

The API was also extended to use the avg household age and combine this with regional information to make a more informed decision

The API was built using Flask 

virtEnv.sh contains the shell commands for creating the venv and running the application api.py

# Run 

    ./virtEnv.sh


