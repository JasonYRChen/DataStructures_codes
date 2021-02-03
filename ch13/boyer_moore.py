from collections import defaultdict


def boyer_moore(text, pattern):
    len_t, len_p, anchor_t = len(text), len(pattern), len(pattern) - 1
    if not len_p:
        return 0

    pat_dict = defaultdict(list)
    for i, char in enumerate(pattern):
        pat_dict[char].append(i)

    while anchor_t < len_t:
        for i, char_p in enumerate(pattern[::-1]):
            if text[anchor_t] != char_p:
                break
            anchor_t -= 1
        else:
            return anchor_t + 1

        char_t = text[anchor_t]
        anchor_p = len_p - i - 1
        if char_t in pat_dict:
            for idx in pat_dict[char_t][::-1]:
                if idx < anchor_p:
                    anchor_t += len_p - 1 - idx
                    break
            else:
                anchor_t += len_p - anchor_p
        else:
            anchor_t += len_p
    return -1


t = 'asushisuchi'
p = 'sushi'
print(boyer_moore(t, p))
