#!/usr/bin/env python3

import csv


def pad_to(unpadded, target_len):
    """
    Pad a string to the target length in characters, or return the original
    string if it's longer than the target length.
    """
    under = target_len - len(unpadded)
    if under <= 0:
        return unpadded
    return unpadded + (' ' * under)


def md_table(table, *, padding=1, divider='|', header_div='-'):
    """
    Convert a 2D array of items into a Markdown table.
    padding: the number of padding spaces on either side of each divider
    divider: the vertical divider to place between columns
    header_div: the horizontal divider to place between the header row and
        body cells
    """
    # Output data buffer
    output = ''
    # Pad short rows to the length of the longest row to fix issues with
    # rendering "jagged" CSV files
    longest_row_len = max([len(row) for row in table])
    for row in table:
        while len(row) < longest_row_len:
            row.append('')
    # Get max length of any cell for each column
    col_sizes = [max(map(len, col)) for col in zip(*table)]
    # Set up the horizontal header dividers
    header_divs = [None] * len(col_sizes)
    num_cols = len(col_sizes)
    # Pad header divs to the column size
    for cell_num in range(num_cols):
        header_divs[cell_num] = header_div * (col_sizes[cell_num] +
                                              padding * 2)
    # Trim first and last padding chars, if they exist
    if padding > 0:
        header_div_row = divider.join(header_divs)[padding:-padding]
    else:
        header_div_row = divider.join(header_divs)
    # Pad each cell to the column size
    for row in table:
        for cell_num, cell in enumerate(row):
            row[cell_num] = pad_to(cell, col_sizes[cell_num])
    # Split out the header from the body
    header = table[0]
    body = table[1:]
    # Build the inter-column dividers using the padding settings above
    multipad = ' ' * padding
    divider = multipad + divider + multipad
    output += divider.join(header) + '\n'
    output += header_div_row + '\n'
    for row in body:
        output += divider.join(row) + '\n'
    # Strip the last newline
    if output.endswith('\n'):
        output = output[:-1]
    return output


def main():
    f = open('openbugs.csv', 'rU')
    csv_reader = csv.reader(f)

    header_row = list(csv_reader.__next__())
    header_row.append('Total')

    table = []
    for row in csv_reader:
        row.append(str(sum(map(int, row[1:]))))
        table.append(row)

    table.sort(key=lambda x: int(x[-1]), reverse=True)

    #total_row = list(map(lambda *args: str(sum(map(lambda s: int(s) if s.isnumeric() else 0, args))), *table))
    #total_row = list(map(lambda x: str(sum(map(lambda s: int(s) if s.isnumeric() else 0, x))), zip(*table)))
    #total_row = list(map(lambda x: str(sum(map(int, x))), list(zip(*table))[1:]))
    total_row = [str(sum(map(int, x))) for x in list(zip(*table))[1:]]
    total_row.insert(0, 'Total')

    table.insert(0, header_row)
    table.append(total_row)

    print(md_table(table))

if __name__ == '__main__':
    main()