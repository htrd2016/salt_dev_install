1.login.sh:登录，并且返回token
2.testping_by_token.sh:通过登录的token发送test.ping命令

3.login_write_cookie.sh:登录，返回token并且将cookie写入~/cookies.txt文件
4.testping_by_cookie.sh:通过读取~/cookies.txt替代token，发送test.ping命令

5.get_all_minion_detail_by_cookie.sh      

6.get_diskuseage_by_cookie.sh             
7.get_job_by_jobid.sh: 把<replace_this_to_your_job_id> 替换为你自己要查询的job id,就可以查询之前job执行结果                    

8.get_saltdev_minion_detail_by_cookie.sh  
9.run_testping_by_username.sh: 通过post用户名和密码的方式通过web的run接口执行test.ping命令，注意：不能通过“X-Auth-Token”否则会提示未授权
             
10.listion_event.sh:监听所有事件
11.listion_event_filter.sh:通过awk显示过滤出的事件信息                 

12.hook_my_event_by_cookie.sh:通过hook接口触发一个自定义事件，事件tag以“salt/netapi/hook”开头

13.hook_mycompany_build.sh:触发事件“hook/mycompany/build/success”

14.fire_event1.sh:触发“hook/web/event/run/event1”,X-Auth-Token:<your log in token>, event1会触发event2
登录获取token:
curl -si localhost:8000/login \
        -H "Accept: application/json" \
        -d username='test6' \
        -d password='test6' \
        -d eauth='pam'

