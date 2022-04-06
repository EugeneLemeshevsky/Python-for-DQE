import re
import csv
import os
from collections import Counter

class TextUtility:
    def __init__(self, working_directory, filename, output_filename, col_names):
        self.working_directory = working_directory
        self.filename = filename
        self.col_names = col_names
        self.count_file_path = os.path.join(self.working_directory, output_filename)
        self.count_dict = {}
        self.read_newsfeed()

    def read_newsfeed(self):
        input_file_path = os.path.join(self.working_directory, self.filename)
        with open(input_file_path, "r") as feed:
            text = feed.read()
            self.words = re.split("[^A-Za-z]*[\s]", text)
            self.words.remove('')

    def save_csv(self):
        with open(self.count_file_path, "w", encoding='utf-8') as csv_file:
            csv_file = csv.DictWriter(csv_file, delimiter=',', lineterminator='\r',
                                      fieldnames=self.col_names)
            csv_file.writeheader()
            for data in self.count_dict.values():
                csv_file.writerow(data)

class WordCalculator(TextUtility):
    def __init__(self, working_directory='.', filename='newsfeed.txt', output_filename='words.csv'):
        super().__init__(working_directory=working_directory, filename=filename, output_filename=output_filename, col_names=['Word', 'Count'])

    def calculate_words(self):
        for word in self.words:
            if word.lower() in self.count_dict:
                self.count_dict[word.lower()][self.col_names[1]] += 1
            else:
                data = dict.fromkeys(self.col_names)
                data[self.col_names[0]] = word.lower()
                data[self.col_names[1]] = 1
                self.count_dict[word.lower()] = data


class LetterCalculator(TextUtility):
    def __init__(self, working_directory='.', filename='newsfeed.txt', output_filename='letters.csv'):
        super().__init__(working_directory=working_directory, filename=filename,
                         output_filename=output_filename, col_names=['letter', 'count_all', 'count_uppercase', 'percentage'])

    def _add_item(self, letter, count):
        item = dict.fromkeys(self.col_names)
        item[self.col_names[0]] = letter.lower()
        item[self.col_names[1]] = count
        item[self.col_names[2]] = count if letter.isupper() else 0
        perc = item[self.col_names[2]]/item[self.col_names[1]]*100
        item[self.col_names[3]] = round(perc, 2)
        self.count_dict[letter.lower()] = item

    def _update_item(self, letter, count):
        item = self.count_dict[letter.lower()]
        item[self.col_names[1]] += count
        count_uppercase_add = count if letter.isupper() else 0
        item[self.col_names[2]] += count_uppercase_add
        perc = item[self.col_names[2]]/item[self.col_names[1]]*100
        item[self.col_names[3]] = round(perc, 2)

    def calculate_letters(self):
        text = ' '.join(self.words)
        self.counter = Counter(text)
        for c, count in self.counter.items():
            if c == ' ':
                continue
            if c.lower() in self.count_dict:
                self._update_item(c, count)
            else:
                self._add_item(c, count)


if __name__ == '__main__':
    wc = WordCalculator()
    wc.calculate_words()
    wc.save_csv()

    lc = LetterCalculator()
    lc.calculate_letters()
    lc.save_csv()
