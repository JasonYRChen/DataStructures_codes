def shift(pattern):
    result = [0] * len(pattern)
    if len(pattern) > 1:
        for i, char in enumerate(pattern[1:], 1):
            if char == pattern[result[i-1]]:
                result[i] = result[i-1] + 1
    return result


def knuth_morris_pratt(text, pattern):
    shift_table = shift(pattern)
    i_t = i_p = 0

    while i_t < len(text) and len(pattern):
        if text[i_t] == pattern[i_p]:
            if i_p == len(pattern) - 1:
                return i_t - i_p
            i_t += 1
            i_p += 1
        elif i_p == 0:
            i_t += 1
        else:
            i_p = shift_table[i_p - 1]
    return -1 if len(pattern) else 0


t = 'baaab'
p = 'ab'
# p = 'susasusadds'
print(knuth_morris_pratt(t, p))
# print(shift(p))
