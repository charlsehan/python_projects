# coding=utf-8

from jira import JIRA

jira = JIRA(server='http://jira.cloudminds-inc.com', basic_auth=('allen.han', 'allen.han'))

query_resolved_bugs = 'project = ESW AND issuetype = 缺陷 AND assignee = {0} ' \
                      'AND status CHANGED FROM (处理中, 待测试, "To Do", "In Progress", 阻塞, 待处理, 重新打开, 监控, 重复的问题) ' \
                      'to ("工程师已解决问题") DURING (startOfDay(-2),endOfDay(-2))'

issues = jira.search_issues('project = ESW AND issuetype = 缺陷 AND assignee = {0} AND '
                            'status CHANGED FROM (处理中, 待测试, "To Do", "In Progress", 阻塞, 待处理, 重新打开, 监控, 重复的问题) '
                            'to ("工程师已解决问题") DURING (startOfDay(-2),endOfDay(-2))'.format('mike.wang'))

print len(issues)

print issues

