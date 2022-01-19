#import necessary liberaries
import csv
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet


#path to the  dictionary csv file 
dict_path="MasterDictionary.csv"
#create path to the csv file containing only positive words
pos_dict_path="pos_dict.txt"
#create path to the csv file containing only negative words
neg_dict_path="neg_dict.txt"


#function provide valid POS tag to be used in lemmanizing the word
def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


#initialize a lemmatizer
lemmatizer = WordNetLemmatizer()

# open the dictionary csv file
dict=open(dict_path,'r',encoding='UTF8')
#read the dictionary file from the beginning
dict.seek(0)

#read the dictionary csv file
dict_reader=csv.reader(dict)

#print the heading values of the dictionary
header=next(dict_reader)

#containing positive words from the dictionary
pos_set=set()
##containing negative words from the dictionary
neg_set=set()

#iterate over each word in the dictionary 
#lemmanize the word 
#put in into  desired pos or neg set using positive and negative column.
for row in dict_reader:
   if row[8]!="0":
      word,pos=list(pos_tag([row[0].lower()])[0])
      pos_set.add(lemmatizer.lemmatize(word.lower(),get_wordnet_pos(pos)))
   elif row[7]!="0":
      word,pos=list(pos_tag([row[0].lower()])[0])
      neg_set.add(lemmatizer.lemmatize(word.lower(),get_wordnet_pos(pos)))
      

#create the file containing positive words
pos_dict=open(pos_dict_path,'w',encoding='UTF8')
pos_dict.seek(0)

#create the file containing negative words
neg_dict=open(neg_dict_path,'w',encoding='UTF8')
neg_dict.seek(0)



#put the words from positive set to positive words text file
for element in sorted(pos_set):
  pos_dict.write(element)
  pos_dict.write("\n")
  
#put the words from positive set to positive words dictionary  
for element in sorted(neg_set):
  neg_dict.write(element)
  neg_dict.write("\n")

#close all the files
pos_dict.close()
neg_dict.close()
dict.close()