#!/usr/bin/env python
# coding=utf-8


from modules import build_table
from modules import table2html


def main():
    print '<html><head>'
    print table2html.get_html_style()
    print '</head><body>'

    print '<br><h2>Bug总数</h2>'
    print table2html.table_to_html(build_table.build_summery_table())

    print '<br><h2>按Owner统计</h2>'
    print table2html.table_to_html(build_table.build_owner_table())

    print '<br></body></html>'


if __name__ == '__main__':
    main()
