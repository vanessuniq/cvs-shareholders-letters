# DATA 620 Assignment 12.1 Text-anaalysis
# Written by Vanessa Fotso
# Last Updated April 23, 2020

"""
We will be performing a text analysis of CVS Health CEO's letters to shareholders from 2010 to 2019.
The letters are in pdf format and could be downloaded from the CVS Health investors website:
https://investors.cvshealth.com/investors/financial-information/annual-reports-archive/default.aspx
I first converted each year letter into a text input files for this analyses. We have a total of ten
text files for this analysis.
we will build a program that give a word count of all the words in a text file, generate the total number
of words  and the top 30 mostly used words after excluding the commonly used 'stop words' and punctuations, stemming the words, and performing sentiment analysis.
We will use the nltk module to exclude those stopwords, stemming words and analyzing sentiment in our files. I already have the module installed on my computer.
For installation:
1) go to docs.anaconda.com
2) download the Anaconda installer
3) after downloading Anaconda, run the following in your terminal: 'pip install nltk'

Note: if you already have anaconda installed, you can simply run 'pip install nltk' in your terminal to install nltk module.

To remove punctuations, we will use the python regular expression package (re) and string. These libraries have been part of the standard download of python.
To use re and string, we just need to import them (e.g. import re)

Finally we will output our list of words and count using pandas library DataFrame. To install pandas, run the following in your terminal:
pip3 install pandas

Attention: When running the this code, make sure to download the dependent text files and save it in the same directory as this python file.

"""
# Getting our dependencies

# We will first import the nltk module and dowload stopwords the list of stop words. we will use this module to remove stop word from our list of words.

import nltk
nltk.download('stopwords')     # this will download a file with multilanguage stopwords
nltk.download('vader_lexicon') # will use this for sentiment analysis

#now let's import pandas, stopwords and re
import pandas as pd
import re
import string
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer  # for word stemming
from nltk.sentiment.vader import SentimentIntensityAnalyzer  #for sentiment analysis

#================================================================================================================================================================

# defining a function that removes punctuation & digits and converts all the text to lower case as we do not need to preserve text structure
# or capitaliztions for this analysis. we will use the re module here

def clean_text(letter):
    #remove all punctuations and digits (except for hyphens) if any
    punctuations = string.punctuation
    punctuations = punctuations.replace("-", "")
    clean1 = re.sub(r'['+punctuations + string.digits +']', "", letter.lower())
    return re.sub(r'\W+', ' ', clean1)

# Define a function that will accomplish the program task:

def top30_csv(file):
    # initialize a dictionary that will collect all unique words from a file plus their counts.
    words_count = dict()
    global y
    #use try/catch exception handling to check if the user entered an existing file. If the input does not exist, raise error and exit gracefully
    try:
        # open and read the file
        letter = open(file, 'r').read()
    except:
        print('There\'s no such file:', file, 'in the directory, make sure to add the files to your directory.')
        exit()

    # read letter and uncapitalize texts and remove punctuations using the predefined 'clean_text' function:
    clean_letter = clean_text(letter)
    
    # split the letter into a list of words using the split method, saving the words into words_list variable
    words_list = clean_letter.split()

    # perform stemming of the words 
    stemmer = SnowballStemmer('english')
    stem_list = [stemmer.stem(word) for word in words_list]

    # create a sentiment analyzer for basic sentiment text. We will save the sentiment score in a dict that we will use later
    sentiment_score = dict()
    sentiment = SentimentIntensityAnalyzer()
    for w in stem_list:
        score = sentiment.polarity_scores(w)        # this will output the scores in a dictionary in the form {'neg':0.0, 'neu': 0.344, 'pos':0.2, 'compound': 0.54}
        # I am only intersted in the compound value
        compound_score = score['compound']
        sentiment_score[w] = compound_score
        
    # iterate over words in words_list using for..in loop
    for w in stem_list:
        # use the get method to add each unique word of words_list as a key to the words_count dictionary defined above and counts its frequency
        words_count[w] = words_count.get(w, 0) + 1

   # remove stop words from the dict:
    # we will add 'also' to the list of stopwords from the stopword library as it is repetitive in the letters
    sw = stopwords.words('english')
    sw.append('also')
    for w in sw:
        if w in words_count:                             #firtst check if the word is a key of the dict
            del(words_count[w])           
    
    # use pandas to convert our dictionary words_count into a DataFrame. For that, we will use list() function and items() dictionary method
    # to convert the dictionary into a list of (key, value) tuple pairs

    df = pd.DataFrame(list(words_count.items()), columns = ['Words', 'Count'])

    # same task for creating a dataframe for sentiment
    dfs = pd.DataFrame(list(sentiment_score.items()), columns = ['Words', 'Sentiment Score'])

    # Add a year column to both data frames
    df['Year'] = [y]*len(df)
    dfs['Year'] = [y]*len(dfs)

    # save all sentiment data frames in sentiment_dataframes list
    sentiment_dataframes.append(dfs)

    # order the data frame by count in descending order:
    df = df.sort_values('Count', ascending=False)

    # customize the data frame index
    df.index = range(1, len(df)+ 1)

    #calculate the total number of unique words in the letter and add it to the num_uniq_words array:
    num_words = sum(df['Count'])
    num_uniq_words.append(num_words)
    print("The total number of unique words in this letter is: ", num_words)
    # output the top 30 words
    print("This is the top 30 words used:")
    print(df.head(30))

    #save data frame to letters_list list
    letters_list.append(df.head(30))
    
#================================================================================================================================================================

# run the program:
# initialize variables:
letters_list = []           # to collect the data frames of word count from each letter
sentiment_dataframes = []   # to collect the data frames of sentiment score from words in each letter
num_uniq_words = []      # collect the total number of words in each letter

y = 2010  # this is a counter to create the year column
text_files = ["2010-letter.txt","2011-letter.txt", "2012-letter.txt", "2013-letter.txt", "2014-letter.txt", "2015-letter.txt",
              "2016-letter.txt", "2017-letter.txt", "2018-letter.txt", "2019-letter.txt"]
#===============================================================================================================================================================

# iterate through text files and generate csv files by calling top30_csv function
for file in text_files:
    top30_csv(file)
    y += 1

# combine all the letters data frames into one data frame using concat method and export it as a csv file
letters_df = pd.concat(letters_list)
print('This is the final data set of words for all letters')
print(letters_df)
letters_df.to_csv("combine_letters.csv", index = False)


# create one csv file for sentiment analysis
df1 = pd.concat(sentiment_dataframes)
print('This is the sentiment data frame')
print(df1)
df1.to_csv("words_sentiment_scores.csv", index = False)
            
        
 
    
