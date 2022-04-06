import os
from typing import List

from Newsfeed import News, PrivateAd, Product, validate_date_format, validate_date, validate_price
from Text_normalization import normalize_text
import json


class Parser:
    def __new__(cls, working_directory, output_directory,
                newsfeed_file_name, input_file_extension):
        print(input_file_extension)
        file_lst: list[str] = list(filter(lambda x: x.endswith(input_file_extension), os.listdir(working_directory)))
        print(file_lst)
        if not os.path.exists(working_directory):
            print(f"Directory '{working_directory}' does not exists!!!")
            return None
        elif not file_lst:
            print(f"Directory '{working_directory}' does not contain any record!!!")
            return None
        else:
            return super().__new__(cls)

    def __init__(self, working_directory='records', output_directory='newsfeed',
                 newsfeed_file_name='newsfeed.txt', input_file_extension='.txt'):
        self.working_directory = working_directory
        self.input_file_extension = input_file_extension
        self.files_list = list(filter(lambda x: x.endswith(self.input_file_extension), os.listdir(working_directory)))
        if not os.path.exists(output_directory):
            os.mkdir(output_directory)
        self.newsfeed_file_path = os.path.join(output_directory, newsfeed_file_name)
        self.separators = r'[.]\s*'
        self.feed_list = []

    def parse_directory(self):
        for f in self.files_list:
            file_name = os.path.join(self.working_directory, f)
            self.parse_file(file_name)

    def parse_file(self, file_path):
        self.get_feed_data(file_path)
        c = input(f"How many records to process from file {os.path.basename(file_path)}?")
        c = int(c)
        c = c if (c < len(self.feed_list)) else len(self.feed_list)
        wrong_records = []
        for item in self.feed_list[:c]:
            if not self._add_record(item):
                print(f"File {file_path} contains wrong records.")
                wrong_records.append(item)
        if c < len(self.feed_list):
            with open(file_path, "w") as file:
                for item in self.feed_list[c:]:
                    file.write(item+'\n\n\n')
        else:
            os.remove(file_path)
        if len(wrong_records) != 0:
            wrong_records_file_path = file_path.replace(self.input_file_extension, '_wrong_records'+self.input_file_extension)
            self.save_wrong_records(wrong_records_file_path, wrong_records)

    def _add_record(self, data):
        if data['type'] == "PrivateAd" and not (validate_date_format(data['additional_info']) and validate_date(data['additional_info'])):
                print('Wrong date format!')
                return False
        if data['type'] == "Product" and not validate_price(data['additional_info']):
                print('Wrong price format!')
                return False
        else:
            r = eval(data['type'] + '()')
            r.set_text_user_input(normalize_text(data['text'], self.separators))
            r.set_additional_info_user_input(data['additional_info'])
            file = open(self.newsfeed_file_path, "a")
            file.write(r.get_content())
            file.close()
            return True

    def get_feed_data(self, file_path):
        raise NotImplementedError()


    def save_wrong_records(self, file_path, wrong_records):
        raise NotImplementedError()


class TxtParser(Parser):
    def __init__(self, working_directory='records', output_directory='newsfeed',
                 newsfeed_file_name='newsfeed.txt', input_file_extension='.json'):
        super().__init__(working_directory=working_directory, output_directory=output_directory,
                         newsfeed_file_name=newsfeed_file_name, input_file_extension=input_file_extension)

    def get_feed_data(self, file_path):
        with open(file_path, "r") as file:
            txt_feed_data = file.read().split('\n\n\n')
        for item in txt_feed_data:
            data = item.split('\n-\n')
            self.feed_list.append({'type': data[0], 'text': data[1], 'additional_info': data[2]})

    def save_wrong_records(self, wrong_records_file_path, wrong_records):
        with open(wrong_records_file_path, "w") as file:
            for item in wrong_records:
                file.write('\n-\n'.join(item.values()))
                file.write('\n\n\n')


class JsonParser(Parser):
    def __init__(self, working_directory='records', output_directory='newsfeed',
                 newsfeed_file_name='newsfeed.txt', input_file_extension='.json'):
        super().__init__(working_directory=working_directory, output_directory=output_directory,
                         newsfeed_file_name=newsfeed_file_name, input_file_extension=input_file_extension)

    def get_feed_data(self, file_path):
        with open(file_path, 'r') as f:
            self.feed_list = json.load(f)

    def save_wrong_records(self, wrong_records_file_path, wrong_records):
        with open(wrong_records_file_path, "w") as file:
            file.write(json.dumps(wrong_records, indent=4))


if __name__ == "__main__":
    p = TxtParser()
    p.parse_directory()
