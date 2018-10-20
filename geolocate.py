
# coding: utf-8

# # Twitter

# In[2]:


tweetsTrain=[]
with open("tweets.train.clean.txt") as file:
    for line in file:
        tweetsTrain.append(line)


# In[3]:


tweetsTest=[]
with open("tweets.test1.clean.txt",encoding="latin-1") as file:
    for line in file:
        tweetsTest.append(line)


# I have splitted each line with the first space
# 

# In[4]:


import pandas as pd
import re
import numpy as np
SplittweetsTrain=[]
for i in range(len(tweetsTrain)):
    SplittweetsTrain.append(tweetsTrain[i].split(" ",1))
SplittweetsTest=[]
for i in range(len(tweetsTest)):
    SplittweetsTest.append(tweetsTest[i].split(" ",1))


# created a separate list for places and tweets

# In[10]:


places=[]
tweets=[]
for i in SplittweetsTrain:
    places.append(i[0])
    tweets.append(i[1])


# In[11]:


Tplaces=[]
Ttweets=[]
for i in SplittweetsTest:
    Tplaces.append(i[0])
    Ttweets.append(i[1])


# In[74]:


trainDic={}
trainDic["places"]=places
trainDic["tweets"]=tweets


# In[79]:


testDic={}
testDic["places"]=Tplaces
testDic["tweets"]=Ttweets


# Created a list of tweets by splitting them

# In[81]:


SplitTweets=[]
for i in trainDic["tweets"]:
    SplitTweets.append(i.split())


# In[82]:


TSplitTweets=[]
for i in testDic["tweets"]:
    TSplitTweets.append(i.split())


# List of stop words

# In[83]:


stop_words = ['enough', 'eg', 'thatll', 'something', 'often', 'nobody', 'more', 'seems', 're', 'therefore', 'until', 'well', 'wasnt', 'your', 'other', 'throughout', 'whereupon', 'thence', 'z', 'may', 'each', 'now', 'someone', 'become', 'between', 'amoungst', 'what', 'during', 'won', 'just', 'whereafter', 'another', 'go', 'out', 'beside', 'find', 'itself', 'x', 'shouldnt', 'few', 'hasnt', 'still', 'please', 'mightn', 'amount', 'shant', 'both', 'everything', 'themselves', 'youll', 'most', 'therein', 'hadnt', 'ltd', 'over', 'part', 'our', 'whoever', 'sometime', 'next', 'herself', 'r', 'becoming', 'whence', 'f', 'anything', 'g', 'afterwards', 'whatever', 'almost', 'cannot', 'b', 'thereafter', 'isnt', 'didnt', 'd', 'none', 'ourselves', 'so', 'her', 'herein', 'either', 'of', 'anywhere', 'have', 'need', 'and', 'up', 'at', 'amongst', 'she', 'whether', 'already', 'yours', 'wherein', 'mightnt', 'had', 'ma', 'many', 've', 'h', 'was', 'sometimes', 'where', 'except', 'everyone', 'meanwhile', 'y', 'off', 'n', 'havent', "should've", 'his', 'also', 'here', 'once', 'done', 'how', 'mine', 'seem', 'to', 'yourself', 'this', 'together', 'cant', 'above', 'does', 'through', 'ever', 'alone', 'w', 'others', 'in', 'these', 'thru', 'within', 'although', 'he', 'behind', 'us', 'even', 'such', 'there', 'll', 'it', 'than', 'whose', 'against', 'mustnt', 'moreover', 'beyond', 'somehow', 'for', 'couldnt', 'am', 'u', 'one', 'are', 'dont', 'you', 'sincere', 't', 'some', 'describe', 'my', 'since', 'de', 'has', 'without', 'could', 'further', 'before', 'ours', 'shan', 'wasn', 'mostly', 'myself', 'might', 'any', 'not', 'v', 'after', 'them', 'thus', 'wouldnt', 'everywhere', 'their', 'p', 'its', 'would', 'much', 's', 'somewhere', 'all', 'neither', 'then', 'be', 'or', 'own', 'take', 'but', 'too', 'anyway', 'else', 'same', 'whenever', 'while', 'if', 'yet', 'ain', 'did', 'having', 'anyhow', 'besides', 'made', 'nor', 'm', 'only', 'otherwise', 'seemed', 'among', 'that', 'whereas', 'which', 'a', 'however', 'across', 'those', 'less', 'though', 'because', 'wherever', 'i', 'about', 'being', 'rather', 'under', 'when', 'etc', 'four', 'nevertheless', 'the', 'thereby', 'with', 'below', 'c', "hasn't", 'thereupon', 'yourselves', 'him', 'do', 'youd', 'we', 'must', 'hers', 'get', 'perhaps', 'anyone', 'towards', 'doesnt', 'wont', 'always', 'found', 'hereupon', 'indeed', 'keep', 'noone', 'were', 'an', 'nowhere', 'from', 'every', 'nothing', 'no', 'onto', 'put', 'hereby', 'who', 'name', 'is', 'doing', 'k', 'youre', 'whereby', 'never', 'very', 'l', 'theirs', 'why', 'arent', 'again', 'becomes', 'give', 'himself', 'j', 'been', 'see', 'will', 'werent', 'e', 'they', 'youve', 'by', 'q', 'hence', 'on', 'o', 'neednt', 'seeming', 'along', 'can',"city" 'should', 'least', 'toward', 'upon', 'ie', 'into', 'became', 'hereafter', 'me', 'namely', 'down', 'whom', 'as']


# Removong the special charecters and punctuations

# In[84]:


newSplitTweets=[]
x=[]
for i in SplitTweets:
    for j in i:
        x.append(re.sub('[^a-zA-Z \n\.]', '', j))
    newSplitTweets.append(" ".join(x).lower())
    x=[]


# In[85]:


TnewSplitTweets=[]
x=[]
for i in TSplitTweets:
    for j in i:
        x.append(re.sub('[^a-zA-Z \n\.]', '', j))
    TnewSplitTweets.append(" ".join(x).lower())
    x=[]


# In[86]:


trainDic["clean"]=newSplitTweets


# In[87]:


testDic["clean"]=TnewSplitTweets


# Again, splitting the clean tweets to remove the stop words

# In[88]:


SplitTweets1=[]
for i in trainDic["clean"]:
    SplitTweets1.append(i.split())


# In[89]:


TSplitTweets1=[]
for i in testDic["clean"]:
    TSplitTweets1.append(i.split())


# Removing the stop words and adding them to df

# In[90]:


newSplitTweets1=[]
x1=[]
for i in SplitTweets1:
    for j in i:
        if j not in stop_words:
            x1.append(j)
    newSplitTweets1.append(" ".join(x1))
    x1=[]


# In[91]:


TnewSplitTweets1=[]
x1=[]
for i in TSplitTweets1:
    for j in i:
        if j not in stop_words:
            x1.append(j)
    TnewSplitTweets1.append(" ".join(x1))
    x1=[]


# In[94]:


trainDic["clean1"]=newSplitTweets1


# In[95]:


testDic["clean1"]=TnewSplitTweets1


# creating a list of all the words present in the tweets

# In[96]:


vocab=""
for i in trainDic["clean1"]:
    vocab=vocab+" "+(" ".join(i.split()))


# In[97]:


Tvocab=""
for i in testDic["clean1"]:
    Tvocab=Tvocab+" "+(" ".join(i.split()))


# In[98]:


vocabulary=vocab.split()


# In[99]:


Tvocabulary=Tvocab.split()


# In[100]:


len(vocabulary)


# In[101]:


len(Tvocabulary)


# In[102]:


len(set(vocabulary))


# In[103]:


len(set(Tvocabulary))


# Removing strings attachements like ".", "..." etc

# In[104]:


j=""
for i in vocabulary:
    j=j+" "+(" ".join(i.split(".")))


# In[105]:


Tj=""
for i in Tvocabulary:
    Tj=Tj+" "+(" ".join(i.split(".")))


# Removing the extra spaces

# In[106]:


k=""
for i in j.split():
    k=k+" "+i


# In[107]:


Tk=""
for i in Tj.split():
    Tk=Tk+" "+i


# In[108]:


newVocabulary=k.split()


# In[109]:


TnewVocabulary=Tk.split()


# In[110]:


len(newVocabulary)


# In[111]:


len(TnewVocabulary)


# In[112]:


len(set(newVocabulary))


# In[113]:


len(set(TnewVocabulary))


# In[52]:


vocabDic={}
for x in set(newVocabulary):
    vocabDic[x]=newVocabulary.count(x)


# In[67]:


len(vocabDic)


# In[54]:


sum(vocabDic.values())


# In[148]:


def WordCount(place):
    PlaceVocab=""
    for i in df[df["places"]==place]["clean1"]:
        PlaceVocab=PlaceVocab+" "+(" ".join(i.split()))
    PlaceVocabulary=PlaceVocab.split()
    #Removing strings attachements like ".", "..." etc
    Placej=""
    for i in PlaceVocabulary:
        Placej=Placej+" "+(" ".join(i.split(".")))
    #Removing the extra spaces
    Placek=""
    for i in Placej.split():
        Placek=Placek+" "+i
    PlaceNewVocabulary=Placek.split()
    PlaceVocabDic={}
    for x in set(PlaceNewVocabulary):
        PlaceVocabDic[x]=PlaceNewVocabulary.count(x)
    return PlaceVocabDic


# {'Atlanta,_GA',
#  'Boston,_MA',
#  'Chicago,_IL',
#  'Houston,_TX',
#  'Los_Angeles,_CA',
#  'Manhattan,_NY',
#  'Orlando,_FL',
#  'Philadelphia,_PA',
#  'San_Diego,_CA',
#  'San_Francisco,_CA',
#  'Toronto,_Ontario',
#  'Washington,_DC'}

# In[149]:


Places=set(df["places"])


# In[295]:


TPlaces=set(Tdf["places"])


# In[151]:


MasterDic={}
for i in Places:
    MasterDic[i]=WordCount(i)


# In[152]:


TMasterDic={}
for i in TPLaces:
    TMasterDic[i]=WordCount(i)


# In[193]:


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


# In[250]:


MasterP


# In[204]:


PlaceP={}
for i in Places:
    PlaceP[i]=(sum(df["places"]==i))/len(trainDic["places"])


# In[205]:


PlaceP


# In[218]:


testDf=pd.DataFrame(testDic)


# In[256]:


testDf


# In[220]:


for i in range(len(testDf)):
    testDf["clean1"][i]=" ".join(testDf["clean1"][i].split("."))


# In[225]:


RowDic={}
for i in range(len(testDf)):
    RowDic[i]=testDf["clean1"][i].split()


# In[249]:


RowDic


# In[247]:


x={}
for i in range(len(RowDic)):
    for j in set(RowDic[i]):
        x.update({j:RowDic[i].count(j)})
    RowWordCount[i]=x
    x={}


# In[259]:


MasterP[]


# In[288]:


RowWordDic={}
xps={}
for i in RowDic:
    for p in Places:
        xps[p]=0
    RowWordDic[i]=xps
    xps={}


# In[289]:


p=1
for j in range(len(RowDic)):
    for k in Places:
        for i in RowDic[j]:
            try:
                p=p*MasterP[i][k]
            except KeyError:
                continue
        RowWordDic[j][k]=p
        p=1


# In[344]:


499*250


# In[350]:


max(RowWordDic[161].values())


# In[352]:


for i in range(len(RowDic)):
    Ans[i]=0
Ans


# In[355]:


qwe=[]
for i in range(len(RowWordDic)):
    for a,b in RowWordDic[i].items():
        if b==max(RowWordDic[i].values()):
            qwe.append(a)
    Ans[i]=qwe
    qwe=[]


# In[361]:


for i in range(500):
    if (len(Ans[i])>1):
        print(i)
        print(Ans[i])


# In[366]:


Jai=[]
for i in range(500):
    if i not in [161,243,317,347,367,391]:
        Jai.append(Ans[i][0]==Tplaces[i])
print(sum(Jai)/500)


# In[365]:


Ans[1][0]


# In[331]:


len(RowWordDic)


# In[329]:


Predict=[]
for i in range(len(RowWordDic)):
    for a,b in RowWordDic[i].items():
        if b==max(RowWordDic[i].values()):
            Predict.append(a)
    


# In[330]:


len(Predict)


# In[ ]:


for i in Predict:
    


# In[316]:


qwerty=[]
for p in Places:
    qwerty.append(RowWordDic[0][p])
max(qwerty)


# In[323]:


for a,b in RowWordDic[0].items():
    if b==4.7620745545409633e-32:
        print(a)


# In[305]:


Ans=[]
for i in range(len(RowWordDic)):
    for p in Places:
        max(RowWordDic[i][p])


# In[298]:


Predict


# In[265]:


Places


# In[190]:


A=["a","b","c"]
d={"la":{"a":2,"b":3},"ny":{"a":3,"b":10},"br":{"a":1,"c":10}}
pp=["la","ny","br"]
xx={}
yy={}
for i in A:
    for j in pp:
        a=0
        try:
            print(j)
            xx[j]=(d[j][i]+1)/(sum(d[j].values())+len(A))
            print(xx)
        except KeyError:
            xx[j]=np.finfo(np.float64).eps
    yy[i]=xx
    xx={}


# In[191]:


yy


# In[172]:


4/16


# In[199]:


sum(df["places"]=="Los_Angeles,_CA")


# In[203]:


len(trainDic["places"])

