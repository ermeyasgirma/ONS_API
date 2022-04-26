from curses.ascii import isdigit
from datetime import datetime
from re import I
import pandas as pd
import json
import sys
from dateutil import relativedelta
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

ageToCol = {29 : "E", 49 : "F", 64 : "G", 74 : "H", 75 : "I"}

cols = ["outgoings water", "outgoings communications", "outgoings_mortgage_rent", "outgoings_insurance", "outgoings_investments", "outgoings_council_tax",
"outgoings_food", "outgoings_clothing", "outgoings_other_living_costs", "outgoings_entertainment", "outgoings_holidays", "outgoings_sports", "outgoings_pension",
"outgoings_car_costs", "outgoings_other_transport_costs", "outgoings_child_care", "outgoings_fuel", "outgoings_ground_rent_service_charge_shared_equity_rent ",
"outgoings_television_license", "outgoings_household_repairs"]
rows = [98, 155, 260, 240, 281, 260, 4, 70, 226, 188, 199, 184, 276, 138, 140, 79, 103, 91, 187, 121 ] # not sure what additional details means

values = {}

colsAge = ["outgoings water", "outgoings communications", "outgoings_mortgage_rent"]
rowsAge = [97,  151, 251]

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

def getAge(date):
    format = date.split("/")
    year = int(format[0])
    month = int(format[1].replace("0", ""))
    day = int(format[2].replace("0", ""))
    date1 = datetime(year, month, day)
    date2 = datetime(2022, 4, 26)
    diff = relativedelta.relativedelta(date2, date1)
    return diff.years

def avgAge(jsondata):
    age1 = jsondata['clients'][0]['details']['dob']
    age2 = jsondata['clients'][1]['details']['dob']
    calcAge = getAge(age1)
    calcAge2 = getAge(age2)
    return (calcAge + calcAge2)/2

def getcolAge(age):
    if age < 30:
        return "E"
    elif age < 50:
        return "F"
    elif age < 65:
        return "G"
    elif age < 75:
        return "H"
    else:
        return "I" 

def read_val_fromRegionExcel(filename, row, col):
    return pd.read_excel('ONSByRegion2019.xls', skiprows= row-1, usecols=col, nrows=1, header=None, names=["Value"]).iloc[0]["Value"]

def read_val_fromAgeExcel(filename, row, col):
    return pd.read_excel('ONSByAge2019.xls', skiprows= row-1, usecols=col, nrows=1, header=None, names=["Value"]).iloc[0]["Value"]


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
    avghouseholdage = avgAge(jsondata)
    #print(avghouseholdage)
    col2 = getcolAge(avghouseholdage)
    for j in range(len(colsAge)):
        cost_name = colsAge[j]
        row = rowsAge[j]
        column = col2
        val = str(read_val_fromAgeExcel('', row, column))
        val = val.replace("[", "")
        val = val.replace("]", "")
        values[cost_name] = values[cost_name] + float(val)
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

