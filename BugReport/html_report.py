#!/usr/bin/env python
# coding=utf-8


from modules import bugzilla
from modules import table2html
from modules.csv2table import csv2table


def main():
    print '<html><head>'
    print table2html.get_html_style()
    print '</head><body>'

    print '<br><h2>剩余Bug数量</h2>'
    print '<h3>按Owner统计</h3>'
    resp = bugzilla.all_open_bugs_by_owner()
    html = table2html.table_to_html(csv2table(resp, count_by_owner=True, zh_name=True))
    print html if html else '0'
    resp.close()

    print '<br><h3>按模块统计</h3>'
    resp = bugzilla.all_open_bugs_by_component()
    html = table2html.table_to_html(csv2table(resp, count_by_owner=False, zh_name=True))
    print html if html else '0'
    resp.close()

    print '<br><h2>今日解决的Bug数量</h2>'
    print '<h3>按Owner统计</h3>'
    resp = bugzilla.today_fixed_bugs_by_owner()
    html = table2html.table_to_html(csv2table(resp, count_by_owner=True, zh_name=True))
    print html if html else '0'
    resp.close()

    print '<br><h3>按模块统计</h3>'
    resp = bugzilla.today_fixed_bugs_by_component()
    html = table2html.table_to_html(csv2table(resp, count_by_owner=False, zh_name=True))
    print html if html else '0'
    resp.close()

    print '<br></body></html>'


if __name__ == '__main__':
    main()
