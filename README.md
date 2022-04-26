# ONS_API


This repository contains the code for a REST API get request

When given a CASE_ID the API returns a json (stored in output.json) which contains the relevant Mortgage information for the Case

The API looks up the mortgage information for indiviuals in the region based on postcode and returns the approriate information from a csv file to make 
a decision about mortgage affordability

The API was also extended to use the avg household age and combine this with regional information to make a more informed decision

The API was built using Flask 

virtEnv.sh contains the shell commands for creating the venv and running the application api.py

    - and the pip installs you should do prior

Once you have run the last command : flask run

The terminal will show a hyperlink to a local webpage which will tell you it wants a case_id

    - to which you will add a dash "/" then the appropriate case_id

    - and it will display what was written to output.json

In the event that you get weird errors and the api.py doesn't work (although it should) :

    the runAPI.sh contains the bash commands to run ons_api.py by itself 

    So do the following 

        - chmod u+x runAPI.sh 

                - this gives you the correct access

        - ./runAPI.sh <case_id>

            - 56763bf7-d046-4a54-a4a1-0728c724a092
                - use this case_id to save time as it's kind of the only one available