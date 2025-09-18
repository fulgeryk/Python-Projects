import pandas
nato_phonetic = pandas.read_csv("nato_phonetic_alphabet.csv")

new_dict = {row.letter:row.code for (_, row) in nato_phonetic.iterrows()}
user_input = input("Enter your name: ").upper()
nato_list = [new_dict[n] for n in user_input]
print(nato_list)
