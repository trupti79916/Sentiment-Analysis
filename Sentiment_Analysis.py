#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import nltk


# In[2]:


df = pd.read_excel(r'C:\Users\hp\OneDrive\Desktop\ML\Input.xlsx')


# In[3]:


df


# In[4]:


scores = {"URL_ID": [],"URL": [], "POSITIVE SCORE": [], "NEGATIVE SCORE": [],"POLARITY SCORE": [],"SUBJECTIVITY SCORE": [],"AVG SENTENCE LENGTH":[],"PERCENTAGE OF COMPLEX WORDS":[],"FOG INDEX":[],"AVG NUMBER OF WORDS PER SENTENCE":[],"COMPLEX WORD COUNT":[],"WORD COUNT":[],"SYLLABLE PER WORD":[],"PERSONAL PRONOUNS":[],"AVG WORD LENGTH":[]}


# In[5]:


#Function to remove punctuations
import string
import re

def remove_punctuations(paragraph):
    # Remove punctuation marks using string.punctuation
    no_punctuations = paragraph.translate(str.maketrans('', '', string.punctuation))

    # Alternatively, remove punctuation marks using regex
    # no_punctuations = re.sub(r'[^\w\s]', '', paragraph)
    

    return no_punctuations


# In[6]:


#Find number of stopwords, positive,negative,polarity and subjectivity scores
def stopw(article_text):
    
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    with open(article_text, 'r',encoding="utf-8") as file:
        text = file.read()

    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stopwords.words('english')]
    #Filtered text without stop words
    filtered_text = ' '.join(filtered_words)
    blob = TextBlob(filtered_text)
    #Calculating polarity, subjectivity score using textblob
    polarity = blob.sentiment.polarity
    scores["POLARITY SCORE"].append(polarity)
    subjectivity = blob.sentiment.subjectivity
    scores["SUBJECTIVITY SCORE"].append(subjectivity)
    #Positive and negative score 
    pos_count = len([w for w in blob.words if TextBlob(w).sentiment.polarity > 0])
    neg_count = len([w for w in blob.words if TextBlob(w).sentiment.polarity < 0])
    #saving the scores to the dictionary
    scores["POSITIVE SCORE"].append(pos_count)
    scores["NEGATIVE SCORE"].append(neg_count)
    #Calling remove punctuations function 
    punc_less = remove_punctuations(filtered_text)
    words = word_tokenize(text.lower())
    #finding the total number of words without stopwords and punctuations
    num_words = len(words)
    
    scores["WORD COUNT"].append(num_words)



# In[7]:


import re
import string
import syllables
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

def get_stats(filename):
    with open(filename, 'r',encoding = 'utf-8') as f:
        text = f.read()

    #Calculating average sentence length
    sentences = re.split('[.?!]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    total_words = sum(len(s.split()) for s in sentences)
    # Calculate the average sentence length
    avg_sentence_length = total_words / len(sentences)
    
    
    # Percentage of complex words
    words = word_tokenize(text.lower())
    num_complex_words = 0
    for word in words:
        if len(word) > 2 and syllables.estimate(word) > 2:
            num_complex_words += 1
    pct_complex_words = num_complex_words / len(words)
    pct_complex_words = pct_complex_words*100

    # FOG index
    fog_index = 0.4 * (avg_sentence_length + pct_complex_words * 100)

    # Average number of words per sentence
    avg_num_words = len(words) / len(sentences)

    # Complex word count
    complex_words = [word for word in words if len(word) > 2 and syllables.estimate(word) > 2]
    num_complex = len(complex_words)


    # Syllables per word
    num_syllables = sum(syllables.estimate(word) for word in words)
    syllables_per_word = num_syllables / len(words)

    # Personal pronouns
    personal_pronouns = ['i','my', 'mine','we', 'us', 'ours']
    num_personal_pronouns = sum(1 for word in words if word.lower() in personal_pronouns)

    # Average word length
    avg_word_len = sum(len(word) for word in words) / len(words)

    # Saving results to dictionary
    scores["AVG SENTENCE LENGTH"].append(avg_sentence_length)
    scores["PERCENTAGE OF COMPLEX WORDS"].append(pct_complex_words)
    scores["FOG INDEX"].append(fog_index)
    scores["AVG NUMBER OF WORDS PER SENTENCE"].append(avg_num_words)
    scores["COMPLEX WORD COUNT"].append(num_complex)
    scores["SYLLABLE PER WORD"].append(syllables_per_word)
    scores["PERSONAL PRONOUNS"].append(num_personal_pronouns)
    scores["AVG WORD LENGTH"].append(avg_word_len)
    



# In[8]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob import TextBlob
import nltk
#Extracting each article and saving them in a file with the url id, skipping the urls with no information
# Loop through each row of the DataFrame
for index, row in df.iterrows():
    url = row['URL']
    url_id = row['URL_ID']
    # Retrieve the HTML content of the article URL
    response = requests.get(url)
    html_content = response.text
    if response.status_code != 200:
        print(f"Failed to get {url}")
        continue
        
    scores["URL_ID"].append(url_id)
    scores["URL"].append(url)
    
    # Use Beautiful Soup to parse the HTML content and extract the article text
    soup = BeautifulSoup(html_content, 'html.parser')
    article_title = soup.find('h1').text
    article_text = ''
    for p in soup.find_all('p'):
        article_text += p.text
    # Save the article text in a text file with the URL_ID as its file name
    with open(f'{url_id}.txt', 'w',encoding="utf-8") as f:
        f.write(f'{article_title}\n\n{article_text}')
    filename = f'{url_id}.txt'
    #Finding all the scores by calling the functions
    get_stats(filename)
        
    stopw(filename)


# In[9]:


#Output dataframe
output = pd.DataFrame(scores)


# In[10]:


#Saving the result in an excel sheet
datatoexcel = pd.ExcelWriter(r'C:\Users\hp\OneDrive\Desktop\ML\Output.xlsx')
  
# write DataFrame to excel
output.to_excel(datatoexcel)
  
# save the excel
datatoexcel.save()
print('DataFrame is written to Excel File successfully.')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




