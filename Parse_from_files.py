import os
from Newsfeed import News, PrivateAd, Product, validate_date_format, validate_date, validate_price
from Text_normalization import normalize_text


class Parser:
    def __new__(cls, working_directory='records', output_directory='newsfeed'):
        if not os.path.exists(working_directory):
            print(f"Directory '{working_directory}' does not exists!!!")
            return None
        elif not list(filter(lambda x: x.endswith('.txt'), os.listdir(working_directory))):
            print(f"Directory '{working_directory}' does not contain any record!!!")
            return None
        else:
            return super().__new__(cls)

    def __init__(self, working_directory='records', output_directory='newsfeed',
                 newsfeed_file_name='newsfeed.txt'):
        self.working_directory = working_directory
        self.files_list = list(filter(lambda x: x.endswith('.txt'), os.listdir(working_directory)))
        if not os.path.exists(output_directory):
            os.mkdir(output_directory)
        self.newsfeed_file_path = os.path.join(output_directory, newsfeed_file_name)
        self.separators = r'[.]\s*'

    def parse_directory(self):
        for f in self.files_list:
            file_name = os.path.join(self.working_directory, f)
            self.parse_file(file_name)

    def _parse_and_write_record(self, item_type, item_text, item_additional_info):
        if item_type == "PrivateAd" and not (validate_date_format(item_additional_info) and validate_date(item_additional_info)):
                print('Wrong date format!')
                return False
        if item_type == "Product" and not validate_price(item_additional_info):
                print('Wrong price format!')
                return False
        else:
            r = eval(item_type + '()')
            r.set_text_user_input(normalize_text(item_text, self.separators))
            r.set_additional_info_user_input(item_additional_info)
            file = open(self.newsfeed_file_path, "a")
            file.write(r.get_content())
            file.close()
            return True

    def parse_file(self, file_path):
        with open(file_path, "r") as file:
            feed_list = file.read().split('\n\n\n')
        c = input(f"How many records to process from file {os.path.basename(file_path)}?")
        c = int(c)
        c = c if (c < len(feed_list)) else len(feed_list)
        wrong_records = []
        for item in feed_list[:c]:
            if not self._parse_and_write_record(*item.split('\n-\n')):
                print(f"File {file_path} contains wrong records.")
                wrong_records.append(item)
        if c < len(feed_list):
            with open(file_path, "w") as file:
                for item in feed_list[c:]:
                    file.write(item+'\n\n\n')
        else:
            os.remove(file_path)
        if len(wrong_records) != 0:
            wrong_records_file_path = file_path.replace('.txt', '_wrong_records.txt')
            with open(wrong_records_file_path, "w") as file:
                for item in wrong_records:
                    file.write(item+'\n\n\n')


if __name__ == "__main__":
    p = Parser()
    p.parse_directory()
