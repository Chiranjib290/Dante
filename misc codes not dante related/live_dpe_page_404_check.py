import requests as r

url = 'https://www.pwc.co.uk/events/templates/webcast-pre-reg-thank-you.html'
url="https://www.strategyand.pwc.com/pt/en"
url="https://www.pwc.co.uk/industries/hospitality-leisure.html"
response = r.get(url)

print(response.status_code)