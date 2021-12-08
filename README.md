- [1. AWS EC2](#1-aws-ec2)- [1. AWS EC2](#1-aws-ec2)
  - [1.1. Connect uuing SSH](#11-connect-uuing-ssh)
# 1. AWS EC2
## 1.1. Connect uuing SSH
* Set the permissions of your private key<br>
`chmod 400 hoang-example.pem`
* To connect to your instance using SSH<br>
`ssh -i "hoang-example.pem" ubuntu@ec2-54-163-162-99.compute-1.amazonaws.com`
* Transfer files to Linux instances using an SCP client<br>
`scp -i key_pair/hoang-example.pem source/file ubuntu@ec2-54-163-162-99.compute-1.amazonaws.com:/home/ubuntu`



