import os
from datetime import datetime
from NewsfeedSQLiteDB import NewsfeedSQLiteRepository

class Generic:
    def __init__(self, newsfeed_type):
        self.newsfeed_type = newsfeed_type
        self.newsfeed_header = f'{self.newsfeed_type} -------------------------'
        self._text = ''
        self._additional_info = ''
        self.footer = '------------------------------\n\n\n'

    def set_text_user_input(self, text):
        self._text = text

    def set_additional_info_user_input(self, additional_info):
        self._additional_info = additional_info

    def get_content(self):
        return '\n'.join([self.newsfeed_header, self._text, self._additional_info, self.footer])


class News(Generic):
    def __init__(self, text=None, city=None):
        self.newsfeed_type = 'News'
        super().__init__(self.newsfeed_type)
        self._text = text
        self._additional_info = f'{city}, {datetime.today()}'

    def set_additional_info_user_input(self, additional_info):
        self._additional_info = f'{additional_info}, {datetime.today()}'


class PrivateAd(Generic):
    def __init__(self, text=None, exp_date=None):
        self.newsfeed_type = 'PrivateAd'
        super().__init__(self.newsfeed_type)
        self._text = text
        self.exp_date = exp_date
        self._additional_info = self.__calculate_days_left(exp_date)

    def __calculate_days_left(self, additional_info):
        if additional_info is not None:
            return f'Actual until: {additional_info}, ' \
                   f'{(datetime.strptime(additional_info, "%Y-%m-%d") - datetime.now()).days} days left'

    def set_additional_info_user_input(self, additional_info):
        self._additional_info = self.__calculate_days_left(additional_info)


class Product(Generic):
    def __init__(self, text=None, price=None):
        self.newsfeed_type = 'Product'
        super().__init__(self.newsfeed_type)
        self._text = text
        self.__levels = {'cheap': 100, 'normal': 500, 'expensive': 1500}
        self._additional_info = f"Price: {price} BYN, {self.__calculate_price_level(price)}"

    def __calculate_price_level(self, price):
        if price is not None:
            for k, v in self.__levels.items():
                if float(price) < v:
                    return k
                else:
                    return 'very expensive'

    def set_additional_info_user_input(self, additional_info):
        self._additional_info = f"Price: {additional_info} BYN, {self.__calculate_price_level(additional_info)}"


def validate_date_format(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime("%Y-%m-%d"):
            raise ValueError
        return True
    except ValueError:
        return False


def validate_date(date_text):
    try:
        if datetime.strptime(date_text, "%Y-%m-%d") < datetime.now():
            raise ValueError
        return True
    except ValueError:
        return False


def validate_price(price_text):
    try:
        float(price_text)
        return True
    except ValueError:
        return False

def add_record(output_directory='.', file_name='newsfeed.txt'):
    newsfeed_file_path = os.path.join(output_directory, file_name)
    file_ext = file_name.split('.')[1]
    while True:
        i = input('What do you want to enter (1 - news, 2 - Private Ad, 3 - Product, 0 - exit): ')
        if i == "1":
            news = News()
            news.set_text_user_input(input('Enter news text: '))
            news.set_additional_info_user_input(input('Enter city: '))
            if file_ext == 'txt':
                with open(newsfeed_file_path, "a") as file:
                    file.write(news.get_content())
            elif file_ext == 'sqlite':
                with NewsfeedSQLiteRepository(newsfeed_file_path) as db:
                    table = 'News'
                    content = news.get_content().split('\n')
                    db.add_record(table, content[1], content[2])
            else:
                print(f"Format {file_ext} does not support!!!")
        elif i == "2":
            privatead = PrivateAd()
            privatead.set_text_user_input(input('Enter private ad text: '))
            expiration_date = input('Enter private ad expiration date: ')
            while not validate_date_format(expiration_date):
                expiration_date = input('Please enter date in format %Y-%m-%d: ')
            while not validate_date(expiration_date):
                expiration_date = input(f'Please enter date greater than {datetime.now()}: ')
            privatead.set_additional_info_user_input(expiration_date)
            if file_ext == 'txt':
                with open(newsfeed_file_path, "a") as file:
                    file.write(privatead.get_content())
            elif file_ext == 'sqlite':
                with NewsfeedSQLiteRepository(newsfeed_file_path) as db:
                    table = 'PrivateAd'
                    content = privatead.get_content().split('\n')
                    db.add_record(table, content[1], content[2])
            else:
                print(f"Format {file_ext} does not support!!!")
        elif i == "3":
            product = Product()
            product.set_text_user_input(input('Enter product name: '))
            product.set_additional_info_user_input(input('Enter product price: '))
            if file_ext == 'txt':
                with open(newsfeed_file_path, "a") as file:
                    file.write(product.get_content())
            elif file_ext == 'sqlite':
                with NewsfeedSQLiteRepository(newsfeed_file_path) as db:
                    table = 'Product'
                    content = product.get_content().split('\n')
                    db.add_record(table, content[1], content[2])
            else:
                print(f"Format {file_ext} does not support!!!")
        elif i == "0":
            break
        else:
            print('Wrong input!')


if __name__ == "__main__":
    add_record()
