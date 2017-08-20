import requests
import json
import logging
import time
import sqlRequests

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')
company = 'h&m'

femaleUrl ='https://app2.hm.com/hmwebservices/service/app/productList?storeId=hm-russia&catalogVersion=Online&locale=ru&categories=ladies_all&start='
maleUrl = 'https://app2.hm.com/hmwebservices/service/app/productList?storeId=hm-russia&catalogVersion=Online&locale=ru&categories=men_all&start='
childrensUrl = 'https://app2.hm.com/hmwebservices/service/app/productList?storeId=hm-russia&catalogVersion=Online&locale=ru&categories=kids_all&start='
homeUrl = 'https://app2.hm.com/hmwebservices/service/app/productList?storeId=hm-russia&catalogVersion=Online&locale=ru&categories=home_all&start='
endOfUrl = '&pageSize=30&sale_boolean=true'
'''
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
'''

def getThings(url, endOfUrl):
    startIndex = 0
    failCounter = 0
    results = []
    headers = sqlRequests.getHeaders(company)
    cookies = sqlRequests.getCookies(company)
    try:
        while True:
            req = url + str(startIndex) + endOfUrl
            response = requests.get(req, headers=headers, cookies=cookies)
            if (response.status_code == 200):
                cookies.update(dict(response.cookies)) #Обновляем куки
                json_string = response.content
                try:
                    parsed_string = json.loads(json_string)
                    if (parsed_string["results"] == []):
                        break
                except ValueError as err:
                    logging.error(u'' + str(err) + ' Ошибка парсинга JSON')
                results.extend(parsed_string["results"])
                print("item: "+str(startIndex)+"  "+str(len(results)))
                startIndex += 30
                failCounter = 0
            else:
                if (response.status_code == 403 and failCounter < 5):
                    print(response.status_code)
                    failCounter += 1
                    time.sleep(10)
                else:
                    break
        sqlRequests.setCookies(company, str(cookies)) #Сохраняем обновленные куки в БД
        return results

    except requests.exceptions.ConnectTimeout as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.ConnectionError as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.HTTPError as err:
        logging.error(u'' + str(err) + '')

def getFemale():
    return getThings(femaleUrl, endOfUrl)

def getMale():
    return getThings(maleUrl, endOfUrl)

def getChildrens():
    return getThings(childrensUrl, endOfUrl)

def getHOME():
    return getThings(homeUrl, endOfUrl)