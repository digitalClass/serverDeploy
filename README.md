# Server Deploy
This is sever deploy for the project of digital classroom which started by 2016 summer school of the USTC of software engeering.

## Introduction
### About digital classroom
Started by i9 on 07/09,2016 aimed at help students in the USTC to learn outside traditional classroom.

### About server deploy
Our group(see below)'s duty is providing the server technology support for this project.

## Team
1. Yunfeng Wang[:octocat:](https://github.com/vra)
2. Zhihua Huang[:octocat:](https://github.com/hzh8311)
3. Yunchong Zhang[:octocat:](https://github.com/Cobbyzhang)

## 工作
1. clone 前端的仓库到项目目录下，在.gitignore中加入`web_page`,这样就能保持模板路径的方便以及git仓库的独立
2. 实现通过网址去访问index.html
3. 实现了登录和注册按钮的初步功能，登录和注册表单还要前端完成
4. 请前端在`templates`里写`users/login.html`和`users/register.html`
5. 尝试写了下courses的模型

## 备注
1. setting.py里包括模板文件的位置,MySQL数据库的配置，语言和市区的设置
2. 用户认证(登录，注册，找回密码)都是用Django自带的`contrib.auth`完成的

