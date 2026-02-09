# import os
import requests
import json
import csv
import time
import threading

# Setting user Parameters
dataCenter = "fra1"
THREAD_COUNT = 26
ROW_LIST = []
INPUT_FILE_NAME = "input.csv"
OUTPUT_FILE_NAME = "input_out.csv"

# API token value from the Qualtrics account seetings page - It differs for each user
apiToken = "uTs9TnWexe4z8qteYsTuKezZaP495FcUZC4SOAel"

def fetch_api_data(urls, sleeptime):
	for url in urls:
		baseUrl1 = "https://{0}.qualtrics.com/API/v3/survey-definitions/{1}/metadata".format(dataCenter, url[0])
		headers = {
			"X-API-TOKEN": apiToken,
			}
		response = requests.request("GET", baseUrl1, headers=headers)
		time.sleep(0.5)
		try:
			result = json.loads(response.text)['result']['SurveyDescription']
			url.append(result)
			ROW_LIST.append(url)
		except Exception as e:
			# If SurveyDescription is missing add "Null"
			url.append("Null")
			ROW_LIST.append(url)
			
		print(baseUrl1)
		print(response.status_code)

# Get WBS code
def getWbs():
	try:
		with open(INPUT_FILE_NAME, 'r', encoding='utf-8') as file:
			reader = csv.reader(file)
			reader = list(reader)
			print("Processing the csv file")
			url_slice = []
			for u_count in range(THREAD_COUNT - 1):
				url_slice.append(reader[int(len(reader)/THREAD_COUNT)*u_count:int(len(reader)/THREAD_COUNT)*(u_count+1)])
			
			url_slice.append(reader[int(len(reader)/THREAD_COUNT)*(THREAD_COUNT-1):len(reader)])
			
			print(len(url_slice))
			threads = []
			status = None
			for i in range (THREAD_COUNT):
				# print(int(len(reader)/THREAD_COUNT)*i)
				# Fetch API Data
				t0 = threading.Thread(target=fetch_api_data, args=(url_slice[i], 0.5))
				t0.start()
				threads.append(t0)
			for athread in threads:
				athread.join()
				print("Thread "+str(athread)+" joined")
		
		print("Done...")
		file.close()
		
		with open(OUTPUT_FILE_NAME, 'w',newline='', encoding='utf-8') as csvfile:
			#print(ROW_LIST)
			csvwriter = csv.writer(csvfile)
			csvwriter.writerows(ROW_LIST)
		csvfile.close()
		
	except Exception as ex:
		print(ROW_LIST)
		print(ex)

# Call getWbs Function
if __name__ == '__main__':
	getWbs()
