from random import randint, seed, random


@staticmethod
def generateId(self):
    seed(1)
    generatedId = None
    # generate id in 00000xxx format
    # for number in range(5):
    #     generatedId += randint(0, 9)
    # for letter in range(3):
    #     generatedId += chr(randint(1, 26)
    # return generatedId
    generatedId = generate_numbers(5, 0, 9)
    generatedId += generate_letters(3, 1, 26)
    return generatedId

@staticmethod
def generate_pwd(pwd_len, num_letters, num_nums, num_symbols):
    numbers = 0
    letters = 0
    symbols = 0
    generated_pwd = None
    try:
        for number in pwd_len:
            type = get_next_type(['letter', 'number', 'symbol'])
            seed(1)
            if type == 'letter' and num_letters > 0:
                if letters < num_letters:
                    generated_pwd += chr(randint(1, 26))
                    letters += 1
            if type == 'number' and num_nums > 0:
                if numbers < num_nums:
                    generated_pwd += randint(0, 9)
                    numbers += 1
            if type == 'symbol' and num_symbols > 0:
                if symbols < num_symbols:
                    generated_pwd += chr(randint(33, 63))
                    symbols += 1
    except Exception as err:
        print(err)
        raise


def generate_letters(num_letters, min_letter, max_letter):
    generated_str = None
    for letter in range(num_letters):
        generated_str += chr(min_letter, max_letter)
    return generated_str


def generate_numbers(length, min_digit, max_digit):
    generated_str = None
    for number in range(length):
        generated_str += randint(min_digit, max_digit)
    return generated_str


def get_next_type(list):
    return random.choices(list)
