from collections import deque


def lcs_number(seq1, seq2):
    len1, len2 = len(seq1), len(seq2)
    matrix = [[0] * (len2+1) for _ in range(len1+1)]
    for i, char1 in enumerate(seq1, 1):
        for j, char2 in enumerate(seq2, 1):
            if char1 == char2:
                matrix[i][j] = matrix[i-1][j-1] + 1
            else:
                matrix[i][j] = max(matrix[i][j-1], matrix[i-1][j])
    return matrix


def lcs_string(seq1, seq2, lcs_number):
    temp = deque([[len(seq1), len(seq2), []]])
    result = []
    while temp:
        package = temp.popleft()
        i, j, s_list = package
        if lcs_number[i][j] > 0:
            if seq1[i-1] == seq2[j-1]:
                s_list.append(seq1[i-1])
                to_append = [[i-1, j-1, s_list]]
            elif lcs_number[i-1][j] > lcs_number[i][j-1]:
                to_append = [[i-1, j, s_list]]
            elif lcs_number[i-1][j] < lcs_number[i][j-1]:
                to_append = [[i, j-1, s_list]]
            else:
                s1, s2 = s_list.copy(), s_list.copy()
                to_append = [[i-1, j, s1], [i, j-1, s2]]
            for package in to_append:
                if package not in temp:
                    temp.append(package)
        else:
            result.append(''.join(reversed(package[2])))
    return result


s1 = 'tcaadbez'
s2 = 'cbeadz'
print(lcs_string(s1, s2, lcs_number(s1, s2)))
