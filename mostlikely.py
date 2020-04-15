from collections import defaultdict
from string import ascii_lowercase

counts = defaultdict(lambda: [0]*27)

def index(letter):
    if letter.isalpha():
        return ord(letter) - ord('a')
    else:
        return 26

def priority(prefix):
    letters = ascii_lowercase + '_'
    sort_key = {}
    for letter in letters:
        sort_key[letter] = []
        for start in range(0, len(prefix)):
            sort_key[letter].append(counts[prefix[start:]][index(letter)])
    
    sorted_letters = sorted(letters, key = lambda letter : sort_key[letter])
    return sorted_letters[::-1] # reversed


def main():
    with open('freqs.dat') as f:
        for line in f:
            word, count = line.split('|')
            count = int(count) # we do nothing with count right now
            prefix, next_letter = word[:-1], word[-1]
            counts[prefix][index(next_letter)] = count

    MAX_LOOKBACK = 4
    history = [' ']

    while True:
        lookback = min(MAX_LOOKBACK, len(history))
        recent = ''.join(history[-lookback:])
        print(''.join(priority(recent)))
        c = input()[0]
        history.append(c)

if __name__ == "__main__":
    main()