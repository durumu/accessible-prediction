from collections import defaultdict
from string import ascii_lowercase

MAX_LOOKBACK = 4
LEARN_RATE = 0.05

wiki_counts = defaultdict(lambda: [0] * 27)
user_counts = defaultdict(lambda: [0] * 27)


def index(letter):
    if letter.isalpha():
        return ord(letter) - ord('a')
    else:
        return 26


def priority(prediction, next_letter):
    wiki_count = wiki_counts[prediction][index(next_letter)]
    user_count = user_counts[prediction][index(next_letter)]
    return max(wiki_count, 1) * (1 + LEARN_RATE * user_count ** 1.5)


def next_by_priority(prefix):
    if len(prefix) > MAX_LOOKBACK:
        prefix = prefix[-MAX_LOOKBACK:]

    letters = ascii_lowercase + '_'

    def sort_key(letter):
        return [priority(prefix[start:], letter) for start in range(len(prefix))]

    return sorted(letters, key=sort_key, reverse=True)


def initialize_wiki_counts():
    with open('freqs.dat') as f:
        for line in f:
            word, count = line.split('|')
            count = int(count)  # we do nothing with count right now
            prefix, next_letter = word[:-1], word[-1]
            wiki_counts[prefix][index(next_letter)] = count


def update_user_counts(history):
    for lookback in range(1, MAX_LOOKBACK):
        prefix = ''.join(history[-lookback - 1:-1])
        user_counts[prefix][index(history[-1])] += 1


"""def main():
    initialize_wiki_counts()

    history = [' ']

    while True:
        lookback = min(MAX_LOOKBACK, len(history))

        recent = ''.join(history[-lookback:])
        print(''.join(next_by_priority(recent)))

        inputted_character = input()[0]
        history.append(inputted_character)
        
        update_user_counts(history)"""


def predictions(history):
    lookback = min(MAX_LOOKBACK, len(history))

    recent = ''.join(history[-lookback:])
    update_user_counts(history)
    return next_by_priority(recent)


initialize_wiki_counts()
