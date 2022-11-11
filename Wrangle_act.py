#!/usr/bin/env python
# coding: utf-8

# ## Project: Wrangling and Analyze Data

# ## Data Gathering
# 
# In this section all three pieces of data required for this project will be gathered in the notebook

# 1. Manually download the WeRateDogs Twitter archive data

# In[91]:


import tweepy
from tweepy import OAuthHandler
import json
from timeit import default_timer as timer
import pandas as pd
import numpy as np
import requests
import os
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
from matplotlib import pyplot as plt
sns.set_style('darkgrid')
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import os


# Import CSV data from file

# In[14]:


df_twitter_arch = pd.read_csv('twitter-archive-enhanced.csv')
df_1 = df_twitter_arch
df_1.head()


# 2. Get second data (image_prediction) using URL provided

# In[15]:


url = 'https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'
response = requests.get(url)
response


# In[16]:


url.split('/')[-1]
with open (os.path.join(url.split('/')[-1]), mode='wb') as file:
    file.write(response.content)


# In[17]:


response.content


# Import tsv file into dataframe

# In[18]:


df_image_perd = pd.read_csv('image-predictions.tsv', sep ='\t')
df_2 = df_image_perd
df_2.head()


# 3. Query Twitter API for each tweet in the Twitter archive using Python's Tweepy library and save as JSON in a text file

# In[19]:


# These are hidden to comply with Twitter's API terms and conditions
consumer_key = 'Hidden'
consumer_secret = 'Hidden'
access_token = 'Hidden'
access_secret = 'Hiddens'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)


# In[20]:


tweet_ids = df_1.tweet_id.values
len(tweet_ids)


# In[11]:


count = 0
fails_dict = {}
start = timer()
count = 0
fails_dict = {}
start = timer()
# Save each tweet's returned JSON as a new line in a .txt file
with open('tweet_json.txt', 'w') as outfile:
    # This loop will likely take 20-30 minutes to run because of Twitter's rate limit
    for tweet_id in tweet_ids:
        count += 1
        print(str(count) + ": " + str(tweet_id))
        try:
            tweet = api.get_status(tweet_id, tweet_mode='extended')
            print("Success")
            json.dump(tweet._json, outfile)
            outfile.write('\n')
        except tweepy.TweepError as e:
            print("Fail")
            fails_dict[tweet_id] = e
            pass
end = timer()
print(end - start)
print(fails_dict)


# In[21]:


df_list = []
with open('tweet_json.txt', 'r') as file:
    for line in file:
        data = json.loads(line)
        tweets = {'tweet_id': data['id'],
                 'retweet_count': data['retweet_count'],
                 'favorite_count': data['favorite_count']}
        df_list.append(tweets)

df_3 = pd.DataFrame(df_list, columns = ['tweet_id', 'retweet_count', 'favorite_count'])


# In[22]:


df_3.head()


# ## Data Assessment
# 
# In this section, visual and programatic assessment will be carried out for quality and tidiness issues

#  - Investigate the first data frame (df_1)

# In[23]:


#Visually assess data
df_1


# #####    Quality Issues
# 
# - Missing in_reply_to_status_id and in_reply_to_user_id
# - Null values in the expanded url
# - Repitition of expanded url in some rows
# - Dog names like a
# - Tweet_ids with value in the retweeted_status_id, retweeted_status_user_id and retweeted_status_timestamp 
# - Retweet columns
# - tweet_id is a string not an int
# - Time_stamp column is a datetime data type.

# In[24]:


# Programmatically assess data 
df_1.info()
df_1.shape


# In[25]:


# Checking statistical description of the data frame
df_1.describe()


# In[26]:


# Checking for null values in the data frame
df_1.isnull().sum()


# In[27]:


# Checking for duplicate values
df_1.duplicated().sum()


#  - Investigate the second data frame (df_2)

# In[28]:


# Visual Assessment 
df_2


# In[29]:


# Programmatic Assessment 
df_2.info()
df_2.shape


# ##### Quality Issues
# 
# - tweet_id is a string not an int
# - Inconsistent letter case for values in P1, P2 and P3
# - Convert p1_conf, p2_conf, p3_conf columns to percentage

# In[30]:


# Checking statistical description of the data frame
df_2.describe()


# In[31]:


# Checking for null Values in df_2
df_2.isnull().sum()


# In[32]:


# Checking for duplicate 
df_2.duplicated().sum()


# - Investigate the third data_frame

# In[33]:


# Visually assess data
df_3


# In[34]:


# Programmatically assess the data frame
df_3.info()
df_3.shape


# ##### Quality Issues
# 
# - tweet_id is a string not an int

# In[35]:


# Checking statistical description of the data frame
df_3.describe()


# In[36]:


# Checking for null Values in df_3
df_3.isnull().sum()


# In[37]:


# Checking for duplicate Values in df_3
df_3.duplicated().sum()


# ##### Quality and Tidiness Issues observed from assessing the data
# 
# Quality
# 
# - Tweet_id in the three data frame is a string not an int
# - Missing values in the (in_reply_to_status_id and in_reply_to_user_id) column
# - Null values in the expanded url and repitition of url in some rows
# - Tweet_ids with value in the retweeted_status_id, retweeted_status_user_id and retweeted_status_timestamp 
# - Time_stamp column is a datetime data type.
# - Retweet columns
# - Inconsistent letter case for values in P1, P2 and P3
# - Convert p1_conf, p2_conf, p3_conf columns to percentage
# 
# Tidiness
# - Dog stages in different columns should be melted into a single column.
# - The three data set to be merged into a single data set

# ## Data Cleaning 
# 
# In this section, all issues identified while assessing data will be cleaned and tidied up

# ##### Creating Copies of the data frames
# 
# The first step in the data cleaning section is to make a copy of each piece of data. All the cleaning process will be conducted on the copies created so one can still view the original dirty and/or messy dataset later

# In[38]:


# Create copies of the original data frames
df_1_copy = df_1.copy()
df_2_copy = df_2.copy()
df_3_copy = df_3.copy()


# ### Cleaning Quality Issues

# ###### a) Tweet_id in the three data frame is a string not an int

# ### Define
# 
# Convert the tweet_id column's data type from an int to a string using astype

# ### Code

# In[39]:


# convert data type from int to str
df_1_copy.tweet_id = df_1_copy.tweet_id.astype(str)
df_2_copy.tweet_id = df_2_copy.tweet_id.astype(str)
df_3_copy.tweet_id = df_3_copy.tweet_id.astype(str)


# ### Test

# In[40]:


df_1_copy.tweet_id.head(), df_2_copy.tweet_id.head(), df_3_copy.tweet_id.head()


# ###### b) Missing values in the (in_reply_to_status_id and in_reply_to_user_id) column

# ### Define
# 
# Drop columns in_reply_to_status_id and in_reply_to_user_id as they are not relevent to the analysis

# ### Code

# In[41]:


df_1_copy.drop(columns = ['in_reply_to_status_id', 'in_reply_to_user_id'], axis =1, inplace =True)


# ### Test

# In[42]:


df_1_copy.columns


# ###### c) Null values in the expanded url and repitition of url in some rows

# ### Define
# 
# Drop expanded url columns

# ### Code

# In[43]:


df_1_copy.drop(columns = ['expanded_urls'], axis=1, inplace = True)


# ### Test

# In[44]:


df_1_copy.columns


# ###### d) Tweet_ids with value in the retweeted_status_id, retweeted_status_user_id and retweeted_status_timestamp

# ### Define
# 
# Drop rows with value in the retweet columns

# ### Code

# In[45]:


df_1_copy = df_1_copy[df_1_copy.retweeted_status_id.isnull()]


# In[46]:


df_1_copy = df_1_copy[df_1_copy.retweeted_status_user_id.isnull()]


# In[47]:


df_1_copy = df_1_copy[df_1_copy.retweeted_status_timestamp.isnull()]


# ### Test

# In[48]:


df_1_copy.retweeted_status_id.notnull().sum(), df_1_copy.retweeted_status_user_id.notnull().sum(), df_1_copy.retweeted_status_timestamp.notnull().sum()


# ###### e) Time_stamp column is a datetime data type.

# ### Define
# 
# Convert the time_stamp column's data type from a string to datetime using to_datetime

# ### Code

# In[49]:


# convert datatype from string to datatime
df_1_copy.timestamp = pd.to_datetime(df_1_copy.timestamp)


# ### Test

# In[50]:


df_1_copy.timestamp.head()


# ###### f) Retweet Columns

# ### Define
# 
# Drop columnns retweeted_status_id, retweeted_status_user_id and retweeted_status_timestamp

# ### Code

# In[51]:


df_1_copy.drop(columns= ['retweeted_status_id', 'retweeted_status_user_id', 'retweeted_status_timestamp'], axis=1, inplace = True)


# ### Test

# In[52]:


df_1_copy.head()


# ###### g) Inconsistent letter case for values in P1, P2 and P3

# ### Define
# 
# Change letter case to uppercase in the second data frame

# ### Code

# In[53]:


df_2_copy['p1'] = df_2_copy['p1'].str.upper()
df_2_copy['p2'] = df_2_copy['p2'].str.upper()
df_2_copy['p3'] = df_2_copy['p3'].str.upper()


# ### Test

# In[54]:


df_2_copy


# ###### h) Convert p1_conf, p2_conf, p3_conf columns to percentage

# ### Define
# 
# Convert p1_conf, P2_conf and p3_conf values to percentage

# ### Code

# In[55]:


df_2_copy['p1_conf'] = (df_2_copy['p1_conf'] * 100).round(0)
df_2_copy['p2_conf'] = (df_2_copy['p2_conf'] * 100).round(0)
df_2_copy['p3_conf'] = (df_2_copy['p3_conf'] * 100).round(0)


# ### Test

# In[56]:


df_2_copy.head()


# ### Cleaning Tidiness Issues

# ###### i) Dog stages in different columns should be melted into a single column.

# ### Define
# 
# Merge dog stages into a single column

# ### Code

# In[57]:


df_1_copy.doggo.replace('None', '', inplace=True)
df_1_copy.floofer.replace('None', '', inplace=True)
df_1_copy.pupper.replace('None', '', inplace=True)
df_1_copy.puppo.replace('None', '', inplace=True)

df_1_copy['dog_stage'] = df_1_copy.doggo + df_1_copy.floofer + df_1_copy.pupper + df_1_copy.puppo

df_1_copy.loc[df_1_copy.dog_stage == 'doggopupper', 'dog_stage'] = 'doggo,pupper'
df_1_copy.loc[df_1_copy.dog_stage == 'doggopuppo', 'dog_stage'] = 'doggo,puppo'
df_1_copy.loc[df_1_copy.dog_stage == 'doggofloofer', 'dog_stage'] = 'doggo,floofer'


# In[58]:


df_1_copy.drop(['doggo', 'floofer',
             'pupper', 'puppo'], axis = 1, inplace = True)


df_1_copy['dog_stage'] = df_1_copy['dog_stage'].replace('', 'none')


# In[59]:


df_1_copy


# ###### ii) The three data set to be merged into a single data set

# ### Define 
# 
# Merge the data frames (df_1_copy, df_2_copy, df_3_copy) into a single data_frame (Master_df)

# ### Code

# In[60]:


Master_df = pd.merge(df_1_copy, df_2_copy, on='tweet_id', how='left').merge(df_3_copy, on='tweet_id', how='left')


# ### Test

# In[61]:


Master_df.info()


# In[62]:


Master_df.head()


# ## Storing Data
# 
# In the storing data section, the master_df will be stored in a CSV file named twitter_archive_master.csv

# In[63]:


# store data
Master_df.to_csv('twitter_archive_master.csv', index = False)


# ## Analyzing and Visualizing Data
# 
# In this section, the wrangled data will be analyzed providing at least 3 insight and 1 visualization

# In[64]:


#Read csv file
twitter_master_df = pd.read_csv('twitter_archive_master.csv')


# In[65]:


twitter_master_df.head()


# In[66]:


twitter_master_df.info()
twitter_master_df.shape


# In[67]:


twitter_master_df.describe()


# In[72]:


# Count of unique values in name
twitter_master_df['name'].value_counts()


# A total of 680 dogs have no name in the data frame.

# In[73]:


# Percentage distribution of names
((twitter_master_df['name'].value_counts()/twitter_master_df['name'].count())*100).round(0)


# 31% of the dogs have no name

# In[68]:


#Count of Values of unique dog stages
twitter_master_df['dog_stage'].value_counts()


# A total of 1831 dogs fall into the none category

# In[71]:


# percentage of unique dog stages
((twitter_master_df['dog_stage'].value_counts()/twitter_master_df['dog_stage'].count())*100).round(0)


# 84% of the dogs have an unidentified dog stage, pupper is the most significant dog_stage in the data set.

# In[75]:


# Tweet id with the highest retweet_count
(twitter_master_df[['tweet_id']][twitter_master_df.retweet_count == twitter_master_df.retweet_count.max()])


# In[88]:


twitter_master_df.nlargest(1,columns='retweet_count',keep='first')


# Tweet_id 744234799360020481 recorded the highest number of retweet of 70330

# In[84]:


# Tweet id with the lowest retweet_count
(twitter_master_df[['tweet_id']][twitter_master_df.retweet_count == twitter_master_df.retweet_count.min()])


# In[85]:


twitter_master_df.nsmallest(1,columns='retweet_count',keep='first')


# Tweet_id 838085839343206401 recorded the lowest number of retweet of 1

# In[81]:


# Tweet id with the most favorite_count
(twitter_master_df[['tweet_id']][twitter_master_df.favorite_count == twitter_master_df.favorite_count.max()])


# In[90]:


twitter_master_df.nlargest(1,columns='favorite_count',keep='first')


# Tweet_id 744234799360020481 recorded the highest number of favourite count of 144247

# In[82]:


# Tweet id with the least favorite_count
(twitter_master_df[['tweet_id']][twitter_master_df.favorite_count == twitter_master_df.favorite_count.min()])


# In[89]:


twitter_master_df.nsmallest(1,columns='favorite_count',keep='first')


# Tweet_id 744234799360020481 recorded the least number of favourite count of 45

# ### Visualization

# In[92]:


# Most significant dog stage
sns.set(rc={'figure.figsize':(10, 7)})
sns.countplot(twitter_master_df.dog_stage)
plt.title('Most Significant Dog Stage')
plt.xlabel('Dog stages', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.show()


# The visualization shows that the none category has the highest however, this cab be said to be invalid because it means dogs that belongs to this category have no stages. The pupper and doggo are more significant as they are a valid dog stage 
