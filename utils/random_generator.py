from random import randint, seed, choice

upper_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
symbol = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]
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


@staticmethod
def generate_pwd(pwd_len=16, num_letters=8, num_nums=4, num_symbols=4):
    # set character counters, seed
    numbers = 0
    letters = 0
    symbols = 0
    # list will store generated characters
    generated_pwd_list = []
    while (numbers + letters + symbols) < pwd_len:
        character_type = get_next_type(character_types)
        # check character type and counter requirements
        if character_type == 'letter' and letters < num_letters:
            # generate random letter, increment count
            letter = generate_letter()
            generated_pwd_list.append(letter)
            letters += 1
        # check character type and counter requirements
        if character_type == 'number' and numbers < num_nums:
            # generate random number, increment count
            number = generate_number()
            generated_pwd_list.append(number)
            numbers += 1
        # check character type and counter requirements
        if character_type == 'symbol' and symbols < num_symbols:
            # generate random symbol, increment count
            symbol = generate_symbol()
            generated_pwd_list.append(symbol)
            symbols += 1
    return "".join(generated_pwd_list)


def generate_letter():
    # decide if letter will be upper/lower
    upper = randint(0, 1)
    # return random upper/lower letter choice
    if upper == 0:
        return choice(upper_letters).lower()
    else:
        return choice(upper_letters)


def generate_letters(num_letters):
    # initialize empty generated_string
    generated_string = ""
    # add num_letters random letters to generated_string
    for n in range(num_letters):
        generated_string += generate_letter()
    return generated_string


def generate_number():
    # randomly choose a number, convert to string
    return str(randint(0, 9))


def generate_numbers(num_numbers):
    # initialize empty generated_numbers
    generated_numbers = ""
    # add num_numbers random numbers to generated_numbers
    for n in range(num_numbers):
        generated_numbers += generate_number()
    return generated_numbers


def generate_symbol():
    # return random symbol choice
    return choice(symbol)


def get_next_type(type_list):
    # randomly choose from type_list
    return choice(type_list)
