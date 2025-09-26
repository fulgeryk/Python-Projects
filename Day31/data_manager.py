import pandas
import random
class DataManager:
    def __init__(self):
        try:
            self.data = pandas.read_csv("./data/words_to_learn.csv")
        except FileNotFoundError:
            self.data = pandas.read_csv("./data/french_words.csv")
        finally:
            self.word = self.data.to_dict(orient="records")
            self.save_random_dict = ""

    def choice_word(self):
        try:
            self.save_random_dict = random.choice(self.word)
        except IndexError:
            return None
        else:
            return self.save_random_dict

    def remove_word(self):
        self.word.remove(self.save_random_dict)

    def save_progress(self):
        data_to_save = pandas.DataFrame(self.word)
        data_to_save.to_csv("./data/words_to_learn.csv", index= False)

