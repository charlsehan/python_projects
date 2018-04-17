import csv
from modules import team


def remove_others(table, members):
    for row in table[1:]:
        if row[0] not in members.keys():
            table.remove(row)


def append_zero(table, members):
    winners = list(zip(*table))[0][1:]
    for person in members.keys():
        if person not in winners:
            zero_row = [person]
            zero_row.extend(['0'] * (len(table[0]) - 1))
            table.append(zero_row)


def email2name(table, members):
    for row in table:
        if row[0] in members.keys():
            row[0] = members[row[0]]


def append_total(table):
    table[0].append('Total')
    for row in table[1:]:
        row.append(str(sum(map(int, row[1:]))))
    table.sort(key=lambda l: int(l[-1]) if str(l[-1]).isdigit() else 999, reverse=True)
#    total_row = list(map(lambda *args: str(sum(map(lambda s: int(s) if s.isnumeric() else 0, args))), *result_table))
#    total_row = list(map(lambda x: str(sum(map(lambda s: int(s) if s.isnumeric() else 0, x))), zip(*result_table)))
#    total_row = list(map(lambda x: str(sum(map(int, x))), list(zip(*result_table))[1:]))
    total_row = [str(sum(map(int, x))) for x in list(zip(*table[1:]))[1:]]
    total_row.insert(0, 'Total')
    table.append(total_row)


def csv2table(resp, count_by_owner=False, zh_name=False):
    table = list(csv.reader(resp))
    if not table:
        return table
    if count_by_owner:
        members = team.members_zh if zh_name else team.members
        remove_others(table, members)
        append_zero(table, members)
        email2name(table, members)
    append_total(table)
    return table
