import re

text = '''homEwork:
	tHis iz your homeWork, copy these Text to variable.

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.'''

normalized_text = text.lower()
sentences = re.split(r'\.\s|\n|\t', normalized_text)  # Breaking the text into sentences
for s in sentences:
    normalized_text = normalized_text.replace(s, s.capitalize())  # Each sentence will start with a capital letter

last_words = re.findall(r'(\b\w+)\.', normalized_text)  # Finding the last words in sentences
last_sentence = ' '.join(last_words).capitalize()  # Creating a sentence from the last words of each sentence
last_sentence += '.'
normalized_text += ' ' + last_sentence

clear_text = normalized_text.replace(' iz ', ' is ')  # Replacing all “iz” with correct “is”, but only when it is a mistake

final_text = re.sub(r'(\w)(“)', r'\1 \2', clear_text)  # Fix missing space before "iz"

spaces_number = len(re.findall(r'\s', final_text))  # Finding the number of spaces

print(final_text)
print('Number of spaces =', spaces_number)

