from flaskk import Flask, render_template, request
from nltk import load_parser
import json
import pymongo
import os
import time
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
app = Flask(__name__)

lst = ['Dog','Apple','monkey','Apple.com','Balaibalan','balaguer','cat','Cigarette','Dell.com','Dell','Delkos','Delkash','Dellen','Delling','Dellys','Dalai_Lama_3904','delhi']
ret_value = []

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

@app.route("/",methods=['GET','POST'])
def template_test():
	del ret_value[:]
	namee = ""
	if request.form.get('searchbox') is "":
		return render_template('index.html')
	else:
		query = request.form.get('searchbox')
		query = str(query).lower()
		cp = load_parser('sub.fcfg')

		try:
			trees = list(cp.parse(query.split()))
			answer = trees[0].label()['SEM']
			answer = [s for s in answer if s]

			q = ' '.join(answer)
			print('question : ',q)

			jso = json.loads('{'+q+'}')

			client = pymongo.MongoClient()
			db = client.test
			data = db.capital.find(jso)
			# print(data[0]["Capital"])
			namee = data[0]["Capital"]
			#ret_value.append(namee)
			for i in lst:
					print(i)

					z = similar(namee,i.lower())
					print(z)
					if (z > 0.5):
						ret_value.append(i)

		except ValueError as e:
				
				for i in lst:
					print(i)

					z = similar(query,i.lower())
					print(z)
					if (z > 0.7):
						ret_value.append(i)
				print(ret_value)
	
	return render_template('index.html',results=ret_value)


@app.route('/result/<query>')
def show_result(query):
	resul = ""
	print(query)
	try:
		os.chdir('/media/shuvo/E/en/articles')
		s_time = time.time()
		level = 0
		query = str(query).lower()
		for i in query:
			print(i)
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
					resul = resul + ptag.get_text()
					print(ptag.get_text())
				break
			else:		
				flag = 1

		if(flag == 1):
			print("not Found")
	
		t_time = time.time()
		e_time = t_time - s_time
		print('Total Time taken : ', e_time,' sec')
	except FileNotFoundError as err:
		print('Ans no Found')
	return render_template('result.html',article=resul,time=e_time)

if __name__ == '__main__':
	app.run('0.0.0.0',5000,debug=True)

