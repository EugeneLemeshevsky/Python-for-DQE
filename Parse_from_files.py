from datetime import datetime
import os
from Newsfeed import News, PrivateAd, Product, validate_date_format, validate_date


class Parser:
    def __init__(self, working_directory='.'):
        self.files_list = list(filter(lambda x: x.endswith('.txt'), os.listdir(working_directory)))
        self.working_directory = working_directory
        self.files_list.remove('newsfeed.txt')

    def parse_directory(self):
        for f in self.files_list:
            self.parse_file(self.working_directory + '/' + f)

    def _parse_and_write_record(self, item_type, item_text, item_additional_info):
        r = eval(item_type + '()')
        r.set_text_user_input(item_text)
        r.set_additional_info_user_input(item_additional_info)
        result = True
        if item_type == "PrivateAd":
            if not (validate_date(item_additional_info) and validate_date_format(item_additional_info)):
                result = False
        if result:
            file = open("newsfeed.txt", "a")
            file.write(r.get_content())
            file.close()
        return result

    def parse_file(self, file_path):
        feed_list = []
        with open(file_path, "r") as file:
            feed_list = file.read().split('\n\n\n')
        print(feed_list)
        wrong_records = []
        for item in feed_list:
            if not self._parse_and_write_record(*item.split('\n-\n')):
                print(f"File {file_path} contains wrong records.")
                wrong_records.append(item)

        if len(wrong_records) == 0:
            os.remove(file_path)
        else:
            with open(file_path, "w") as file:
                for item in wrong_records:
                    file.write(item+'\n\n\n')



if __name__ == "__main__":
    p = Parser()
    p.parse_directory()
