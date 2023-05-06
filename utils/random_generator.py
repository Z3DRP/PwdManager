from random import randint, seed, choices, shuffle

# tuples represent the start and end value for ascii numbers
symbols = {
    'symbolGroup1': (32, 47),
    'symbolGroup2': (58, 64),
    'symbolGroup3': (91, 96),
    'symbolGroup4': (123, 126)
}
letters = {
    'upperGroup': (65, 90),
    'lowerGroup': (97, 122)
}
upperGroup = (65, 90)
lowerGroup = (97, 122)


@staticmethod
def generateId():
    seed(1)
    generatedId = None
    # generate id in 00000xxx format
    generatedId = generate_numbers(5)
    generatedId += generate_letters(3)
    return generatedId


@staticmethod
def generate_pwd(pwd_len, num_letters, num_nums, num_symbols):
    try:
        # generate a string for each number of characters concat them then return the shuffled version
        if num_letters + num_nums + num_symbols > pwd_len:
            raise ValueError('The number of characters cannot be greater than the entire password length')
        unShuffledString = generateRandomPassword(num_letters, num_nums, num_symbols)
        generated_pwd = shuffleString(unShuffledString)
        return generated_pwd
    except Exception as err:
        print(err)


def generate_letters(num_letters):
    generated_str = ''
    cases = ['upperGroup', 'lowerGroup']
    for letter in range(num_letters):
        case = choices(cases)[0]
        selectedCase = letters[case]
        generated_str += chr(randint(selectedCase[0], selectedCase[1]))
    return generated_str


def generate_numbers(length):
    generated_str = ''
    for number in range(length):
        generated_str += str(randint(0, 9))
    return generated_str


def generateRandomPassword(num_letters, num_numbers, num_symbols):
    randomString = ''
    cases = ['upperGroup', 'lowerGroup']
    for letter in range(num_letters + 1):
        # randomly get the key for letters dict
        case = choices(cases)[0]
        selectedCase = case
        # the dict will return the number range based on case
        randomString = chr(randint(selectedCase[0], selectedCase[1]))
    # generate the num_numbers
    for number in range(num_numbers + 1):
        randomString += str(randint(0, 9))
    # as above rangeGroups corresponds to keys for symbol dict range will be returned based on key
    rangeGroups = ['symbolGroup1', 'symbolGroup2', 'symbolGroup3', 'symbolGroup4']
    # generate the symbols
    for symbol in range(num_symbols + 1):
        # symbols are spread out over four groups in ascii table
        # randomly select a group and use that as the range
        group = choices(rangeGroups)[0]
        selectedGroup = symbols[group]
        randomString += chr(randint(selectedGroup[0], selectedGroup[1]))
    return randomString


def shuffleString(string):
    shuffledString = ''
    # get a list of the characters in string bc shuffle only works on list
    listOfChars = [character for character in string]
    # shuffle list then create new string and return
    shuffle(listOfChars)
    for char in listOfChars:
        shuffledString += char
    return shuffledString
