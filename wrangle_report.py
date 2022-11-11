#!/usr/bin/env python
# coding: utf-8
#### Reporting: wragle_report
* Create a **300-600 word written report** called "wrangle_report.pdf" or "wrangle_report.html" that briefly describes your wrangling efforts. This is to be framed as an internal document.
# #### DATA WRANGLING REPORT

# ###### Objective 
# 
# The objective of this report is to understand and carry out a data wrangling process by gathering data from a variety of sources and in a variety of formats, assess its quality and tidiness, then clean it. plus showcase them through analyses and visualizations using Python (and its libraries) and/or SQL.
# 

# #### Data Gathering 
# 
# The following are the steps carried out in the data gathering process
# -	Manually download the WeRateDogs Twitter archive data provided by Udacity and read it into a data frame.
# -	Programmatically download the second data (image prediction) using the Requests library and URL hosted on Udacity's servers.
# -	Query Twitter API for each tweet in the Twitter archive using Python's Tweepy library and save JSON in a text file. Write each tweet's JSON data to its own line, then read the tweet_json .txt file line by line into a pandas DataFrame with tweet ID, retweet count, and favorite count. 
# 

# #### Assessing Data
# 
# Following the gathering of the three pieces of data, I carried out a visual and programmatic assessment for quality and tidiness issues. Below are some of the assessment methods adopted
# -	df_1.info()
# -	df_1.shape()
# -	df_1.describe()
# -	df_3.isnull().sum()
# -	df_3.duplicated().sum()
# 

# #### Data Cleaning
# 
# In cleaning the data, the following were carried out
# -	I created a copy of the original data before cleaning
# -	I Adopted the define code-test framework
# -	I documented the define code-test framework
# -	I Created a master data frame with all pieces of gathered data 
# All the issues identified while assessing data will be cleaned and tidied up, the issues identified include:
# 
# Quality
# 
# -	Tweet_id in the three data frame is a string not an int
# -	Missing values in the (in_reply_to_status_id and in_reply_to_user_id) column
# -	Null values in the expanded url and repitition of url in some rows
# -	Tweet_ids with value in the retweeted_status_id, retweeted_status_user_id and retweeted_status_timestamp 
# -	Time_stamp column is a datetime data type.
# -	Retweet columns
# -	Inconsistent letter case for values in P1, P2 and P3
# -	Convert p1_conf, p2_conf, p3_conf columns to percentage
# 
# Tidiness
# 
# -	Dog stages in different columns should be melted into a single column.
# -	The three data set to be merged into a single data set
# 

# #### Storing Data
# 
# Following the gathering, assessing and cleaning process carried out, the master_df was stored in a CSV file named twitter_archive_master.csv
# 

# In[ ]:




