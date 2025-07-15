import datetime
from datetime import date

import requests
from bs4 import BeautifulSoup


class ParsePageLinks:
    """
    Класс для парсинга страницы.

    Объект класса на вход получает url страницы для парсинга, tag и class_html
    по которому будет осуществляться парсинг.
    """
    def __init__(self, url: str, tag: str, class_html: str):
        self.url = url
        self.tag = tag
        self.class_html = class_html

    def _get_html(self):
        """Метод для получения html в виде текста по url."""
        return requests.get(self.url).text

    def _get_all_data_with_tag(self):
        """Метод для получения всех данных из тега."""
        soup = BeautifulSoup(self._get_html(), 'html.parser')
        data = soup.find_all(self.tag, class_=self.class_html)
        return data

    def get_links_in_date_interval(
            self,
            start_date: date,
            end_date: date,
            url_pattern: str,
            pattern_name: str,
            head_url: str):
        """
        Метод для получения ссылок по паттерну в диапазоне дат.

        url_pattern - отвечает что ссылка отвечает заданному пути
        pattern_name - помогает отделить дату в имени файла
        head_url - добавляет заголовок url если ссылка не полная
        Например:
        url_pattern = /upload/reports/oil_xls/oil_xls_
        pattern_name = oil_xls_
        head_url = https://spimex.com
        Из ссылки такого вида:
        href='/upload/reports/oil_xls/oil_xls_20240101_test.xls'
        Получит:
        [(https://spimex.com/upload/reports/oil_xls/oil_xls_20240101_test.xls,
        20240101)]
        """
        results = []
        for link in self._get_all_data_with_tag():
            href = link.get('href')
            if not href:
                continue

            href = href.split('?')[0]
            if url_pattern not in href or not href.endswith(
                    '.xls'):
                continue

            try:
                date = href.split(pattern_name)[1][:8]
                file = datetime.datetime.strptime(date, '%Y%m%d').date()
                if start_date <= file <= end_date:
                    u = href if href.startswith(
                        'http') else f'{head_url}{href}'
                    results.append((u, file))
                else:
                    print(f'Ссылка {href} вне диапазона дат')
            except Exception as e:
                print(f'Не удалось извлечь дату из ссылки {href}: {e}')
