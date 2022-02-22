from datetime import datetime


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

    def collect_info(self):
        self.set_text_user_input()
        self.set_additional_info_user_input()


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
        self._additional_info = f'Actual until: {exp_date}, ' \
                                f'{(datetime.strptime(exp_date, "%Y-%m-%d") - datetime.now()).days} days left'

    def set_additional_info_user_input(self, additional_info):
        self._additional_info = f'Actual until: {additional_info}, ' \
                                f'{(datetime.strptime(additional_info, "%Y-%m-%d") - datetime.now()).days} days left'


class Product(Generic):
    def __init__(self, text=None, price=None):
        self.newsfeed_type = 'Product'
        super().__init__(self.newsfeed_type)
        self._text = text
        self.__levels = {'cheap': 100, 'normal': 500, 'expensive': 1500}
        self._additional_info = f"Price: {price} BYN, {self.__calculate_price_level(price)}"

    def __calculate_price_level(self, price):
        for k, v in self.__levels.items():
            if float(price) < v:
                return k
        else:
            return 'very expensive'

    def set_additional_info_user_input(self, additional_info):
        self._additional_info = f"Price: {additional_info} BYN, {self.__calculate_price_level(additional_info)}"


def validate_date(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime("%Y-%m-%d"):
            raise ValueError
        return True
    except ValueError:
        return False


with open("newsfeed.txt", "a") as file:
    while True:
        i = input('What do you want to enter (1 - news, 2 - Private Ad, 3 - Product, 0 - exit): ')
        supported_articles = {'1': 'News()', '2': 'PrivateAd()'}
        a = eval(supported_articles[i]).set_text_user_input(input('Enter news text: '))

        if i == "1":
            news = News()
            news.set_text_user_input(input('Enter news text: '))
            news.set_additional_info_user_input(input('Enter city: '))
            file.write(news.get_content())
        elif i == "2":
            privatead = PrivateAd()
            privatead.set_text_user_input(input('Enter private ad text: '))
            expiration_date = input('Enter private ad expiration date: ')
            while not validate_date(expiration_date):
                expiration_date = input('Please enter date in format %Y-%m-%d: ')
            privatead.set_additional_info_user_input(expiration_date)
            file.write(privatead.get_content())
        elif i == "3":
            product = Product()
            product.set_text_user_input(input('Enter product name: '))
            product.set_additional_info_user_input(input('Enter product price: '))
            file.write(product.get_content())
        elif i == "0":
            break
        else:
            print('Wrong input!')
