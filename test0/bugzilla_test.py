import bugzilla

bz = bugzilla.Bugzilla(url="http://bugzilla.smartwireless.cn:9998")
#用户名密码
userinfo = bz.login(user='jack.xiao@cloudminds.com', password='123456')

idlist = [14048, 13386, 13773, 13310, 13768]
bugs = bz.getbugs(idlist)

for bug in bugs:
    print bug.id, bug.component, bug.assigned_to, bug.status, bug.resolution, bug.summary, bug.last_change_time


