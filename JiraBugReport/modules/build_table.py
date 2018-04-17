# coding=utf-8
from modules import team
from modules import jira_query


def build_summery_table():
    table = []
    head = ["今日新增", "今日解决", "剩余"]
    table.append(head)

    counts = [str(jira_query.team_new_bug_count(team.members_zh.keys())),
              str(jira_query.team_resolved_bug_count(team.members_zh.keys())),
              str(jira_query.team_open_bug_count(team.members_zh.keys()))]
    table.append(counts)
    return table


def build_owner_table():
    table = []
    open_total = 0
    resolve_total = 0

    for owner in team.members_zh:
        open_count = jira_query.owner_open_bug_count(owner)
        resolve_count = jira_query.owner_resolved_bug_count(owner)

        item_list = [team.members_zh[owner], str(open_count), str(resolve_count)]
        table.append(item_list)

        open_total += open_count
        resolve_total += resolve_count

    table.sort(key=lambda l: int(l[-1]), reverse=True)

    table.insert(0,  ["Owner", "剩余", "今日解决"])
    table.append(["总计", str(open_total), str(resolve_total)])
    return table
