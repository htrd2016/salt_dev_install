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
def configSectionMap(Config, section):
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
def set_minion_ip(local, sevent, minion_name, ip, mask, gateway, name='Local'):
  if(gateway.strip()==''):
    gateway = 'none'
  else:
    gateway = 'gateway='+gateway+' gwmetric=1'
  param = 'netsh interface ip set address name="'+name+'" source=static addr='+ ip +' mask='+mask+' ' + gateway
  ret_code, ret_data = send_cmd(local, sevent, minion_name, 'cmd.run', param)
  return (ret_code, ret_data)
  
def set_minion_dns(local, sevent, minion_name, dns, name='Local'):
  if(dns.strip()==''):
    dns = 'none'
  param = 'netsh interface IP set dns "'+name+'" static ' + dns
  ret_code, ret_data = send_cmd(local, sevent, minion_name, 'cmd.run', param)
  return (ret_code, ret_data)

def minion_write_client_config_file(local, sevent, minion_name, file_name, line_list):
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

def minion_process_exist(local, sevent, minion_name, exe_name):
  cmd = 'tasklist|find /i "'+ exe_name +'"'
  ret_code, ret_data = send_cmd(local, sevent, minion_name, 'cmd.run', cmd)
  if(ret_code != 0):
    print 'error:kill process '+ process_folder + ' failed,code-'+str(ret_code) + ',data-' + ret_data
    return -1
  else:
    if(ret_data == ''):
      return 0
    else:
     return 1
   
def minion_kill_process(local, sevent, minion_name, process_name):
  if (0 == minion_process_exist(local, sevent, minion_name, process_name)):
      return 0
  cmd = 'taskkill /f /im '+ process_name
  ret_code, ret_data = send_cmd(local, sevent, minion_name, 'cmd.run', cmd)
  if(ret_code != 0):
    print 'error:kill process '+ process_name + ' failed,code-'+str(ret_code) + ',data-' + ret_data
    return -1
  else:
    if (0 == minion_process_exist(local, sevent, minion_name, process_name)):
      return 0
    else:
      print 'error:kill process '+ process_name + 'failed!!'
  return -1
  
def minion_start_process(local, sevent, minion_name, process_folder, exe_name):
  cmd = 'START /normal /D "' + process_folder + '" ' + exe_name
  ret_code, ret_data = send_cmd(local, sevent, minion_name, 'cmd.run', cmd)
  if(ret_code != 0):
    print 'error:kill process '+ process_folder + ' failed,code-'+str(ret_code) + ',data-' + ret_data
    return -1
  return 0
  
def minion_windows_cmd(local, sevent, minion_name, cmd):
  ret_code, ret_data = send_cmd(local, sevent, minion_name, 'cmd.run', cmd)
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
    list_data = ret_data.split('\r\n')
    mac = list_data[len(list_data)-1]
    mac = mac[0:17]
    mac = mac.replace('-', '')
    print mac
    if(mac == ''):
      print 'parse mac error: code-'+str(ret_code) + ',data-' + ret_data
      return -1
  else:
    print 'get mac error: code-'+str(ret_code) + ',data-' + ret_data
    return -1
  
  config = ConfigParser.ConfigParser()
  config.read(config_file) 
  
  ip_from_ini = configSectionMap(config, mac)['ip']
  mask_from_ini = configSectionMap(config, mac)['mask']
  gateway_from_ini = configSectionMap(config, mac)['gateway']
  #get ip
  ret_code, ret_data = send_cmd_no_param(local, sevent, minion_name, 'network.ip_addrs')
  if(ret_code == 0):
    if(ip_from_ini not in ret_data):
      ret_code, ret_data = set_minion_ip(local, sevent, minion_name, ip_from_ini, mask_from_ini, gateway_from_ini)
      if (ret_code != 0):
        print 'set ip error: code-'+str(ret_code) + ',data-' + ret_data
        return -1
  else:
    print 'get ip error: code-'+str(ret_code) + ',data-' + ret_data
    return -1
    
  #dns
  dns_from_ini = configSectionMap(config, mac)['dns']
  ret_code, ret_data = set_minion_dns(local, sevent, minion_name, dns_from_ini)
  if (ret_code != 0):
    print 'set ip error: code-'+str(ret_code) + ',data-' + ret_data
    return -1
    
  #hostname
  hostname_from_ini = configSectionMap(config, mac)['hostname']
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
    
  if (0 != minion_kill_process(local, sevent, minion_name, 'Guardian.exe')):
    print 'kill Guardian.exe faild!!!'
    return -1
    
  #kill process
  if (0 != minion_kill_process(local, sevent, minion_name, 'Client.exe')):
    print 'kill Client.exe faild!!!'
    return -1
   
  hongt_app_path = 'C:\\hongt\\'
  server_ip = configSectionMap(config, 'Main')['host']
  server_port = configSectionMap(config, 'Main')['port']
  to_run_app_count = configSectionMap(config, mac)['to_run_app_count']
  
  #clean files
  minion_windows_cmd(local, sevent, minion_name, 'del /S C:/test/client.run')
  minion_windows_cmd(local, sevent, minion_name, 'del /S C:/test/*.reg')
  
  #write client config file
  minion_client_config = ['[Home]', 'AutoRun=1', '[Main]', 'Host='+server_ip, 'Port='+server_port, 'Bind='+ip_from_ini,
  '[Login]', 'Enable=0', 'Manually=0', 'DomainName=', 'UserName=', 'Lock=0', '[File]', 'BackUp=0',
  'Tactics=0', 'FilePath=', 'FileSize=', 'FileExt=', 'FilePathEx']
  minion_write_client_config_file(local, sevent, minion_name, hongt_app_path+'WebConfig.ini', minion_client_config)
  
  client_folders = ['Client01', 'Client02', 'Client03', 'Client04', 'Client05', 'Client06', 'Client07', 'Client08', 'Client09', 'Client10']
  count = 0
  for folder in client_folders:
    client_folder = hongt_app_path + folder
    # del /f /s /q 
    del_client_file_cmd = 'del /f /s /q ' + client_folder
    #remove folder
    minion_windows_cmd(local, sevent, minion_name, del_client_file_cmd)
    #create dir
    minion_windows_cmd(local, sevent, minion_name, 'md '+ hongt_app_path + folder)
    #copy config file
    minion_windows_cmd(local, sevent, minion_name, 'copy /y ' + hongt_app_path + 'WebConfig.ini ' + client_folder + '\\WebConfig.ini')
    #copy client.exe
    minion_windows_cmd(local, sevent, minion_name, 'copy /y ' + hongt_app_path + 'Client.exe ' + client_folder + '\\Client.exe')
    #start process
    minion_start_process(local, sevent, minion_name, client_folder, 'Client.exe')
    count+=1
    print count
    print to_run_app_count
    if(count>=int(to_run_app_count)):
      break;
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
