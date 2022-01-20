#import liberaries
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import filter_pos_neg as f2                    
from nltk.corpus import wordnet
import matplotlib.pyplot as plt
import csv
import os
import statistics
import download_files as f1

#initialize a lemmatizer
lemmatizer = WordNetLemmatizer()

#set indices to iterate over subplots of pyplot
pyplot_ind=[[0,0],[0,1],[1,0],[1,1]]

#figures folder to save all the pyplots in it.
figures_path="figures"

#sentimental_score=(pos-neg)/(pos+neg)

# Y axis points list  in  average_sentimental_score vs year
avg_y=[]

#iterate over years 1995 to 2021
for yr in f1.years:
      
      yearly_y=[]  
      
      #initializing fig1 and axes1 to plot 4 graph containing average_sentimental_score vs quarter in each year
      fig1, axes1 = plt.subplots(2,2,figsize=(20,20)) 
      
      #iterate over each 4 quarters  of each year
      for k,qtr in enumerate(f1.quarters):
      
      # Y axis points list  in  average_sentimental_score of filling vs filling date(dates in ascending order) in each quarter
        quatorly_y=[]
        
       #iterate over the 8k fillings(which we randomly downloaded before) 
        for i in range(10):
        
          # random 8k file were in the format 1.txt 2.txt etc...
          base_name=f'{i}.txt'   
          
           #open the 8-k file to read 
          f=open('/'.join([f1.fillings_path,str(yr),str(qtr),base_name]), 'r+')
          
          #extract only text of the 8-k filling(filtering tags in it)(clean the file data)
          Ctext = BeautifulSoup(f, features="lxml").get_text()
      
          #rewrite the clean text on the file
          f.write(Ctext)
          f.close()  
            
          #convert the extracted text to lowercase
          Ctext=Ctext.lower()
          
          #initialize a tokenizer to get only words containing only alphabatical charactors
          tokenizer = RegexpTokenizer(r'[a-z]+')
          tokens = tokenizer.tokenize(Ctext)
        
          #remove stopwords from the list of words
          filtered_tokens= [token for token in tokens if not token in stopwords.words('english')]
          
          #lemmatize the list of words
          lem_tokens=[]
          for token in filtered_tokens:
            word,pos=list(pos_tag([token])[0])
            lem_tokens.append(lemmatizer.lemmatize(word,f2.get_wordnet_pos(pos)))
             
          #get the no. of positive and negative words in the text
          pos=neg=0  
          for token in lem_tokens:
            if token in sorted(f2.pos_set):
              pos=pos+1
            elif token in sorted(f2.neg_set):
              neg=neg+1
              
          #normalized diff= sentimental_score((pos-neg)/(pos+neg))  of each corrosponding 8-k filling
          if (pos+neg)==0:
            normalized_diff=0
          else:  
            normalized_diff=(pos-neg)/(pos+neg)
            
           #append the sentimental scores to the quaterly_y list
          quatorly_y.append(normalized_diff)
          
        #get the quaterly_x
        #read this csv file to get the 10 8-k filling dates which (we saved before only) to plot a graph
        file_csv=open('/'.join([f1.csv_path,str(yr),str(qtr),'companies_identifier_vs_date.csv']), 'r', encoding='UTF8')
        reader=csv.reader(file_csv)
        header=next(reader)
        quatorly_x=[]
        for row in reader:
          if row!=[]:
           quatorly_x.append(row[1])
           
        #close the csv file   
        file_csv.close()    
        
        
        
        #if path to the file does not exist   
        if not os.path.exists('/'.join([figures_path,str(yr)])):      
         #sort the quaterly_y(sentimental_scores) in the same order when we sort quaterly_x(filling dates)  to preserve the key value pair
          quoterly_y=[x for _, x in sorted(zip(quatorly_x,quatorly_y))]
          quatorly_x=sorted(quatorly_x) 
        #subplot a graph of sentimental_score vs quarter in each year
          axes1[pyplot_ind[k][0],pyplot_ind[k][1]].set_title(qtr, fontsize=14) 
          axes1[pyplot_ind[k][0],pyplot_ind[k][1]].set_xlabel('date', fontsize=10)
          axes1[pyplot_ind[k][0],pyplot_ind[k][1]].set_ylabel('good_sentiment score', fontsize=10)
          axes1[pyplot_ind[k][0],pyplot_ind[k][1]].plot(quatorly_x,quatorly_y)  
          axes1[pyplot_ind[k][0],pyplot_ind[k][1]].set_xticklabels(quatorly_x,rotation=90)
      
         #now append the mean of the quaterly_y list to the yearly_y list
        yearly_y.append(statistics.mean(quatorly_y)) 
      
      #if path to the file does not exist   
      if not os.path.exists('/'.join([figures_path,str(yr)])):  
      #create a path (for ex: "figures/1995") and save the figure (plot of sentimental_score of 4 quarters in 1 figure) there
        os.makedirs('/'.join([figures_path,str(yr)]))  
        fig1.savefig('/'.join([figures_path,str(yr),'plot.png']))   
        plt.close()
            
    #append the mean of the yearly_y list to the avg_y list
      avg_y.append(statistics.mean(yearly_y))   
 

 #plot a graph of sentimental_score vs year 
fig, axes = plt.subplots(1,1) 
axes[0,0].set_title("yearwise distribution of sentiment score", fontsize=18)
axes[0,0].set_xlabel('year', fontsize=18)
axes[0,0].set_ylabel('good_sentiment score', fontsize=18)
axes[0,0].plot(f1.years,avg_y)  
plt.xticks(rotation=90)  
fig.savefig('figures/year_vs_sentiment_score_plot.png')
plt.close()
