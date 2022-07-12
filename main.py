# Problem 81:
#     Path Sum: Two Ways
#
# Description:
#     In the 5 by 5 matrix below, the minimal path sum from the top left to the bottom right,
#       by only moving to the right and down, is indicated in bold red and is equal to 2427.
#
#         | [131]  673   234   103    18  |
#         | [201] [ 96] [342]  965   150  |
#         |  630   803  [746] [422]  111  |
#         |  537   699   497  [121]  956  |
#         |  805   732   524  [ 37] [331] |
#
#     Find the minimal path sum from the top left to the bottom right by only moving right and down
#       in matrix.txt (right click and "Save Link/Target As..."), a 31K text file containing an 80 by 80 matrix.

from typing import List, Tuple


def main(filename: str) -> Tuple[int, List[str]]:
    """
    Returns the minimal path sum in the given `filename`
      walking from the top-left to the bottom-right of the matrix,
      as well as the path taken, as a list of step directions from {'R', 'D'}.

    Args:
        filename (str): File name containing integer matrix

    Returns:
        (Tuple[int, List[str]]):
            Tuple of ...
              * Minimal path sum walking from top-left to bottom-right in matrix
              * Minimal path represented as a list of steps from {'R', 'D'}

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(filename) == str

    # Idea:
    #     Use dynamic programming to only keep track of minimal subpaths
    #       landing within the matrix and use then use those to further compute longer subpaths.

    with open(filename, 'r') as f:
        m = list(map(lambda line: list(map(int, line.split(','))), f.readlines()))

    # Assume given matrix is square
    n = len(m)

    # Grid to keep track of minimal sub-path sum ending at that coordinate in matrix
    trellis_sum = [[0 for _ in range(n)] for _ in range(n)]
    trellis_sum[0][0] = m[0][0]

    # Grid to keep track of what was the previous point in minimal sub-path ending at current point
    trellis_dir = [['' for _ in range(n)] for _ in range(n)]

    # Fill in trellises by iterating through the diagonals
    for d in range(1, 2*n):  # Diagonals go from bottom-left to top-right (like this: // )
        # Start at bottom-left coordinate of diagonal
        py = min([n-1, d])
        px = max([0, d-(n-1)])

        # Walk along diagonal towards top-right, figuring out minimal sub-paths
        while py >= 0 and px < n:
            curr_elt = m[py][px]

            # Quick checks for edge cases
            if px == 0:  # Left edge of matrix, so only incoming choice is from above
                trellis_dir[py][px] = 'U'
                trellis_sum[py][px] = curr_elt + trellis_sum[py-1][px]
            elif py == 0:  # Upper edge of matrix, so only incoming choice is from left
                trellis_dir[py][px] = 'L'
                trellis_sum[py][px] = curr_elt + trellis_sum[py][px-1]
            else:  # Inside of matrix, so incoming from up and left are both possible
                # Figure out optimal incoming direction
                choices = [(py-1, px, 'U'), (py, px-1, 'L')]
                min_choice = min(choices, key=lambda c: trellis_sum[c[0]][c[1]])
                qy, qx = min_choice[:2]

                # Store in trellises
                trellis_dir[py][px] = min_choice[2]
                trellis_sum[py][px] = curr_elt + trellis_sum[qy][qx]

            py -= 1
            px += 1

    # Walk backwards through trellises, from bottom-right to top-left, enumerating minimal path
    py = px = n-1
    path_sum = trellis_sum[py][px]
    fwd_path = []
    while py > 0 or px > 0:
        if trellis_dir[py][px] == 'L':
            fwd_dir = 'R'
            px -= 1
        else:
            fwd_dir = 'D'
            py -= 1
        fwd_path.append(fwd_dir)
    fwd_path.reverse()
    return path_sum, fwd_path


if __name__ == '__main__':
    matrix_filename = 'matrix.txt'
    minimal_path_sum, minimal_path = main(matrix_filename)
    print('Minimal path sum in "{}":'.format(matrix_filename))
    print('  {}'.format(minimal_path_sum))
    print('Path producing that sum:')
    print('  {}'.format(' -> '.join(minimal_path)))
