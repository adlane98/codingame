if __name__ == '__main__':

    magic_phrase = input()
    pattern_dict = {}

    for len_subs in range(1, int(len(magic_phrase) / 2) + 1):
        pattern = magic_phrase[:len_subs]
        if " " in pattern:
            break

        for first_index_next_subs in range(len_subs, len(magic_phrase), len_subs):
            if pattern == magic_phrase[first_index_next_subs:first_index_next_subs+len_subs]:
                pattern_count = pattern_dict.get(pattern, 1)
                pattern_dict[pattern] = pattern_count + 1
            else:
                break

    print(pattern_dict)