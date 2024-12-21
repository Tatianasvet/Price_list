import os
import csv


class PriceMachine:
    product_names = ('товар', 'название', 'наименование', 'продукт')
    price_names = ('розница', 'цена')
    weight_names = ('вес', 'масса', 'фасовка')
    
    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0
    
    def load_prices(self, file_path='.'):
        for file in os.scandir(file_path):
            if 'price' in file.name:
                with open(os.path.join(file_path, file.name), mode='r', encoding='utf-8') as scan_file:
                    reader = csv.reader(scan_file, delimiter=',')
                    product_col, price_col, weight_col = '', '', ''
                    for row_number, row in enumerate(reader):
                        if row_number == 0:
                            product_col, price_col, weight_col = self._search_product_price_weight(row)
                        else:
                            product = row[product_col].lower()
                            price = int(row[price_col])
                            weight = int(row[weight_col])
                            self.data.append({'file': file.name,
                                              'product': product,
                                              'price': price,
                                              'weight': weight,
                                              'price per kg': round(price / weight, 2)})
        self.data.sort(key=lambda entry: (entry['price per kg'], entry['product'], entry['price']))

    def _search_product_price_weight(self, headers):
        product_col, price_col, weight_col = None, None, None
        for number, title in enumerate(headers):
            if title in self.product_names:
                product_col = number
            elif title in self.price_names:
                price_col = number
            elif title in self.weight_names:
                weight_col = number
        return product_col, price_col, weight_col

    def export_to_html(self, fname='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        for number, entry in enumerate(self.data):
            result += (f'<tr>'
                       f'<td>{number + 1}</td>'
                       f'<td>{entry["product"]}</td>'
                       f'<td>{entry["price"]}</td>'
                       f'<td>{entry["weight"]}</td>'
                       f'<td>{entry["file"]}</td>'
                       f'<td>{entry["price per kg"]}</td>'
                       f'</tr>')
        result += '</table></body>'
        with open(fname, mode='w') as file:
            file.write(result)
    
    def find_text(self, text):
        search_result = []
        for i in self.data:
            if text.lower() in i['product']:
                search_result.append(i)
        return search_result
    
pm = PriceMachine()
pm.load_prices()
print('Добро пожаловать в анализатор прайс-листов')
print("Для завершения работы введите \'exit\'")
while True:
    request = input('Поиск по названию продукта: ')
    if request == 'exit':
        break
    else:
        result = pm.find_text(request)
        if len(result) == 0:
            print(f'продукт {request} не найден')
        else:
            print(f'{'№':<4} {'Наименование':<35} {'Цена':<9} {'Вес':<7} {'Файл':<15} {'Цена за кг':<10}')
            for number, i in enumerate(result):
                print(f'{number:<4} '
                      f'{i["product"]:<35} '
                      f'{i["price"]:<9} '
                      f'{i["weight"]:<7} '
                      f'{i["file"]:<15} '
                      f'{i["price per kg"]:<10}')
print('the end')
pm.export_to_html()
