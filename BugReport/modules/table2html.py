

def get_html_style():
    return ('<style>\n'
            '  table {border-collapse: collapse}\n'
            '  table, td, th {border: 1px solid black}\n'
            '  tr:nth-child(even){background-color: #f2f2f2}\n'
            '  tr:nth-last-child(1){background-color: #c2c2c2}\n'
            '  td:nth-last-child(1){background-color: #c2c2c2}\n'
            '  th {background-color: #505050; color: white}\n'
            '  th, td {padding: 8px}\n'
            '</style>')


def table_to_html(table):
    if not table:
        return ''
    output = '<table>\n'
    output += "<tr><th>" + "</th><th>".join(table[0]) + "</th></tr>\n"
    for row in table[1:]:
        output += "<tr><td>" + "</td><td>".join(row) + "</td></tr>\n"
    output += '</table>'
    return output
