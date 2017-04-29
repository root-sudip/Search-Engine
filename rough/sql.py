from nltk import load_parser
import json
import pymongo
import os
import time
from bs4 import BeautifulSoup

cp = load_parser('/home/shuvo/python/sys/advance search algo/sub.fcfg')
#query = 'What cities are located in China'
#query = 'What is the capital of India'
#query = 'What is the capital of India'
query = input('Enter Query : ').lower()
try:
	trees = list(cp.parse(query.split()))
	answer = trees[0].label()['SEM']
	answer = [s for s in answer if s]
	#print(answer)
	# print(answer)
	q = ' '.join(answer)
	# print(q)

	json = json.loads('{'+q+'}')
	#print(json)

	client = pymongo.MongoClient()
	db = client.test
	data = db.capital.find(json)
	print(data[0]["Capital"])

# S[SEM=?n] -> N[SEM=?n]
# N[SEM='Apple'] -> 'Apple'
except ValueError as e:
	try:
		os.chdir('/media/shuvo/E/en/articles')
		s_time = time.time()
		level = 0
		for i in query:
			if (level == 3):
				break
			else:
				os.chdir(i)
				level = level + 1
		print(os.getcwd())
		flag = 0
		for name in os.listdir(os.getcwd()): 
			name.replace('_',' ')
			if(name.lower().replace(".html","") == query.replace(".html","")):#bug fixed
				flag = 0
				print(name)
				print('Found')
				fileOpen = open(name)
				soup = BeautifulSoup(fileOpen)
				tags = soup.find_all('p')
				for ptag in tags:
					print(ptag.get_text())
				break
			else:		
				flag = 1

		if(flag == 1):
			print("not Found")
	
		t_time = time.time()
		e_time = t_time - s_time
		print('Total Time is taken : ', e_time,' sec')
	except FileNotFoundError as err:
		print('Ans no Found')



