import datetime


class News:
    def __init__(self, text, city):
        self.text = text
        self.city = city
        self.date = datetime.datetime.today()

    def __str__(self):
        return f"News -------------------------\n{self.text}\n{self.city}," \
               f" {self.date}\n------------------------------\n\n\n"

    @classmethod
    def get_user_input(self):
        while 1:
            try:
                text = input('Enter news text: ')
                city = input('Enter city: ')
                return self(text, city)
            except:
                print('Invalid input!')
                continue


class PrivateAd:
    def __init__(self, text, exp_date):
        self.text = text
        self.exp_date = exp_date
        self.date = (datetime.datetime.strptime(exp_date, "%Y-%m-%d") - datetime.datetime.now()).days

    def __str__(self):
        return f"Private Ad ------------------\n{self.text}\nActual until: {self.exp_date}," \
               f" {self.date}  days left\n------------------------------\n\n\n"

    @classmethod
    def get_user_input(self):
        while 1:
            try:
                text = input('Enter private ad text: ')
                exp_date = input('Enter private ad expiration date: ')
                return self(text, exp_date)
            except:
                print('Invalid input!')
                continue


class Product:
    def __init__(self, text, price):
        self.text = text
        self.price = price
        self.levels = {'cheap': 100, 'normal': 500, 'expensive': 1500}
        for k, v in self.levels.items():
            if price < v:
                self.price_level = k
                break
            else:
                self.price_level = 'very expensive'

    def __str__(self):
        return f"Product -------------------------\n{self.text}\nPrice: {self.price} BYN," \
               f" {self.price_level}\n------------------------------\n\n\n"

    @classmethod
    def get_user_input(self):
        while 1:
            try:
                text = input('Enter product name: ')
                price = input('Enter product price: ')
                return self(text, float(price))
            except:
                print('Invalid input!')
                continue


with open("newsfeed.txt", "a") as file:
    while True:
        i = input('What do you want to enter (1 - news, 2 - Private Ad, 3 - Product, 0 - exit): ')
        if i == "1":
            news = News.get_user_input()
            file.write(str(news))
        elif i == "2":
            privatead = PrivateAd.get_user_input()
            file.write(str(privatead))
        elif i == "3":
            product = Product.get_user_input()
            file.write(str(product))
        elif i == "0":
            break
        else:
            print('Wrong input!')
