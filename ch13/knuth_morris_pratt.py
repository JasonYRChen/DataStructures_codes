def shift(pattern):
    start = end = temp_start = idx = 0
    temp_end = 1
    if len(pattern) > 1:
        for i, char in enumerate(pattern[1:], 1):
            if char == pattern[idx]:
                temp_start = i if idx == 0 else temp_start
                temp_end = i + 1 if idx == 0 else temp_end + 1
                idx += 1
            else:
                temp_start = temp_end = idx = 0
            if (temp_end - temp_start) > (end - start):
                start, end = temp_start, temp_end
    return start ,end


def knuth_morris_pratt(text, pattern):
    # start, end = shift(pattern)
    i_t = i_p = 0

    while i_t < len(text):
        if text[i_t] == pattern[i_p]:
            if i_p == len(pattern) - 1:
                return i_t - i_p
            i_t += 1
            i_p += 1
        elif i_p == 0:
            i_t += 1
        else:




# t = 'ssssushishuchi'
# p = 'sushi'
p = 'susasu'
# print(knuth_morris_pratt(t, p))
print(shift(p))
