import os
from Newsfeed import News, PrivateAd, Product, validate_date_format, validate_date, validate_price
from Text_normalization import normalize_text
import json
import xml.etree.ElementTree as et
from NewsfeedSQLiteDB import NewsfeedSQLiteRepository


class Parser:
    def __new__(cls, working_directory, output_directory,
                newsfeed_file_name, input_file_extension):
        file_lst: list[str] = list(filter(lambda x: x.endswith(input_file_extension), os.listdir(working_directory)))
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
            self.save_records(file_path, self.feed_list[c:])
        else:
            os.remove(file_path)
        if len(wrong_records) != 0:
            wrong_records_file_path = file_path.replace(self.input_file_extension, '_wrong_records'+self.input_file_extension)
            self.save_records(wrong_records_file_path, wrong_records)

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
            file_ext = self.newsfeed_file_path.split('.')[1]
            if file_ext == 'txt':
                with open(self.newsfeed_file_path, "a") as file:
                    file.write(r.get_content())
            elif file_ext == 'sqlite':
                with NewsfeedSQLiteRepository(self.newsfeed_file_path) as db:
                    content = r.get_content().split('\n')
                    db.add_record(data['type'], content[1], content[0])
            else:
                print(f'Format {file_ext} does not support!')
            return True


    def get_feed_data(self, file_path):
        raise NotImplementedError()


    def save_records(self, file_path, records):
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

    def save_records(self, file_path, records):
        with open(file_path, "w") as file:
            for item in records:
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

    def save_records(self, file_path, records):
        with open(file_path, "w") as file:
            file.write(json.dumps(records, indent=4))


class XmlParser(Parser):
    def __init__(self, working_directory='records', output_directory='newsfeed',
                 newsfeed_file_name='newsfeed.txt', input_file_extension='.xml'):
        super().__init__(working_directory=working_directory, output_directory=output_directory,
                         newsfeed_file_name=newsfeed_file_name, input_file_extension=input_file_extension)

    def get_feed_data(self, file_path):
        tree = et.parse(file_path)
        root = tree.getroot()
        for item in root.findall('item'):
            record = {}
            for child in item:
                record[child.tag] = child.text
            self.feed_list.append(record)
        print(f'feed_data = {self.feed_list}')

    def save_records(self, file_path, records):
        with open(file_path, "wb") as file:
            xml_records = et.Element('records')
            for item in records:
                it = et.SubElement(xml_records, 'item')
                type_item = et.SubElement(it, 'type')
                type_item.text = item['type']
                text_item = et.SubElement(it, 'text')
                text_item.text = item['text']
                add_info_item = et.SubElement(it, 'additional_info')
                add_info_item.text = item['additional_info']
            rec_xml = et.tostring(xml_records)
            file.write(rec_xml)


if __name__ == "__main__":
    p = TxtParser()
    p.parse_directory()
