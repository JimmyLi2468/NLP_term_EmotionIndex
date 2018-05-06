# NLP_term_EmotionIndex
###### Term project of NLP. An Emotion Volatility Index uses sentiment analysis(svm) on financial news articles
**Training Data:**
	  - in /dataset folder, yelp review data. 
	  - parse.py get all 5-star/1-star review as pos/neg training data


**classifier.py**
	  - train a model
	  - calculate accuracy/precision of the model
	
**News Data**
	  - in /financial-news-dataset-master folder, Bloomberg and Reuters news
	  - from 2006/10/20 to 2013/11/26
	  - parse.py 
		  - get every news' date+context
		  - put them into one file news.json & news.txt
		  ###### Example
		  '''
			  2010-08-01
				  Bridgepoint Capital Ltd is in advanced talks to buy French 
				  jewelery retailers Histoire dOr and Marc [...] Qualium 
				  Investissement    To contact the reporter on this story  
				  Jonathan Browning  in London   jbrowning9bloombergnet                                         
			  2010-08-01
				  Cell C Pty Ltd South Africas thirdlargest mobile phoneoperator 
				  apologized to customers for poor service and said it was taking 
				  steps to fix the problem    Criticism [...] South Africas 
				  biggest mobilephone operators    To contact the reporter on 
				  this story  Mike Cohen  in Cape Town at   mcohen21bloombergnet
		  '''
		
**news file is to large so splited because it is too large to process**
	  - /xa
	  - However, there is too many, not able to upload

**term.py**
	  - train the model
	  - use the model to classify all news article
	  - store to a file of resulted classification
	  - result.txt
	
**lastParse.py**
	  - process result.txt to assign weights to the positive and the negative each day
	  - create a file for plot
	  - final.txt

**plot.py**
	  - plot the data
	  - \plots
	
	## NLP term project Emotion_Index
 
