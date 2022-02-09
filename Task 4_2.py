import random
import string


# List of random number of dicts (n) with random number of keys (max_dict_len) and values from 0 to 100 generation
def generate_list(n, max_dict_len):
    res = []
    for i in range(n):
        dict_len = random.randrange(1, max_dict_len, 1)
        rand_string = ''.join(random.sample(string.ascii_lowercase, dict_len))
        d = {a: random.randrange(0, 101, 1) for a in rand_string}
        res.append(d)
    return res


# Dictionary with the count of each key in all dictionaries
def keys_count(list_of_dicts):
    count_keys = dict.fromkeys(list(set().union(*list_of_dicts)), 0)
    for k in count_keys:
        count = 0
        for d in res:
            if k in d.keys():
                count += 1
        count_keys[k] = count
    return count_keys


# get generated list of dicts and create one common dict
def common_dict(list_of_dicts, count_keys_dict):
    # Dict with all unique keys from res with 0 values
    new_res_dict = dict.fromkeys(list(set().union(*list_of_dicts)), 0)
    changed_keys = {}

    # Creating one common dict with keys and their corresponding max values.
    # Creating one more dict with keys and the number of the dict that contains the max value for this key.
    for i in range(0, len(list_of_dicts), 1):
        for k in list_of_dicts[i].keys():
            if k in new_res_dict.keys():
                if list_of_dicts[i][k] > new_res_dict[k]:
                    new_res_dict[k] = list_of_dicts[i][k]
                    changed_keys[k] = i
            else:
                new_res_dict[k] = list_of_dicts[i][k]

    # Add index to the key if count of keys != 1
    for k in changed_keys.keys():
        if not (count_keys_dict[k] == 1):
            new_k = k + '_' + str(changed_keys[k] + 1)
            new_res_dict[new_k] = new_res_dict[k]
            del new_res_dict[k]
    return new_res_dict


n = random.randrange(2, 11, 1)  # Generate number of dicts
max_dict_len = len(string.ascii_lowercase)  # Set the max dict length
res = generate_list(n, max_dict_len)
count_keys = keys_count(res)

print(common_dict(res, count_keys))
