import fnmatch
import salt.config
import salt.utils.event
import salt.client
import sys
import re
import ConfigParser
import time

'''
read ini file
'''
def ConfigSectionMap(Config, section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
    
'''
get sub string start with start_str,end with end_str of content
'''
def get_middle_str(content,start_str,end_str):
  start_index = content.index(start_str)
  if start_index>=0:
    start_index += len(start_str)
  end_index = content.index(end_str)
  return content[start_index:end_index]

'''
send command to minion named with minion_name
cmd:commad,forexample cmd.run
param:param for cmd
return ret
'''
def send_cmd(local, sevent, minion_name, cmd, param, has_param=True):
  if(has_param == False):
    mjid = local.cmd_async(minion_name, cmd)
  else:
    mjid = local.cmd_async(minion_name, cmd, [param])
    
  #wait for event
  wait_time = 0
  while True:
    ret = sevent.get_event(full=True)
    #no event
    if ret is None:
       print "ret none"
       wait_time+=1
       if (wait_time > 10):
         return ("", "")
       else:
         continue

    if fnmatch.fnmatch(ret['tag'], 'salt/job/'+mjid+'/ret/'+minion_name):
      ret_data = ret['data']['return']
      if(ret['data'].has_key('success')):
        if(ret['data']['success'] == False):
          ret_code = -1
        else:
          ret_code = 0
      else:
        ret_code = ret['data']['retcode']
      return (ret_code, ret_data)


def send_cmd_no_param(local, sevent, minion_name, cmd):
  return send_cmd(local, sevent, minion_name, cmd, '', False)
  
'''
set minion ip
'''      
def set_minion_ip(local, sevent, minion_name, ip):
  param = 'netsh interface ip set address name="Local" source=static addr='+ ip +' mask=255.255.255.0 none'
  ret_code, ret_data = send_cmd(local, sevent, minion_name, 'cmd.run', param)
  return (ret_code, ret_data)
  
def write_client_config_file(local, sevent, minion_name, file_name, line_list):
  cmd = ""
  for line in line_list:
    if(cmd != ""):
    	cmd += ' & '
    else:
      cmd += '( '
    cmd += ('echo ' + line)
  cmd += (' ) > ' + file_name)
  print cmd
  ret_code, ret_data = send_cmd(local, sevent, minion_name, 'cmd.run', cmd)
  if(ret_code != 0):
    print 'error:write config '+ file_name + ' failed,code-'+str(ret_code) + ',data-' + ret_data
    return -1
  return 0
  
def kill_minion_process(local, sevent, minion_name, process_name):
  cmd = 'taskkill /f /im '+ process_name
  ret_code, ret_data = send_cmd(local, sevent, minion_name, 'cmd.run', cmd)
  if(ret_code != 0):
    print 'error:kill process '+ process_name + ' failed,code-'+str(ret_code) + ',data-' + ret_data
    return -1
  return 0
  
def start_minion_process(local, sevent, minion_name, process_folder, exe_name):
  cmd = 'START /normal /D "' + process_folder + '" ' + exe_name
  ret_code, ret_data = send_cmd(local, sevent, minion_name, 'cmd.run', cmd)
  if(ret_code != 0):
    print 'error:kill process '+ process_folder + ' failed,code-'+str(ret_code) + ',data-' + ret_data
    return -1
  return 0
  
def clean_files(local, sevent, minion_name, rm_cmd):
  ret_code, ret_data = send_cmd(local, sevent, minion_name, 'cmd.run', rm_cmd)
  if(ret_code != 0):
    print 'clean files '+ process_name + ' failed,code-'+str(ret_code) + ',data-' + ret_data
    return -1
  return 0
      
def main_exec(salt_path, config_file, minion_name):
  opts = salt.config.client_config(salt_path+'/etc/salt/master')
  local = salt.client.LocalClient(salt_path+'/etc/salt/master')
  sevent = salt.utils.event.get_event(
        'master',
        sock_dir=opts['sock_dir'],
        transport=opts['transport'],
        opts=opts)

  #get mac of minion
  ret_code, ret_data = send_cmd(local, sevent, minion_name, 'cmd.run', 'GETMAC /s localhost')
  if(ret_code == 0):
    mac = get_middle_str(ret_data, '{', '}')
  else:
    print 'get mac error: code-'+str(ret_code) + ',data-' + ret_data
    return -1;
  
  config = ConfigParser.ConfigParser()
  config.read(config_file) 
  
  ip_from_ini = ConfigSectionMap(config, mac)['ip']#read ip from ini file
  #get ip
  ret_code, ret_data = send_cmd_no_param(local, sevent, minion_name, 'network.ip_addrs')
  if(ret_code == 0):
    if(ip_from_ini not in ret_data):
      ret_code, ret_data = set_minion_ip(local, sevent, minion_name, ip_from_ini)
      if (ret_code != 0):
        print 'set ip error: code-'+str(ret_code) + ',data-' + ret_data
        return -1
  else:
    print 'get ip error: code-'+str(ret_code) + ',data-' + ret_data
    return -1;
    
  #hostname
  hostname_from_ini = ConfigSectionMap(config, mac)['hostname']
  ret_code, ret_data = send_cmd(local, sevent, minion_name, 'cmd.run', 'hostname')
  if(ret_code == 0):
    if(ret_data != hostname_from_ini):
      hostname_cmd = 'wmic computersystem where name="'+ret_data+'" call rename name="'+hostname_from_ini+'"'
      print hostname_cmd
      ret_code, ret_data = send_cmd(local, sevent, minion_name, 'cmd.run', hostname_cmd)
      if(ret_code != 0):
        print 'set hostname error: code-'+str(ret_code) + ',data-' + ret_data
        return -1
      else:
        local.cmd(minion_name, 'system.reboot', expr_form='list')
        return 0
  else:
    print 'get hostname error: code-'+str(ret_code) + ',data-' + ret_data
    return -1
    
  #kill process
  kill_minion_process(local, sevent, minion_name, 'client.exe')
  
  #clean files
  clean_files(local, sevent, minion_name, 'del /S C:/test/*.reg')
  
  #client config file
  write_client_config_file(local, sevent, minion_name, 'C:/test.txt', ['server=127.0.0.1', 'port=100'])
  
  start_minion_process(local, sevent, minion_name, 'C:\\test\\', 'test.bat');
  return 0

if __name__=="__main__": 
  count = 0
  if(len(sys.argv)>=2):
    minion_name = str(sys.argv[1])
    while True:
      if(0 == main_exec('/home/test6/salt_dev_env/', '/home/test6/config.ini', minion_name)):
        break
      count += 1
      if(count>3):
        break
      time.sleep(10);
  else:
    print 'please input salt id'
