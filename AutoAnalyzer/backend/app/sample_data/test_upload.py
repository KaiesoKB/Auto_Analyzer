import requests

url = "http://127.0.0.1:8000/upload/"
files = {"file": open("retail_demo.csv", "rb")}

response = requests.post(url, files=files)
print(response.json())