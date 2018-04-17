#!/usr/bin/env python
# coding=utf-8


from modules import bugzilla
from modules import table2md
from modules.csv2table import csv2table


def main():
    print '\n\n#剩余Bug数量'
    print '\n##按Owner统计\n'
    resp = bugzilla.all_open_bugs_by_owner()
    md = table2md.table_to_md(csv2table(resp, count_by_owner=True, zh_name=False))
    print md if md else '0'
    resp.close()

    print '\n##按模块统计\n'
    resp = bugzilla.all_open_bugs_by_component()
    md = table2md.table_to_md(csv2table(resp, count_by_owner=False, zh_name=False))
    print md if md else '0'
    resp.close()

    print '\n\n#今日解决的Bug数量'
    print '\n##按Owner统计\n'
    resp = bugzilla.today_fixed_bugs_by_owner()
    md = table2md.table_to_md(csv2table(resp, count_by_owner=True, zh_name=False))
    print md if md else '0'
    resp.close()

    print '\n##按模块统计\n'
    resp = bugzilla.today_fixed_bugs_by_component()
    md = table2md.table_to_md(csv2table(resp, count_by_owner=False, zh_name=False))
    print md if md else '0'
    resp.close()


if __name__ == '__main__':
    main()
