import requests
import json
import pickle


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str, keys: dict):
        if quote == base:
            raise ConvertionException(f'Не удалось перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось получить валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось получить валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * amount

        return total_base

    #получаем список валют из файла
    @staticmethod
    def get_values():
        try:
            with open('values.txt', 'rb') as file:
                keys = pickle.load(file)
        except FileNotFoundError:
            raise ConvertionException("Ошибка открытия файла с валютами")

        return keys

    #добавляем новые валюты для конвертации
    @staticmethod
    def add_values(name: str, ticker: str, keys: dict):
        if name in list(keys.keys()):
            raise ConvertionException(f'Валюта {name} уже доступна к конвертации')
        if ticker in list(keys.values()):
            raise ConvertionException(f'Тикер {ticker} уже используется')
        #проверяем существует ли валюта с указанным тикером(не уверен что данный запрос оптимален, но другой в api не нашел)
        r = requests.get(f'https://data-api.cryptocompare.com/asset/v1/data/by/symbol?asset_symbol={ticker}')
        result = json.loads(r.content)
        if len(result['Err']) > 0:
            raise ConvertionException(f'Валюты с тикером {ticker} не существует')
        else:
            try:
                keys[name] = ticker  #добавляем валюту в словарь
                with open('values.txt', 'wb') as file:
                    pickle.dump(keys, file)  #обновляем содержимое файла с валютами
            except FileNotFoundError:
                raise ConvertionException("Ошибка добавления в список валют")
