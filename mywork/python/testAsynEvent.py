import fnmatch

import salt.config
import salt.utils.event
import salt.client

time = 0
opts = salt.config.client_config('/home/test6/salt_dev_env/etc/salt/master')
local = salt.client.LocalClient('/home/test6/salt_dev_env/etc/salt/master')

sevent = salt.utils.event.get_event(
        'master',
        sock_dir=opts['sock_dir'],
        transport=opts['transport'],
        opts=opts)

m1jid0 = local.cmd_async('saltdev', 'cmd.run', ['sleep 3'])
print "(2) saltdev cmd.run a error command!!!"
print "jid:"+m1jid0
if (m1jid0 == 0):
  print "failed!!!"

time+=1

m2jid0 = local.cmd_async('ubuntu', 'test.sleep', [2])
print "(3) ubuntu test.sleep 3"
print "jid:"+m2jid0
if (m2jid0 == 0):
  print "failed!!!"

time+=1

m1jid1 = 0
m1jid2 = 0
m2jid1 = 0

while True:
  ret = sevent.get_event(full=True)
  if ret is None:
     print "ret none"
     continue

  if fnmatch.fnmatch(ret['tag'], 'salt/job/*/ret/*'):
    print ret['tag']
    print ret['data']
    time-=1
    if (ret['data']['jid']==m1jid0):
      m1jid1 = local.cmd_async('saltdev', 'test.sleep', [2])
      time+=1

    if (ret['data']['jid']==m1jid1):
      m1jid2 = local.cmd_async('saltdev', 'test.ping')
      time+=1

    if (m2jid0 == ret['data']['jid']):
      m2jdi1 = local.cmd_async('ubuntu', 'cmd.run', ['sleep 2'])
      time+=1

    print time

    if(0 == time):
      print "---------all finished!!!-----------"
      break
