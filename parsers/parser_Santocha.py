from parsers import base_parser
from bs4 import BeautifulSoup
import logging

class ParserSantocha(base_parser.BaseParser):

    def __init__(self):
        super().__init__()
        logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                            filename=u'log.txt')
        self._PAGE_SIZE = 48

    # Метод получает все вещи с переданой страницы
    def _get_things_by_sale_page(self, response, old_things):
        results = []
        soup = BeautifulSoup(response.content, "html.parser")
        product_grid = soup.find('div', class_='isproductgrid')
        products = product_grid.find_all('div', {'class': 'producttileinner'})
        if not products:
            return results
        for product in products:
            try:
                code = product.find('div', {'class': 'image thumbnail productimage'}).get('data-productid')
                price = product.find('div', {'class': 'pricinginitial'}).find('div').find('div').get(
                    'data-standardprice').replace("-", "0")
                actual_price = product.find('div', {'class': 'pricinginitial'}).find('div').find('div').get(
                    'data-salesprice').replace("-", "0")
                name = product.find('div', {'class': 'name'}).find('a').text
                link = product.find('div', {'class': 'name'}).find('a').get('href')
                if code not in old_things:
                    thing_page = self._get_thing_page(link)
                    thing = [code, price, actual_price, name, self._get_sizes_by_page(thing_page), link,
                             self._get_thing_status_by_page(thing_page)]
                else:
                    thing = [code, price, actual_price, name, '-', link, False]
                results.append(thing)
            except ValueError:
                continue
        return results

    def _get_sizes_by_page(self, thing_page):
        sizes = []
        try:
            if thing_page.status_code == 200:
                try:
                    soup = BeautifulSoup(thing_page.content, "html.parser")
                    swatchesdisplay = soup.find('div', {'class': 'sizes-panel-inner'})\
                        .find('ul', {'class': 'swatchesdisplay'})
                    sizes_list = swatchesdisplay.find_all('li')
                    for size in sizes_list:
                        if 'variant-off' in size.get('class') or 'master-off' in size.get('class'):
                            continue
                        else:
                            sizes.append(size.find('a').text)
                except ValueError as err:
                    logging.error(u'' + str(err) + '')
        finally:
            return sizes

    def _get_thing_status_by_page(self, thing_page):
        status = True
        try:
            if thing_page.status_code == 200:
                try:
                    BeautifulSoup(thing_page.content, "html.parser").find('div', {'class': 'promoprice'}).text
                except AttributeError:
                    status = False
        finally:
            return status

    def _create_req(self, url, start_index):
        return url + "?sz="+str(self._PAGE_SIZE)+"&start=" + str(start_index)
