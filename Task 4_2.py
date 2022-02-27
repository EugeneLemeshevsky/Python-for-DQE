import random
import string


def generate_list(n):
    """List of random number of dicts (n) with random number of keys (max_dict_len) and values from 0 to 100
    generation """
    res = []
    max_dict_len = len(string.ascii_lowercase)  # Set the max dict length
    for i in range(n):
        dict_len = random.randrange(1, max_dict_len, 1)
        rand_string = ''.join(random.sample(string.ascii_lowercase, dict_len))
        d = {a: random.randrange(0, 101, 1) for a in rand_string}
        res.append(d)
    return res


def dict_with_unique_keys(list_of_dicts):
    return dict.fromkeys(list(set().union(*list_of_dicts)), 0)


def keys_count(list_of_dicts):
    """Dictionary with the count of each key in all dictionaries"""
    count_keys = dict_with_unique_keys(list_of_dicts)
    for k in count_keys:
        count = 0
        for d in list_of_dicts:
            if k in d.keys():
                count += 1
        count_keys[k] = count
    return count_keys



def common_dict(list_of_dicts, count_keys_dict):
    """get generated list of dicts and create one common dict"""
    new_res_dict = dict_with_unique_keys(list_of_dicts)  # Dict with all unique keys from res with 0 values
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


if __name__ == "__main__":
    n = random.randrange(2, 11, 1)  # Generate number of dicts
    res = generate_list(n)
    count_keys = keys_count(res)

    print(common_dict(res, count_keys))
