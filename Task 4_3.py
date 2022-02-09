import re

# Normalization of the text
def normalize_text(text, sep_regexp):
    normalized_text = text.lower()
    sentences = re.split(sep_regexp, normalized_text)  # Breaking the text into sentences
    sep = re.findall(sep_regexp, normalized_text)  # Create list for sentence separators
    normalized_text = ''
    for s, p in zip(sentences, sep):
        normalized_text += s.capitalize() + p  # Each sentence will start with a capital letter
    return normalized_text


# Creating a sentence from the last words of each sentence
def add_sentence(text):
    last_words = re.findall(r'(\b\w+)\.', text)  # Finding the last words in sentences
    last_sentence = ' '.join(last_words).capitalize()  # Creating a sentence from the last words of each sentence
    last_sentence += '.'
    text += ' ' + last_sentence
    return text


separators = r'[.|:]\s*'
text = '''homEwork:
	tHis iz your homeWork, copy these Text to variable.

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.'''

normalized_text = normalize_text(text, separators)
add_sentence(normalized_text)

clear_text = normalized_text.replace(' iz ', ' is ')  # Replacing all “iz” with correct “is”, but only when it is a mistake

final_text = re.sub(r'(\w)(“)', r'\1 \2', clear_text)  # Fix missing space before "iz"

spaces_number = len(re.findall(r'\s', text))  # Finding the number of spaces

print(final_text)
print('Number of spaces =', spaces_number)
