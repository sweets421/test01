# coding=utf-8
from modules.http import HTTP

http = HTTP()
http.post('http://112.74.191.10/inter/HTTP/auth')
http.assertequals('status','200')
http.saveresults('token','retoken')
http.addheaders('token','{retoken}')
http.post('http://112.74.191.10/inter/HTTP/login',d="username=Will&password=123456")
http.assertequals('status','200')
http.saveresults('userid','uid')
http.post('http://112.74.191.10/inter/HTTP/getUserInfo',d="id={uid}")
http.assertequals('status','200')
http.post('http://112.74.191.10/inter/HTTP/logout')
http.assertequals('status','200')
