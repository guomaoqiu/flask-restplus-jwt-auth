#!/bin/bash
# @Author: Green
# @Date:   2018-08-18 21:44:27
# @Last Modified by:   guomaoqiu
# @Last Modified time: 2019-09-24 18:27:47
curl -H "Content-Type: application/json" --data '{"username":"user1","password":"123.com", "email":"user1@qq.com"}' http://127.0.0.1:5000/api/v1/auth/register
curl -H "Content-Type: application/json" --data '{"username":"user2","password":"123.com", "email":"user2@qq.com"}' http://127.0.0.1:5000/api/v1/auth/register
curl -H "Content-Type: application/json" --data '{"username":"user3","password":"123.com", "email":"user3@qq.com"}' http://127.0.0.1:5000/api/v1/auth/register
curl -H "Content-Type: application/json" --data '{"username":"user4","password":"123.com", "email":"user4@qq.com"}' http://127.0.0.1:5000/api/v1/auth/register
curl -H "Content-Type: application/json" --data '{"username":"user5","password":"123.com", "email":"user5@qq.com"}' http://127.0.0.1:5000/api/v1/auth/register
curl -H "Content-Type: application/json" --data '{"username":"user6","password":"123.com", "email":"user6@qq.com"}' http://127.0.0.1:5000/api/v1/auth/register
curl -H "Content-Type: application/json" --data '{"username":"user7","password":"123.com", "email":"user7@qq.com"}' http://127.0.0.1:5000/api/v1/auth/register
curl -H "Content-Type: application/json" --data '{"username":"user8","password":"123.com", "email":"user8@qq.com"}' http://127.0.0.1:5000/api/v1/auth/register
curl -H "Content-Type: application/json" --data '{"username":"user9","password":"123.com", "email":"user9@qq.com"}' http://127.0.0.1:5000/api/v1/auth/register
curl -H "Content-Type: application/json" --data '{"username":"user10","password":"123.com", "email":"user10@qq.com"}' http://127.0.0.1:5000/api/v1/auth/register
curl -H "Content-Type: application/json" --data '{"username":"admin","password":"123.com", "email":"admin@qq.com"}' http://127.0.0.1:5000/api/v1/auth/register
curl -H "Content-Type: application/json" --data '{"username":"guomaoqiu","password":"123.com", "email":"guomaoqiu@sina.com"}' http://127.0.0.1:5000/api/v1/auth/register

mysql -uroot -p123.com -e "use restapi; update user set is_active = 1"
