def sum_all(matrix):
    return sum(sum(a) for a in matrix)


if __name__ == '__main__':
    a = [list(range(5)), list(range(5, 10)), list(range(10, 15))]
    print(sum_all(a))