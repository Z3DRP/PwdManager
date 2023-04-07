from random import randint, seed

# NOTE: chr takes in unicode points and spits out a character. Unfortunately unicode points are 4 digit codes that include letters, so I am making a list for the different unicode characters wer're going to use to generate stuff.

upper_unicode = [chr(i) for i in range(65, 91)]
lower_unicode = [chr(i) for i in range(97, 123)]
symbol_unicode = [chr(i) for i in range(33, 48)]
character_types = ['letter', 'number', 'symbol']


@staticmethod
def generate_id():
    # set seed to none for random generation each operation
    seed()
    # initialize empty generated_id
    generated_id = ""
    # generate id in 12345abc format
    generated_id += generate_numbers(5)
    generated_id += generate_letters(3)
    return generated_id


# TODO default generator values should be reflected in UI for generation settings
@staticmethod
def generate_pwd(pwd_len=16, num_letters=8, num_nums=4, num_symbols=4):
    # set character counters, seed, and initialize empty password
    numbers = 0
    letters = 0
    symbols = 0
    seed()
    generated_pwd = ""
    try:
        for n in range(pwd_len):
            character_type = get_next_type(character_types)
            
            # check character type and counter requirements
            if character_type == 'letter' and (num_letters > 0 and letters < num_letters):
                # generate random letter
                generated_pwd += generate_letter()
                # increment letters counter
                letters += 1
            
            # check character type and counter requirements
            if character_type == 'number' and (num_nums > 0 and numbers < num_nums):
                # generate random number
                generated_pwd += generate_number()
                # increment numbers counter
                numbers += 1
            
            # check character type and counter requirements
            if character_type == 'symbol' and (num_symbols > 0 and symbols < num_symbols):
                # generate random symbol
                generated_pwd += generate_symbol()
                # increment symbols counter
                symbols += 1
    
    except Exception as err:
        print(err)
        raise
    
    return generated_pwd


def generate_letter():
    # initialize empty generated_letter
    generated_letter = ""
    upper_lower = randint(0, 1)
    # generate a lowercase letter by randomly choosing a character index and passing index to list of lower_unicode
    if upper_lower == 0:
        character_index = randint(0, len(lower_unicode) - 1)
        generated_letter += lower_unicode[character_index]
    # generate an uppercase letter
    else:
        character_index = randint(0, len(upper_unicode) - 1)
        generated_letter += upper_unicode[character_index]
    return generated_letter


def generate_letters(num_letters):
    # initialize empty generated_string
    generated_string = ""
    # add num_letters random letters to generated_string
    for n in range(num_letters):
        generated_string += generate_letter()
    return generated_string


def generate_number():
    # initialize empty generated_number
    generated_number = ""
    # randomly choose a number, convert to string and insert into generated_number
    generated_number += str(randint(0, 9))
    return generated_number


def generate_numbers(num_numbers):
    # initialize empty generated_numbers
    generated_numbers = ""
    # add num_numbers random numbers to generated_numbers
    for n in range(num_numbers):
        generated_numbers += generate_number()
    return generated_numbers


def generate_symbol():
    # initialize empty generated_symbol
    generated_symbol = ""
    # generate a symbol by randomly choosing a character index and passing index to list of symbol_unicode characters.
    character_index = randint(0, len(symbol_unicode) - 1)
    generated_symbol += symbol_unicode[character_index]
    return generated_symbol


def get_next_type(type_list):
    # randomly choose index from type_list
    index = randint(0, len(type_list) - 1)
    # chooses index from type_list
    character_type = type_list[index]
    return character_type


# can run test to see if it works
"""
print("Testing Password Generation...")
test_password = generate_pwd(12, 6, 3, 3)
print("Generated Password: " + test_password)
print("Testing ID Generation...")
print("Generated ID: " + generateId())
"""
