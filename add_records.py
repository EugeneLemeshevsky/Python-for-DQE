from Newsfeed import add_record
from Parse_from_files import Parser
from word_letter_calculator import WordCalculator, LetterCalculator

if __name__ == '__main__':
    a = input("Enter record by hands (1) or read from files? (2): ")
    output_dir = input("Enter output directory: ")
    output_dir = output_dir if output_dir != '' else 'newsfeed'
    file_name = input("Enter filename with newsfeed with extension: ")
    file_name = file_name if file_name != '' else 'newsfeed.txt'
    if a == '1':
        add_record(output_directory=output_dir, file_name=file_name)
    elif a == '2':
        input_dir = input("Input directory with records: ")
        input_dir = input_dir if input_dir != '' else 'records'
        p = Parser(working_directory=input_dir, output_directory=output_dir)
        if p is not None:
            p.parse_directory()
    wc = WordCalculator(working_directory=output_dir, filename=file_name)
    lc = LetterCalculator(working_directory=output_dir, filename=file_name)
    wc.calculate_words()
    wc.save_csv()
    lc.calculate_letters()
    lc.save_csv()