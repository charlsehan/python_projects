# coding=utf-8

from jira import JIRA

jira = JIRA(server='http://jira.cloudminds-inc.com', basic_auth=('allen.han', 'allen.han'))


query_open_bugs = 'project = ESW AND 子项目 = "BT Phone" AND issuetype = 缺陷 AND assignee in ({0}) ' \
                  'AND status in (处理中, 待测试, "To Do", "In Progress", 阻塞, 待处理, 重新打开, 监控)'

query_resolved_bugs = 'project = ESW AND 子项目 = "BT Phone" AND issuetype = 缺陷 AND assignee in ({0}) ' \
                      'AND status CHANGED FROM (处理中, 待测试, "To Do", "In Progress", 阻塞, 待处理, 重新打开, 监控, 重复的问题) ' \
                      'to ("工程师已解决问题") DURING (startOfDay(),endOfDay())'

query_new_bugs = 'project = ESW AND 子项目 = "BT Phone" AND issuetype = 缺陷 AND assignee in ({0}) ' \
                  'AND createdDate >= -1d and createdDate <= -0d'


def owner_open_bug_count(owner):
    issues = jira.search_issues(query_open_bugs.format(owner))
    return issues.total


def team_open_bug_count(team_list):
    query = query_open_bugs.format(','.join(team_list))
    #print query
    issues = jira.search_issues(query)
    return issues.total


def owner_resolved_bug_count(owner):
    issues = jira.search_issues(query_resolved_bugs.format(owner))
    return issues.total


def team_resolved_bug_count(team_list):
    query = query_resolved_bugs.format(','.join(team_list))
    #print query
    issues = jira.search_issues(query)
    return issues.total


def team_new_bug_count(team_list):
    query = query_new_bugs.format(','.join(team_list))
    #print query
    issues = jira.search_issues(query)
    return issues.total