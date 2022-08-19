from functools import cache

data = "HHGNHHGNGNRHNTTGHHGNHHGNGNRHNTTGGNRHNTTGRHHHHHGNNTTGTGTGTGTGGNRHUNTTGTGTGTGTGGNRHTGTGGNRHTGTGGNRHTGTGGNRHTGTGGNRHGNRHNTTGRHHHHHGNTGTGGNRHTGTGGNRHGNRHNTTGRHHHHHGNTGTGGNRHTGTGGNRHGNRHNTTGRHHHHHGNORHHHHHGNHHGNHHGNHHGNHHGNGNRHNTTGHHGNHHGNGNRHNTTGHHGNHHGNGNRHNTTGGNRHNTTGRHHHHHGNNTTGTGTGTGTGGNRHRHHHHHGNHHGNHHGNHHGNHHGNGNRHNTTGATGTGGNRHTGTGGNRHGNRHNTTGRHHHHHGNTGTGGNRHTGTGGNRHGNRHNTTGRHHHHHGNHHGNHHGNGNRHNTTGHHGNHHGNGNRHNTTGGNRHNTTGRHHHHHGNNTTGTGTGTGTGGNRHERHHHHHGNHHGNHHGNHHGNHHGNGNRHNTTGHHGNHHGNGNRHNTTGHHGNHHGNGNRHNTTG"

var = "GHNRT"
const = "AIUEO"

one_to_pair = {
    'G': 'GN',
    'R': 'NT',
    'N': 'RH',
    'H': 'TG',
    'T': 'HH'
}

def invert(d : dict):
    return {v: k for k, v in d.items()}

def char_type(c : str) -> bool:
    '''True if c in var, False if c in const'''
    assert c in var or c in const
    return c in var

def squish(streak : list[str], num_iters : int = 6) -> list[str]:
    state = list(streak)
    if len(streak) % 2 == 0:
        for _ in range(num_iters):
            # state = [pair_to_one[''.join(state[index:index + 2])] for index in range(0, len(streak) - 2 + 1, 2)]
            state = [pair_to_one[''.join(pair)] for pair in split_in_pairs(state)]
    return state

def split_in_pairs(seq):
    return [seq[index:index + 2] for index in range(0, len(seq) - 1, 2)]

def flatten(array):
    return [element for subarray in array for element in subarray]

pair_to_one = invert(one_to_pair)

# find streaks of chars of the same type

streaks = []

for index, char in enumerate(data):
    if not streaks or char_type(streaks[-1][0]) != char_type(char):
        # start a new streak
        streaks.append([char])
    elif char_type(streaks[-1][-1]) == char_type(char):
        # continure previous streak
        streaks[-1].append(char)

streaks_joined = list(map(''.join, streaks))

# print(streaks_joined)
# print(list(map(len, streaks_joined)))

print(''.join(flatten(list(map(squish, streaks)))))
