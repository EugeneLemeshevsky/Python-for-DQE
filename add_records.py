from Newsfeed import add_record
from Parse_from_files import Parser

if __name__ == '__main__':
    a = input("Enter record by hands (1) or read from files? (2): ")
    if a == '1':
        add_record()
    elif a == '2':
        input_dir = input("Input directory with records: ")
        input_dir = input_dir if input_dir != '' else 'records'
        p = Parser(working_directory=input_dir)
        if p is not None:
            p.parse_directory()
