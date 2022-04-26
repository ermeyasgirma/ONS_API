from curses.ascii import isdigit
import pandas as pd
import json
import sys

'''
# API get request requires authentication and sign- in so couldn't fetch from gitlab
url = 'https://gitlab.com/acresoftware/recruitment/be-tech-test-eg/-/blob/master/case.json'
req = requests.get(url)
req.json()
'''



regions = {}

def reader():
    with open('postcodelookup.txt', 'r') as file1:
        lines = file1.readlines()
        for line in lines:
            arr1 = line.split(":")
            region = arr1[0]
            postcodes = []
            for pc in arr1[1].split(" "):
                if not(pc == "" or pc == "\n"):
                    postcodes.append(pc)
            regions[region] = postcodes


regionToCol = {"North East" : "G", "North West" : "H", "Yorkshire and the Humber" : "I", "East Midlands" : "J", "West Midlands" : "K", "East" : "L", "London" : "M", 
"South East" : "N", "South West" : "O"}

cols = ["outgoings water", "outgoings communications", "outgoings_mortgage_rent", "outgoings_insurance", "outgoings_investments", "outgoings_council_tax",
"outgoings_food", "outgoings_clothing", "outgoings_other_living_costs", "outgoings_entertainment", "outgoings_holidays", "outgoings_sports", "outgoings_pension",
"outgoings_car_costs", "outgoings_other_transport_costs", "outgoings_child_care", "outgoings_fuel", "outgoings_ground_rent_service_charge_shared_equity_rent ",
"outgoings_television_license", "outgoings_household_repairs"]
rows = [98, 155, 260, 240, 281, 260, 4, 70, 226, 188, 199, 184, 276, 138, 140, 79, 103, 91, 187, 121 ] # not sure what additional details means
#rows = [97, 155, 260, 240, 281, 260, 4, 70, 226, 188, 199, 183, 276, 138+139, 140, 79+265+268, 103, 91, 187, 121 ] 
values = {}

def checkRegion(pc):
    for region in regions:
        if (regions[region]).count(pc) > 0:
            return region

def parseJSON(jsondata):
    postcode = jsondata['clients'][0]['details']['address']['postcode']
    prefix = ""
    if isdigit(postcode[1]):
        prefix += postcode[0]
    else:
        prefix += postcode[0] + postcode[1]
    return prefix

def read_val_fromRegionExcel(filename, row, col):
    return pd.read_excel('ONSByRegion2019.xls', skiprows= row-1, usecols=col, nrows=1, header=None, names=["Value"]).iloc[0]["Value"]

def read_val_fromCompExcel(filename, row, col):
    return pd.read_excel('ONSComposition2019.xls', skiprows= row-1, usecols=col, nrows=1, header=None, names=["Value"]).iloc[0]["Value"]


def affordability(jsondata):
    postcode = parseJSON(jsondata)
    #print(postcode)
    region  = checkRegion(postcode)
    # use region to find appropriate column in excel file
    for i in range(len(cols)):
        cost_name = cols[i]
        row = rows[i]
        column = regionToCol[region]
        val = str(read_val_fromRegionExcel('', row, column))
        val = val.replace("[", "")
        val = val.replace("]", "")
        values[cost_name] = float(val)
    #print(values)
    return values


def mainAPI(case_id):
    j = open('case.json')
    jdata = json.load(j)
    output = affordability(jdata)
    #print(output)
    identifier = {"case_id" : case_id, "values" : output}
    idjson =  json.dumps(identifier, indent=4)
    with open('output.json', 'w') as outputwrite:
        outputwrite.seek(0)
        outputwrite.truncate()
        outputwrite.write(idjson)
        outputwrite.close()
    return output


reader()
#mainAPI('56763bf7-d046-4a54-a4a1-0728c724a092')
mainAPI(sys.argv[1])

