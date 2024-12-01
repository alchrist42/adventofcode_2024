def nbs(data: list[list[any]], row: int, col: int, diag=True, coord=False) -> list | dict:
    """return neigboards values [coordinates]"""
    if coord:
        ans = dict()
    else:
        ans = list()
    if diag:
        shifts = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    else:
        shifts = ((-1, 0), (0, -1), (0, 1), (1, 0))
    for y, x in shifts:
        nrow, ncol = row + y, col + x
        if -1 < nrow < len(data) and -1 < ncol < len(data[0]):
            if coord:
                ans[(nrow, ncol)] = data[nrow][ncol]
            else:
                ans.append(data[nrow][ncol])
    return ans
