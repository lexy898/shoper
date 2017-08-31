import requests
import logging
import sqlRequests
import time
from bs4 import BeautifulSoup

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')
company = 'Roxy'
pageSize = 48

femaleUrl = "http://www.roxy-russia.ru/skidki-women/"
childrensUrl = "http://www.roxy-russia.ru/skidki-kids/"

def getThings(url):
    startIndex = 0
    failCounter = 0
    headers = sqlRequests.getHeaders(company)
    cookies = sqlRequests.getCookies(company)
    results = []
    try:
        while True:
            print("company: "+company+" | page: "+str(startIndex/pageSize+1))
            req = url+"?sz=48&start="+str(startIndex)
            response = requests.get(req, headers=headers, cookies=cookies)
            if (response.status_code == 200):
                cookies.update(dict(response.cookies))  # Обновляем куки
                soup = BeautifulSoup(response.content, "html.parser")

                productGrid = soup.find('div', class_='isproductgrid')
                products = productGrid.find_all('div', {'class': 'producttileinner'})
                if products == []:
                    break
                for product in products:
                    code = product.find('div', {'class': 'image thumbnail productimage'}).get('data-productid')
                    price = product.find('div', {'class': 'pricinginitial'}).find('div').find('div').get('data-standardprice').replace("-","0")
                    actualPrice = product.find('div', {'class': 'pricinginitial'}).find('div').find('div').get('data-salesprice').replace("-","0")
                    name = product.find('div', {'class': 'name'}).find('a').text
                    thing = [code, price, actualPrice, name,'-']
                    results.append(thing)
            else:
                if (response.status_code == 403 and failCounter < 5):
                    print(response.status_code)
                    failCounter += 1
                    time.sleep(10)
                else:
                    break
            sqlRequests.setCookies(company, str(cookies))  # Сохраняем обновленные куки в БД
            failCounter = 0
            startIndex += pageSize
    except requests.exceptions.ConnectTimeout as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.ReadTimeout as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.ConnectionError as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.HTTPError as err:
        logging.error(u'' + str(err) + '')
    print("Вещей загружено: "+str(len(results)))
    return results

def getThingStatusById(id):
    return True

def getFemale():
    return getThings(femaleUrl)

def getChildrens():
    return getThings(childrensUrl)