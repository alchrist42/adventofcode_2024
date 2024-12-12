DIAG_K = ((1, 1), (1, -1), (-1, -1), (-1, 1))
LINE_K = ((0, 1), (1, 0), (0, -1), (-1, 0))

def nbs(data: list[list[any]], row: int, col: int, line=True, diag=True,  coord=False) -> list | dict:
    """return neigboards values [coordinates]"""
    if coord:
        ans = dict()
    else:
        ans = list()
    if diag and line:
        shifts = DIAG_K + LINE_K
    elif line:
        shifts = LINE_K
    elif diag:
        shifts = DIAG_K
    for y, x in shifts:
        nrow, ncol = row + y, col + x
        if -1 < nrow < len(data) and -1 < ncol < len(data[0]):
            if coord:
                ans[(nrow, ncol)] = data[nrow][ncol]
            else:
                ans.append(data[nrow][ncol])
    return ans
