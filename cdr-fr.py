# coding: utf-8

import numpy as np
import pandas as pd
import random
import csv
import uuid
import datetime
import os
import phoenixdb
import phoenixdb.cursor


database_url = "https://cod--1csdunit3mbci-gateway0.se-sandb.a465-9q4k.cloudera.site/cod--1csdunit3mbci/cdp-proxy-api/avatica/?serialization=PROTOBUF&authentication=BASIC"
#conn = phoenixdb.connect(database_url, autocommit=True, user='ledel', password='BadPass#1')

#cursor = conn.cursor()

#cursor.execute("SHOW TABLES")
#print(cursor.fetchall())


#session_id,calling_msisdn,called_msisdn,date_beg,date_end,duration,call_type,call_result,calling_net_type,radio_calling,cell_calling,lon_calling,lat_calling,called_net_type,radio_called,cell_called,lon_called,lat_called
#303c36b9-7fb2-4b4e-a352-0be40ead11d5,33757150547,33767150516,2022-08-15 16:08:25.223656,2022-08-15 16:11:07.223656,0,SMS,SUCCESS,21,GSM,10494,2.976922,50.216257,8,GSM,29403,2.453293,48.814949
#02c7a39b-95a5-4ff2-bd39-770847d0c090,33617150593,33747150531,2022-08-15 16:14:25.223656,2022-08-15 16:19:30.223656,0,SMS,FAILURE,10,GSM,20739,4.82456,45.27143,20,GSM,11056,2.9134368896483998,50.326309204102
#f591abd7-434b-42e9-a7f7-63f5e8f99aa3,33636150569,33760150597,2022-08-15 15:43:25.223656,2022-08-15 15:53:45.223656,0:10:20,Voice,SUCCESS,21,GSM,58227,6.415826,48.257754999999996,15,GSM,29308,7.204447,43.762039

#============================================================================================================

debug = 0
#============================================================================================================
# Read in the French area codes
#============================================================================================================
def get_area_codes():
    
    print("Getting area codes")

    f = open(os.getcwd() + "/fr_area_codes.csv", "r", encoding="utf-8-sig")

    csvfile = csv.reader(f)
    areacodes = []

    for x in csvfile:
        if (debug):
            print (x)
        areacodes.append(x[0])

    f.close()

    print("Number of area codes is", len(areacodes))

    return areacodes

#============================================================================================================
# Read in the country codes
#============================================================================================================
def get_country_codes():

    print("Getting country codes")

    f = open(os.getcwd() +"/country_codes.csv", "r", encoding="utf-8-sig")

    csvfile = csv.reader(f)
    countrycodes = []

    for x in csvfile:
        if (debug):
            print (x)
        countrycodes.append(x[0])

    f.close()
    
    print("Number of country codes is", len(countrycodes))

    return countrycodes



#============================================================================================================
# Small function that return TRUE with a specified probability
#============================================================================================================
def probability(p):
    
    # p is a percentage
    # Get a number between 1 and 200
    
    r = random.random() * 100
    
    if (r < p):
        rv = 1
    else:
        rv = 0
      
    return rv
#============================================================================================================
# Construct a French only MSISDN
# Calling country code is always 33
# Choose the first digit as 7 or something else - it should be a 7, 25% of the time.
# if 7 add the remaing 9 digits of the MSISDN 
# If not 7 then normall choose an area code () and occasionally make a 4 digit area code up
# then add a 6 digit number
#============================================================================================================

def get_fr_msisdn(areacodes):

    cc = '0033'
    ac = []

    if (probability(90)):
        ac = str(random.choice(['6', '7'])) 
       
      
    elif (probability(25)):
        ac =  areacodes[random.randint(0, len(areacodes)-1)]
        
    else:
        ac = str(random.choice([ '6', '7'])) 
    
    msisdn = cc + ac + str(random.randint(10, 99)) + '15' + '05'+str(random.randint(10, 99))
    net_type = str(random.choice(['1','2','8','9','10','15','20','21']))     
    return msisdn, net_type

# 
#============================================================================================================    
# Construct any MSISDN, international allowed but mostly UK
# 95% of the time return a UK MSISDN
# 5% of the time get a valid countro code followed by 10 digits
#============================================================================================================
def get_any_msisdn(areacodes, countrycodes):
    
    if (probability(96)):
        msisdn = get_fr_msisdn(areacodes)
    else:
        cc = countrycodes[random.randint(0, len(countrycodes)-1)]
        msisdn = '0'+ cc + str(random.randint(10000000, 99999999))
  
    return msisdn

  
  
def get_network_type():
    orange=[]
    free=[]
    sfr=[]
    bouygues=[]
    
    with open(os.getcwd() +"/fr_cell_id_location.csv",'r') as data:
      for line in csv.reader(data):
        array=np.array(line)
        if array[2]=='1'or array[2]=='2':
          orange.append(array)
        elif array[2]=='8' or array[2]=='9'or array[2]=='10' or array[2]=='11':
          sfr.append(array)
        elif array[2]=='15' :
          free.append(array)          
        else:
          bouygues.append(array)
        #list.append(array) 

      return orange,sfr,free,bouygues


#============================================================================================================
# Construct any MSISDN, international allowed but mostly DZ
# 95% of the time return a DZ MSISDN
# 5% of the time get a valid country code followed by 10 digits
#============================================================================================================
def get_cdr(areacodes, countrycodes, date,x,y,z,w):
    
    id = str(uuid.uuid4())
    
    
    #start = datetime.datetime.now()
    start=date
    end = start + datetime.timedelta(0,random.randint(1, 999))
    
    calling_msisdn , calling_net_type  = get_fr_msisdn(areacodes)
    called_msisdn , called_net_type  = get_fr_msisdn(areacodes)
    #get_any_msisdn(areacodes, countrycodes)

    
    if (probability(80)):
        call_type = 'Voice'
        #duration = end - start
        duration = int((end - start).total_seconds())
    else:
        call_type = 'SMS'
        duration = 0
    charge = str(   int(random.random() * 1000) / 100  )

    if (probability(80)):
        call_result = 'SUCCESS'
    else:
        call_result = 'FAILURE'
        duration = 0
        
    
    if calling_net_type == '1' or calling_net_type == '2' :
      
      array_calling=(random.choice(x))
      radio_calling=array_calling[0]
      mcc_calling=array_calling[1]
      net_calling=array_calling[2]
      cell_calling=array_calling[3]
      lon_calling=array_calling[4]
      lat_calling=array_calling[5]
      
    elif calling_net_type == '8' or calling_net_type == '9' or calling_net_type == '10':
      
      array_calling=(random.choice(y))
      radio_calling=array_calling[0]
      mcc_calling=array_calling[1]
      net_calling=array_calling[2]
      cell_calling=array_calling[3]
      lon_calling=array_calling[4]
      lat_calling=array_calling[5]
    
    elif calling_net_type == '15' :
      
      array_calling=(random.choice(z))
      radio_calling=array_calling[0]
      mcc_calling=array_calling[1]
      net_calling=array_calling[2]
      cell_calling=array_calling[3]
      lon_calling=array_calling[4]
      lat_calling=array_calling[5]

    else :
      array_calling=(random.choice(w))
      radio_calling=array_calling[0]
      mcc_calling=array_calling[1]
      net_calling=array_calling[2]
      cell_calling=array_calling[3]
      lon_calling=array_calling[4]
      lat_calling=array_calling[5]
    
    if called_net_type == '1' or called_net_type == '2':
      
      array_called=(random.choice(x))
      radio_called=array_called[0]
      mcc_called=array_called[1]
      net_called=array_called[2]
      cell_called=array_called[3]
      lon_called=array_called[4]
      lat_called=array_called[5]    
    
    elif called_net_type == '8' or called_net_type == '9' or called_net_type == '10':    
      array_called=(random.choice(y))
      radio_called=array_called[0]
      mcc_called=array_called[1]
      net_called=array_called[2]
      cell_called=array_called[3]
      lon_called=array_called[4]
      lat_called=array_called[5]   
      
    elif called_net_type == '15':
      array_called=(random.choice(z))
      radio_called=array_called[0]
      mcc_called=array_called[1]
      net_called=array_called[2]
      cell_called=array_called[3]
      lon_called=array_called[4]
      lat_called=array_called[5]  
    else :
      array_called=(random.choice(w))
      radio_called=array_called[0]
      mcc_called=array_called[1]
      net_called=array_called[2]
      cell_called=array_called[3]
      lon_called=array_called[4]
      lat_called=array_called[5]   
      
      
    #cdr = str(id) + ',' + calling_msisdn + ',' + called_msisdn + ','
    cdr = calling_msisdn + ',' + str(id) + ',' + called_msisdn + ','
    cdr = cdr + str(start) + ',' + str(end) + ',' + str(duration) + ','  + call_type + ','
    cdr = cdr + call_result + ','   
    cdr = cdr + calling_net_type + ',' + radio_calling + ',' + cell_calling + ',' + lon_calling + ',' + lat_calling + ',' 
    cdr = cdr + called_net_type +  ',' + radio_called + ',' + cell_called + ',' + lon_called + ',' + lat_called 
    
    return cdr

  
#============================================================================================================
# set batches to the required number
batches = 1

# set files_per_batch to the required number
files_per_batch = 24

# set records_per_file to the required number
records_per_file = 1000000

x,y,z,w = get_network_type()
# f = open("cdr.csv", "w")

areacodes = get_area_codes ()
countrycodes = get_country_codes()

#cell_id = get_cell_id ()
#print (cell_id)
#============================================================================================================
date = datetime.datetime.now ()
for b in range(batches):
   
    
    print(date)
    
    print ("Batch ", b)
    #for f in range(files_per_batch):
    filename = os.getcwd() +"/cdr/cdr-"+ str(date)+".csv" 
    filename = os.getcwd() +"/cdr/cdr-"+ date.strftime("%Y%m%d_%H%M%S") +".csv" 
    filename = os.getcwd() +"/cdr/cdr.csv"
        
    fh = open(filename, "w")

    for l in range(records_per_file):
            
            start= date + datetime.timedelta(minutes =random.randint(1,59))
            cdr = get_cdr(areacodes, countrycodes,start,x,y,z,w)
            fh.write(cdr + "\n")
        
    fh.close()
              
    cdrh =['session_id','calling_msisdn','called_msisdn', 'date_beg', 'date_end', 'duration','call_type', 'call_result', 'calling_net_type', 'radio_calling', 'cell_calling', 'lon_calling', 'lat_calling', 'called_net_type', 'radio_called', 'cell_called', 'lon_called', 'lat_called']
      
    print (filename)
    file = pd.read_csv(filename)
    #file.to_csv(filename, header=cdrh, index=False)
    file.to_csv(filename, index=False)
    date += datetime.timedelta(hours=1)
        
date2 = datetime.datetime.now()        
print(date2)
