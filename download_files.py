from email import charset
from encodings import utf_8
import os
import random
import time
import requests
import numpy as np
import csv

#path to the master files folder in which year/quarter combination of master.idx files to be downloaded
master_path="master_files"

#path to the fillings file foder which cotains year/quarter combination of random 10 8K txt files in each of them
fillings_path="fillings"

#path to the CSVs file folder which contains year/quarter combination of each csv file contains CIK vs date
csv_path="CSVs"


# List of years to be searched in the full index folder of the website
years = [1995 + x for x in range(0,27)]

# List of quarters to be searched in each year folder of the website
quarters = ['QTR1', 'QTR2', 'QTR3', 'QTR4']


# loop for each year/quarter combination,to  get the corresponding
# master.idx file   and save it to our local machine  as a text file.
for yr in years:
      #if files already created
      if  os.path.exists('/'.join([master_path, str(yr)])):
        continue
        #iterate for each quarter
      for qtr in quarters:
        #  to store the index files locally.
           base_file_path =  f'master-index-{yr}-{qtr}.txt'
          
        # get the absolute file path to the empty text file(on which master.idx content to be downloaded)we created locally on our pc   
           absolute_file_path='/'.join([master_path, str(yr),base_file_path])
           
        # Define the url of the master.idx file to be downloaded
           url = f'https://www.sec.gov/Archives/edgar/full-index/{yr}/{qtr}/master.idx'
        
           heads = {'Host': 'www.sec.gov', 'Connection': 'close',
         'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest',
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
           }
         
          #get the content of the file using request library
           response = requests.get(url, headers=heads)
           
          #create the  folder before creating file in it 
           if not os.path.exists('/'.join([master_path, str(yr)])):
             os.makedirs('/'.join([master_path, str(yr)]))
        # Get the corrosponding master.idx file from the website and save it to a corrosponding empty text file.
          
           f=open(absolute_file_path, 'w+b')
           f.write(response.content)
           #to reach the begining of the file text
           f.seek(0) 
         #get the lines of the downloaded master.idx file to filter the fillings which are not 8-K.  
           lines=f.readlines()
           f.close()
          # Cloud http path i.e "https://www.sec.gov/Archives/"
           cloud_http_path="https://www.sec.gov/Archives"
            
           #only keep the fillings which are 8-Ks
           f=open(absolute_file_path, 'w+b')
           f.seek(0)
           for line in lines:
              if b"|8-K|" in line:
                f.write(line)   
           f.seek(0)     
           modified_lines=f.readlines()
           f.close()  
           
           #create the  folder before creating file in it
           if not os.path.exists('/'.join([csv_path,str(yr),str(qtr)])):
             os.makedirs('/'.join([csv_path,str(yr),str(qtr)]))
           
           #open the csv file
           CSV_file=open('/'.join([csv_path,str(yr),str(qtr),'companies_identifier_vs_date.csv']), 'w', encoding='UTF8')
            
            #get a write object to write on csv file
           writer = csv.writer(CSV_file) 
            
            #write the heading of the csv file
           heading=["CIK","date"]   
           writer.writerow(heading)
            
            #get random 10 lines of the filtered master.idx(contains only 8-K fillings)
           random_10_lines=random.sample(modified_lines,10)
            
            #loop over each line of the random_10_lines
           for i,line in enumerate(random_10_lines): 
           
            #split the line in to list elements where it encounters '|'
             line.strip()
             elements = line.split(b"|") 
             
            #get the absolute path of the 8k file 
             filling_absolute_path='/'.join([cloud_http_path,elements[4].decode()])
      
             #download the content to filling absolute path of our local machine  
             response = requests.get(filling_absolute_path, headers=heads)
             
             #let the random 8k file name be like 1.txt 2.txt etc...
             base_name=f'{i}.txt'
             
             #create the  folder before creating a file in it
             if not os.path.exists('/'.join([fillings_path,str(yr),str(qtr)])):
               os.makedirs('/'.join([fillings_path,str(yr),str(qtr)]))
               
             #open the file
             f=open('/'.join([fillings_path,str(yr),str(qtr),base_name]), 'w+b')
             
             #writer the corrosponding 8k file's content to it
             f.write(response.content)
            
             #also write the CIK and date of each 8-k filling
             writer.writerow([elements[0].decode(),elements[3].decode()])
           CSV_file.close()
        # Wait one-tenth of a second before sending another request to EDGAR.
           time.sleep(0.1)
           
        