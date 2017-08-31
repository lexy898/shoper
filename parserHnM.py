import requests
import json
import logging
import time
import sqlRequests

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')
company = 'h&m'
pageSize = 30

femaleUrl ='https://app2.hm.com/hmwebservices/service/app/productList?storeId=hm-russia&catalogVersion=Online&locale=ru&categories=ladies_all&start='
maleUrl = 'https://app2.hm.com/hmwebservices/service/app/productList?storeId=hm-russia&catalogVersion=Online&locale=ru&categories=men_all&start='
childrensUrl = 'https://app2.hm.com/hmwebservices/service/app/productList?storeId=hm-russia&catalogVersion=Online&locale=ru&categories=kids_all&start='
homeUrl = 'https://app2.hm.com/hmwebservices/service/app/productList?storeId=hm-russia&catalogVersion=Online&locale=ru&categories=home_all&start='
endOfUrl = '&pageSize=30&sale_boolean=true'
thingByIdUrl = 'https://app2.hm.com/hmwebservices/service/article/get-article-by-code/hm-russia/Online/'
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
    global parsed_string
    startIndex = 0
    failCounter = 0
    loaded_results = []
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
                loaded_results.extend(parsed_string["results"])
                print("company: " + company + " | page: " + str(startIndex / pageSize + 1))
                startIndex += pageSize
                failCounter = 0
            else:
                if (response.status_code == 403 and failCounter < 5):
                    print(response.status_code)
                    failCounter += 1
                    time.sleep(10)
                else:
                    break
        sqlRequests.setCookies(company, str(cookies)) #Сохраняем обновленные куки в БД

    except requests.exceptions.ConnectTimeout as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.ReadTimeout as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.ConnectionError as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.HTTPError as err:
        logging.error(u'' + str(err) + '')

    for full_result in loaded_results:
        result = [full_result["defaultCode_string"],
                  full_result["productWhitePrice_rub_double"],
                  full_result["actualPrice_rub_double"],
                  full_result["name_text_ru"],
                  full_result.get("sizes_ru_string_mv","-"),]
        results.append(result)
    return results

def getThingStatusById(id):
    global parsed_string
    headers = sqlRequests.getHeaders(company)
    cookies = sqlRequests.getCookies(company)
    try:
        req = thingByIdUrl + str(id) + "/ru"
        response = requests.get(req, headers=headers, cookies=cookies, timeout = 15.0)
        if (response.status_code == 200):
            cookies.update(dict(response.cookies))  # Обновляем куки
            sqlRequests.setCookies(company, str(cookies))  # Сохраняем обновленные куки в БД
            json_string = response.content
            try:
                parsed_string = json.loads(json_string)
                if (parsed_string["product"] == []):
                    return False
            except ValueError as err:
                logging.error(u'' + str(err) + ' Ошибка парсинга JSON')
            product = parsed_string["product"]
            inStock = product.get("inStock","False")
            print("id: "+str(id)+" inStock: "+str(inStock))
            if inStock:
                return True
            else:
                return False

    except requests.exceptions.ConnectTimeout as err:
        logging.error(u'' + str(err) + '')
        return False
    except requests.exceptions.ReadTimeout as err:
        logging.error(u'' + str(err) + '')
        return False
    except requests.exceptions.ConnectionError as err:
        logging.error(u'' + str(err) + '')
        return False
    except requests.exceptions.HTTPError as err:
        logging.error(u'' + str(err) + '')
        return False

def getFemale():
    return getThings(femaleUrl, endOfUrl)

def getMale():
    return getThings(maleUrl, endOfUrl)

def getChildrens():
    return getThings(childrensUrl, endOfUrl)

def getHOME():
    return getThings(homeUrl, endOfUrl)
