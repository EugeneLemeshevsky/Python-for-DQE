from Newsfeed import add_record
from Parse_from_files import TxtParser, JsonParser, XmlParser
from word_letter_calculator import WordCalculator, LetterCalculator

if __name__ == '__main__':
    a = input("Enter record by hands (1) or read from files? (2): ")
    output_dir = input("Enter output directory (Press 'Enter' to use default ('./newsfeed') directory): ")
    output_dir = output_dir if output_dir != '' else 'newsfeed'
    file_name = input("Enter filename with newsfeed with extension (Press 'Enter' to use default ('newsfeed.txt') file name): ")
    file_name = file_name if file_name != '' else 'newsfeed.txt'
    if a == '1':
        add_record(output_directory=output_dir, file_name=file_name)
    elif a == '2':
        input_dir = input("Input directory with records (Press 'Enter' to use default (./records)) directory: ")
        input_dir = input_dir if input_dir != '' else 'records'
        fmt = input('What format of records? (1 - txt,  2 - json, 3 - xml) (default txt): ')
        parser = ""
        file_ext = ""
        if fmt == "2":
            parser = "JsonParser"
            file_ext = ".json"
        elif fmt == "3":
            parser = "XmlParser"
            file_ext = ".xml"
        else:
            parser = "TxtParser"
            file_ext = ".txt"
        cmd = parser + "(working_directory=input_dir, output_directory=output_dir, newsfeed_file_name=file_name, input_file_extension=file_ext)"
        p = eval(cmd)
        if p is not None:
            p.parse_directory()

    wc = WordCalculator(working_directory=output_dir, filename=file_name)
    lc = LetterCalculator(working_directory=output_dir, filename=file_name)
    wc.calculate_words()
    wc.save_csv()
    lc.calculate_letters()
    lc.save_csv()