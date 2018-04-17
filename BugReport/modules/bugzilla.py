import cookielib
import urllib
import urllib2
from modules import team

username = 'allen.han@cloudminds.com'
password = '123456'

url_head = 'http://bugzilla.smartwireless.cn:9998/report.cgi?'
url_tail = '&width=1024&height=600&action=wrap&ctype=csv&format=table'

all_open = 'bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&resolution=---'
all_fixed = 'bug_status=RESOLVED&bug_status=VERIFIED&bug_status=CLOSED&resolution=FIXED'
today_fixed = all_fixed + '&chfield=resolution&chfieldfrom=-0ds&chfieldto=Now&chfieldvalue=FIXED'

email_cloudminds = '&email1=cloudminds&emailassigned_to1=1&emailtype1=substring'
email_team = ('&email1=' + '%2C%20'.join(team.members.keys()).replace('@', '%40') +
              '&emailassigned_to1=1&emailtype1=exact')

assigned_to = "assigned_to"
component = "component"
bug_severity = "bug_severity"
target_milestone = "target_milestone"

url_all_open_by_owner = (url_head + all_open + email_team +
                     '&x_axis_field=' + bug_severity + '&y_axis_field=' + assigned_to + url_tail)

url_today_fixed_by_owner = (url_head + today_fixed + email_team +
                     '&x_axis_field=' + bug_severity + '&y_axis_field=' + assigned_to + url_tail)

url_all_open_by_component = (url_head + all_open + email_team +
                     '&x_axis_field=' + bug_severity + '&y_axis_field=' + component + url_tail)

url_today_fixed_by_component = (url_head + today_fixed + email_team +
                     '&x_axis_field=' + bug_severity + '&y_axis_field=' + component + url_tail)

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

login_data = urllib.urlencode({'Bugzilla_login' : username, 'Bugzilla_password' : password})
opener.open('http://bugzilla.smartwireless.cn:9998/index.cgi', login_data)


def all_open_bugs_by_owner():
    return opener.open(url_all_open_by_owner)


def today_fixed_bugs_by_owner():
    return opener.open(url_today_fixed_by_owner)


def all_open_bugs_by_component():
    return opener.open(url_all_open_by_component)


def today_fixed_bugs_by_component():
    return opener.open(url_today_fixed_by_component)