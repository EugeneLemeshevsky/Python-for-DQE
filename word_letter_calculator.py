import collections
import re
import csv
import os
from collections import Counter

class TextUtility:
    def __init__(self, working_directory, filename):
        "docstring"
        self.working_directory = working_directory
        self.filename = filename
        self.read_newsfeed()

    def read_newsfeed(self):
        input_file_path = os.path.join(self.working_directory, self.filename)
        with open(input_file_path, "r") as feed:
            text = feed.read()
            self.words = re.split("[^A-Za-z]*[\s]", text)
            self.words.remove('')


class WordCalculator(TextUtility):
    def __init__(self, working_directory='.', filename='newsfeed.txt'):
        super().__init__(working_directory=working_directory, filename=filename)
        self.word_counts = {}
        self.col_names = ['Word', 'Count']

    def calculate_words(self):
        for word in self.words:
            if word.lower() in self.word_counts:
                self.word_counts[word.lower()] += 1
                continue
            else:
                self.word_counts[word.lower()] = 1

    def save_csv(self):
        words_count_file_path = os.path.join(self.working_directory, "words.csv")
        with open(words_count_file_path, "w", encoding='utf-8') as csv_file:
            csv_file = csv.DictWriter(csv_file, delimiter=',', lineterminator='\r',
                                      fieldnames=self.col_names)
            csv_file.writeheader()
            for word, count in self.word_counts.items():
                csv_file.writerow({self.col_names[0]: word, self.col_names[1]: count})


class LetterCalculator(TextUtility):
    def __init__(self, working_directory='.', filename='newsfeed.txt'):
        super().__init__(working_directory=working_directory, filename=filename)
        self.letters_count = {}
        self.col_names = ['letter', 'count_all', 'count_uppercase', 'percentage']

    def _add_item(self, letter, count):
        item = dict.fromkeys(self.col_names)
        item['letter'] = letter.lower()
        item['count_all'] = count
        item['count_uppercase'] = count if letter.isupper() else 0
        perc = item['count_uppercase']/item['count_all']*100
        item['percentage'] = perc
        self.letters_count[letter.lower()] = item

    def _update_item(self, letter, count):
        item = self.letters_count[letter.lower()]
        item['count_all'] += count
        count_uppercase_add = count if letter.isupper() else 0
        item['count_uppercase'] += count_uppercase_add
        perc = item['count_uppercase']/item['count_all']*100
        item['percentage'] = perc

    def calculate_letters(self):
        text = ' '.join(self.words)
        self.counter = Counter(text)
        for c, count in self.counter.items():
            if c == ' ':
                continue
            if c.lower() in self.letters_count:
                self._update_item(c, count)
            else:
                self._add_item(c, count)

    def save_csv(self):
        letters_count_file_path = os.path.join(self.working_directory, 'letters.csv')
        with open(letters_count_file_path, "w", encoding='utf-8') as csv_file:
            csv_file = csv.DictWriter(csv_file, delimiter=',', lineterminator='\r',
                                      fieldnames=self.col_names)
            csv_file.writeheader()
            for data in self.letters_count.values():
                csv_file.writerow(data)


if __name__ == '__main__':
    wc = WordCalculator()
    wc.calculate_words()
    wc.save_csv()

    lc = LetterCalculator()
    lc.calculate_letters()
    lc.save_csv()
