#!/usr/bin/env python3

##########################
###### Installation ######
# $ pip3 install pyenchant
#
##########################
### Changes to be made ###
# Look for `change this` in this file
# and update the values before running
##########################

import subprocess
import itertools
import enchant

english_dict = enchant.Dict("en_US")

binary_path = './main' # change this
file_path = './passwd' # change this
letters = list('abcdefghijklmnopqrstuvwxyz')

# function returns meaningful english words formed from a list
# of letters
def find_english_words(letters):
    letters_permutations = list(itertools.permutations(letters))
    word_list = []
    
    for letters_permutation in letters_permutations:
        possible_word = ''.join(letters_permutation)

        if english_dict.check(possible_word):
            word_list.append(possible_word)
    
    return word_list

password_letters = []

# find out all letters in the password using the binary
for letter in letters:
    output = subprocess.run(['sudo', binary_path, file_path, letter], stdout=subprocess.PIPE)
    # print("{}: {}".format(letter, output.stdout.decode('utf-8').strip()))

    if output.stdout.decode('utf-8').strip() == '1':
        password_letters.append(letter)

# print(password_letters)

# find out all unique combinations of the letters
all_combinations = list(itertools.combinations(password_letters, 4))
unique_letters_combinations = list(set(all_combinations))

# iterate through the combinations to find meaningful passwords
for unique_letters_combination in unique_letters_combinations:
    
    # find all `word_1` meaningful english words
    word_1_list = find_english_words(unique_letters_combination)
    
    # find all `word_2` meaningful english words
    word_2_letters = list(set(password_letters) - set(unique_letters_combination))
    word_2_list = find_english_words(word_2_letters)

    # permute between `word_1` and `word_2` lists
    possible_password_list = list(itertools.product(word_1_list, word_2_list))
    
    for possible_password in possible_password_list:
        print("{}-{}".format(possible_password[0], possible_password[1]))
