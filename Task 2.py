import random
import string

n = random.randrange(2, 11, 1)  # Generate number of dicts
max_dict_len = len(string.ascii_lowercase)  # Set the max dict length
res = []
# List of random number of dicts (n) with random number of keys (max_dict_len) and values from 0 to 100 generation
for i in range(n):
    dict_len = random.randrange(1, max_dict_len, 1)
    rand_string = ''.join(random.sample(string.ascii_lowercase, dict_len))
    d = {a: random.randrange(0, 101, 1) for a in rand_string}
    res.append(d)

new_res_dict = dict.fromkeys(list(set().union(*res)), 0)  # Dict with all unique keys from res with 0 values
changed_keys = {}

# Dictionary with the count of each key in all dictionaries
count_keys = dict.fromkeys(list(set().union(*res)), 0)
for k in count_keys:
    count = 0
    for d in res:
        if k in d.keys():
            count += 1
    count_keys[k] = count

# Creating one common dict with keys and their corresponding max values.
# Creating one more dict with keys and the number of the dict that contains the max value for this key.
for i in range(0, len(res), 1):
    for k in res[i].keys():
        if k in new_res_dict.keys():
            if res[i][k] > new_res_dict[k]:
                new_res_dict[k] = res[i][k]
                changed_keys[k] = i
        else:
            new_res_dict[k] = res[i][k]

# Add index to the key if count of keys != 1
for k in changed_keys.keys():
    if not (count_keys[k] == 1):
        new_k = k + '_' + str(changed_keys[k] + 1)
        new_res_dict[new_k] = new_res_dict[k]
        del new_res_dict[k]

print(new_res_dict)
