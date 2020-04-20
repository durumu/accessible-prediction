import tkinter as tk

from collections import defaultdict
from string import ascii_lowercase

MAX_LOOKBACK = 4
LEARN_RATE = 0.05
ALPH_SIZE = 27
FREQUENCY_FILEPATH = 'freqs.dat'

LONG_DELAY = 1000
SHORT_DELAY = 800


def index(letter):
    if letter.isalpha():
        return ord(letter.lower()) - ord('a')
    else:
        return ALPH_SIZE - 1
    

def initialize_wiki_counts(filepath = FREQUENCY_FILEPATH):
    wiki_counts = defaultdict(lambda: [0] * ALPH_SIZE)
    with open(filepath) as f:
        for line in f:
            word, count = line.split('|')
            count = int(count)  # we do nothing with count right now
            prefix, next_letter = word[:-1], word[-1]
            wiki_counts[prefix][index(next_letter)] = count
    return wiki_counts


class LetterPredictor:
    def __init__(self, max_lookback = MAX_LOOKBACK):
        self.max_lookback = min(max_lookback, MAX_LOOKBACK)
        self.wiki_counts = initialize_wiki_counts()
        self.user_counts = defaultdict(lambda: [0] * ALPH_SIZE)
        self.history = [' ']


    def priority(self, prediction, next_letter):
        wiki_count = self.wiki_counts[prediction][index(next_letter)]
        user_count = self.user_counts[prediction][index(next_letter)]
        return max(wiki_count, 1) * (1 + LEARN_RATE * user_count ** 1.5)


    def update_user_counts(self):
        for lookback in range(1, self.max_lookback):
            prefix = ''.join(self.history[-lookback - 1:-1])
            self.user_counts[prefix][index(self.history[-1])] += 1

    
    def next_by_priority(self):
        lookback = min(self.max_lookback, len(self.history))
        prefix = ''.join(self.history[-lookback:])

        def sort_key(letter):
            return [self.priority(prefix[start:], letter) for start in range(len(prefix))]

        letters = ascii_lowercase + '_'
        return sorted(letters, key=sort_key, reverse=True)


    def add_character(self, character):
        self.history.append(character)
        self.update_user_counts()


class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.predictor = LetterPredictor()

        self.cursor_position = 0

        self.create_widgets()

        self.master.after(LONG_DELAY, self.loop)


    def select_character(self, event):
        priority = self.predictor.next_by_priority()
        character_selected = priority[max(self.cursor_position, 0)]
        if character_selected == '_':
            character_selected = ' '
        
        self.add_typed_character(character_selected)
        self.predictor.add_character(character_selected)
        self.reset_cursor()


    def add_typed_character(self, character):
        self.typed_text.configure(state = "normal")
        self.typed_text.insert("end-2c", character)
        self.typed_text.configure(state = "disabled")


    def reset_cursor(self):
        self.cursor_position = -1
        self.refresh_labels()


    def advance_cursor(self):
        self.cursor_position += 1
        if self.cursor_position >= ALPH_SIZE:
            self.reset_cursor()
        self.refresh_labels()


    def loop(self):
        self.advance_cursor()

        delay = LONG_DELAY if self.cursor_position <= 3 else SHORT_DELAY
        self.master.after(delay, self.loop)


    def refresh_labels(self):
        priority = self.predictor.next_by_priority()
        self.order_label_text.set(''.join(priority))

        cursor_text = [' '] * 27
        cursor_text[max(0, self.cursor_position)] = '^'
        self.cursor_label_text.set(''.join(cursor_text))


    def create_widgets(self):
        self.order_label_text = tk.StringVar()
        self.order_label = tk.Label(
            self.master,
            textvariable = self.order_label_text,
            font = ('Courier', 36),
        )
        self.order_label.pack(side = "top")

        self.cursor_label_text = tk.StringVar()
        self.cursor_label = tk.Label(
            self.master,
            textvariable = self.cursor_label_text,
            font = ('Courier', 36),
        )
        self.cursor_label.pack(side = "top")

        self.typed_text = tk.Text(
            self.master,
            font = ('Courier', 24),
            height = 6,
            width = 40,
            wrap = tk.WORD,
        )
        self.typed_text.pack(side = "top")

        self.typed_text.insert(tk.END, "|")
        self.typed_text.configure(state = "disabled")
        selectbackground = self.typed_text.cget("selectbackground")
        self.typed_text.configure(inactiveselectbackground = selectbackground)

        self.refresh_labels()

<<<<<<< HEAD

def main():
    root = tk.Tk()
    root.title("Text Prediction Prototype")
    app = Application(master = root)
    root.bind("<space>", app.select_character)
    app.mainloop()
=======
def predictions(history):
    lookback = min(MAX_LOOKBACK, len(history))

    recent = ''.join(history[-lookback:])
    update_user_counts(history)
    return next_by_priority(recent)
>>>>>>> 30c7bf0ce45658afa00bf2fced0763f3eef602e5


if __name__ == "__main__":
    main()
