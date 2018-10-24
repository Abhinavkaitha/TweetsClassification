
# coding: utf-8

# In[1]:


#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# 1 VocabuDic <-- all distinct words present in 32000 tweets
# 2 Calculated the required P(location) and P(word|location) 
#       n <-- total number of words in tweets from a particular location
#       for each word Wk in Vocabulary
#               nk <-- number of times a word occurs in a tweet from a particular place
#               P(Word|location) <-- (nk + 1)/(n + len(VocabDic))
# ---------------------------------------------------------------------------
import pandas as pd
import re
import numpy as np
from collections import Counter
import heapq


# In[2]:


#storing each line from train file in tweets train
tweetsTrain=[]
with open("tweets.train.clean.txt") as file:
    for line in file:
        tweetsTrain.append(line)


# In[3]:


# storing each line from test file in tweets test
tweetsTest=[]
with open("tweets.test1.clean.txt") as file:
    for line in file:
        tweetsTest.append(line)


# I have splitted each line with the first space
# 

# In[4]:


# splliting and separating the places and tweets for both test and train file
SplittweetsTrain=[]
for i in range(len(tweetsTrain)):
    SplittweetsTrain.append(tweetsTrain[i].split(" ",1))
SplittweetsTest=[]
for i in range(len(tweetsTest)):
    SplittweetsTest.append(tweetsTest[i].split(" ",1))


# created a separate list for places and tweets

# In[5]:


places=[]
tweets=[]
for i in SplittweetsTrain:
    places.append(i[0])
    tweets.append(i[1])


# In[6]:


Tplaces=[]
Ttweets=[]
for i in SplittweetsTest:
    Tplaces.append(i[0])
    Ttweets.append(i[1])


# In[7]:


#created dictionaries to store places and tweets
trainDic={}
trainDic["places"]=places
trainDic["tweets"]=tweets


# In[8]:


testDic={}
testDic["places"]=Tplaces
testDic["tweets"]=Ttweets


# Created a list of tweets by splitting them

# In[9]:


SplitTweets=[]
for i in trainDic["tweets"]:
    SplitTweets.append(i.split())


# In[10]:


TSplitTweets=[]
for i in testDic["tweets"]:
    TSplitTweets.append(i.split())


# List of stop words

# In[11]:


# I have collected  these stop words from NLTK package, https://www.ranks.nl/stopwords, from this website. I took the union of both of them
# and also I have found some words like job,jobs,careerarc,day, latest,amp,click which are in top 5 among all the places
#So, they wont play any major role in decision making. So I removed them
stop_words = ["click","amp",'latest', 'day',"careerarc","hiring","job","jobs",'enough',"im",'eg', 'thatll', 'something', 'often', 'nobody', 'more', 'seems', 're', 'therefore', 'until', 'well', 'wasnt', 'your', 'other', 'throughout', 'whereupon', 'thence', 'z', 'may', 'each', 'now', 'someone', 'become', 'between', 'amoungst', 'what', 'during', 'won', 'just', 'whereafter', 'another', 'go', 'out', 'beside', 'find', 'itself', 'x', 'shouldnt', 'few', 'hasnt', 'still', 'please', 'mightn', 'amount', 'shant', 'both', 'everything', 'themselves', 'youll', 'most', 'therein', 'hadnt', 'ltd', 'over', 'part', 'our', 'whoever', 'sometime', 'next', 'herself', 'r', 'becoming', 'whence', 'f', 'anything', 'g', 'afterwards', 'whatever', 'almost', 'cannot', 'b', 'thereafter', 'isnt', 'didnt', 'd', 'none', 'ourselves', 'so', 'her', 'herein', 'either', 'of', 'anywhere', 'have', 'need', 'and', 'up', 'at', 'amongst', 'she', 'whether', 'already', 'yours', 'wherein', 'mightnt', 'had', 'ma', 'many', 've', 'h', 'was', 'sometimes', 'where', 'except', 'everyone', 'meanwhile', 'y', 'off', 'n', 'havent', "should've", 'his', 'also', 'here', 'once', 'done', 'how', 'mine', 'seem', 'to', 'yourself', 'this', 'together', 'cant', 'above', 'does', 'through', 'ever', 'alone', 'w', 'others', 'in', 'these', 'thru', 'within', 'although', 'he', 'behind', 'us', 'even', 'such', 'there', 'll', 'it', 'than', 'whose', 'against', 'mustnt', 'moreover', 'beyond', 'somehow', 'for', 'couldnt', 'am', 'u', 'one', 'are', 'dont', 'you', 'sincere', 't', 'some', 'describe', 'my', 'since', 'de', 'has', 'without', 'could', 'further', 'before', 'ours', 'shan', 'wasn', 'mostly', 'myself', 'might', 'any', 'not', 'v', 'after', 'them', 'thus', 'wouldnt', 'everywhere', 'their', 'p', 'its', 'would', 'much', 's', 'somewhere', 'all', 'neither', 'then', 'be', 'or', 'own', 'take', 'but', 'too', 'anyway', 'else', 'same', 'whenever', 'while', 'if', 'yet', 'ain', 'did', 'having', 'anyhow', 'besides', 'made', 'nor', 'm', 'only', 'otherwise', 'seemed', 'among', 'that', 'whereas', 'which', 'a', 'however', 'across', 'those', 'less', 'though', 'because', 'wherever', 'i', 'about', 'being', 'rather', 'under', 'when', 'etc', 'four', 'nevertheless', 'the', 'thereby', 'with', 'below', 'c', "hasn't", 'thereupon', 'yourselves', 'him', 'do', 'youd', 'we', 'must', 'hers', 'get', 'perhaps', 'anyone', 'towards', 'doesnt', 'wont', 'always', 'found', 'hereupon', 'indeed', 'keep', 'noone', 'were', 'an', 'nowhere', 'from', 'every', 'nothing', 'no', 'onto', 'put', 'hereby', 'who', 'name', 'is', 'doing', 'k', 'youre', 'whereby', 'never', 'very', 'l', 'theirs', 'why', 'arent', 'again', 'becomes', 'give', 'himself', 'j', 'been', 'see', 'will', 'werent', 'e', 'they', 'youve', 'by', 'q', 'hence', 'on', 'o', 'neednt', 'seeming', 'along', 'can',"city" 'should', 'least', 'toward', 'upon', 'ie', 'into', 'became', 'hereafter', 'me', 'namely', 'down', 'whom', 'as']


# Removong the special charecters,punctuations and numbers

# In[12]:


newSplitTweets=[]
x=[]
for i in SplitTweets:
    for j in i:
        x.append(re.sub('[^a-zA-Z \n\.]', '', j))
    newSplitTweets.append(" ".join(x).lower())
    x=[]


# In[13]:


TnewSplitTweets=[]
x=[]
for i in TSplitTweets:
    for j in i:
        x.append(re.sub('[^a-zA-Z \n\.]', '', j))
    TnewSplitTweets.append(" ".join(x).lower())
    x=[]


# In[14]:


trainDic["clean"]=newSplitTweets


# In[15]:


testDic["clean"]=TnewSplitTweets


# Again, splitting the clean tweets to remove the stop words

# In[16]:


SplitTweets1=[]
for i in trainDic["clean"]:
    SplitTweets1.append(i.split())


# In[17]:


TSplitTweets1=[]
for i in testDic["clean"]:
    TSplitTweets1.append(i.split())


# Removing the stop words and adding them to dictionary

# In[18]:


newSplitTweets1=[]
x1=[]
for i in SplitTweets1:
    for j in i:
        if j not in stop_words:
            x1.append(j)
    newSplitTweets1.append(" ".join(x1))
    x1=[]


# In[19]:


TnewSplitTweets1=[]
x1=[]
for i in TSplitTweets1:
    for j in i:
        if j not in stop_words:
            x1.append(j)
    TnewSplitTweets1.append(" ".join(x1))
    x1=[]


# In[20]:


trainDic["clean1"]=newSplitTweets1


# In[21]:


testDic["clean1"]=TnewSplitTweets1


# creating a list of all the words present in the tweets

# In[22]:


vocab=[]
for i in trainDic["clean1"]:
    vocab.extend(i.split())


# Removing strings attachements like ".", "..." etc

# In[23]:


vocabulary=vocab
for i in range(len(vocabulary)):
    vocabulary[i]=vocabulary[i].replace(".","").replace(" ","")


# In[24]:


vocabDic={}
vocabDic=Counter(vocabulary)


# In[25]:


df=pd.DataFrame(trainDic)


# In[26]:


# this function returns a dictionaty with all the clean words and their count present in all the tweets from place
#similar to the previous operations
def WordCount(place):
    PlaceVocab=[]
    for i in df[df["places"]==place]["clean1"]:
        PlaceVocab.extend(i.split())
    PlaceVocabulary=PlaceVocab
    for i in range(len(PlaceVocabulary)):
        PlaceVocabulary[i]=PlaceVocabulary[i].replace(".","").replace(" ","")
    PlaceVocabDic={}
    PlaceVocabDic=Counter(PlaceVocabulary)
    del PlaceVocabDic[""]
    return PlaceVocabDic


# In[27]:


Places=set(df["places"])


# In[28]:


Tdf=pd.DataFrame(testDic)


# In[29]:


TPlaces=set(Tdf["places"])


# In[30]:


#this masterdic is a nested dictionay which consists of all the words present in all the places and their count
MasterDic={}
for i in Places:
    MasterDic[i]=WordCount(i)


# In[31]:


#This p dictionary will consists of p(word/location) for all the word in the vocabDic
#If a particulat word doesn't have this value then it is substitute with the least positive value
P={}
MasterP={}
for i in vocabDic:
    for j in Places:
        try:
            P[j]=(MasterDic[j][i]+1)/(sum(MasterDic[j].values())+len(vocabDic))
        except KeyError:
            P[j]=np.finfo(np.float64).eps
    MasterP[i]=P
    P={}


# In[32]:


#Calculated the p(location)
PlaceP={}
for i in Places:
    PlaceP[i]=(sum(df["places"]==i))/len(trainDic["places"])


# In[33]:


testDf=pd.DataFrame(testDic)


# In[34]:


for i in range(len(testDf)):
    testDf["clean1"][i]=" ".join(testDf["clean1"][i].split("."))


# In[35]:


#consists of all the clean words in each line of test file 
RowDic={}
for i in range(len(testDf)):
    RowDic[i]=testDf["clean1"][i].split()


# In[36]:


#Initiated a dictionary to store all p(location/word) i.e, probrability that a tweet is from a particular place
RowWordDic={}
xps={}
for i in RowDic:
    for p in Places:
        xps[p]=0
    RowWordDic[i]=xps
    xps={}


# In[37]:


#Calculated p(location/word) and multiplied them for a particular tweet
p=1
for j in range(len(RowDic)):
    for k in Places:
        for i in RowDic[j]:
            try:
                p=p*MasterP[i][k]
            except KeyError:
                continue
        RowWordDic[j][k]=p*PlaceP[k]
        p=1


# In[38]:


#Initiated a dictionary to store all the maximum probabilities from a place
Ans={}
for i in range(len(RowDic)):
    Ans[i]=0


# In[39]:


# took the maximum value from a particular tweet and stored it in qwe
#Then took the first value(in case if there are multiple maximum values)
qwe=[]
for i in range(len(RowWordDic)):
    for a,b in RowWordDic[i].items():
        if b==max(RowWordDic[i].values()):
            qwe.append(a)
    Ans[i]=qwe[0]
    qwe=[]


# In[40]:


with open("output.txt","w") as f:
    output=[]
    for i in range(len(tweetsTest)):
        tlist=tweetsTest[i].split()
        tlist.insert(0,Ans[i])
        output.append((" ".join(tlist)))
    f.writelines(["%s\n" % item  for item in output])
f.close()


# In[41]:


Jai=[]
for i in range(500):
    Jai.append(Ans[i]==Tplaces[i])
print(sum(Jai)/500)


# In[42]:


#Printing the top words from each place p(location/word)
top={}
test=[]
value=0
temp={}
for j in Places:
    for i in vocabDic:
        try:
            if MasterDic[j][i]!=1:
                value=MasterP[i][j]*PlaceP[j]
        except KeyError:
            continue
        temp[i]=value
    top[j]=temp
    temp={}


# In[43]:


#I DID NOT GET THE WORDS LIKE "click","amp",'latest', 'day',"careerarc","hiring","job","jobs",'enough',"im" BEACUSE I REMOVED
#THEM TO INCREASE THE EFFICIENCY
for i in Places:
    print(i)
    print(heapq.nlargest(5, top[i], key=top[i].get))

