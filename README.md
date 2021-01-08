# Testify - Oleg's Project

## AWS services
---

First step - Registration on [AWS](https://aws.amazon.com) website.
    *Note:* AWS service will ask your credit card number and other private information. It is safe and they need it for person's identification. No charges.

After registration perform following steps:
  * On *Account Management Console* page find service called *EC2*.
  * In *Instances* press Launch Instances
  * Find Ubuntu Server 20.04 LTS (HVM), SSD Volume Type and press select
  * choose t2 (free tier) and press Review and Launch
  * Down below again press Launch Button
  * In pop-up window you can select various options.
          If you're new to AWS select *Create a new key pair* and download file to your hard drive. Name it as you wish in the same window.
  * Saved file you need to copy to *.ssh* folder in your linux pc
  ```
  cd <filepath>/<filename>.pem ~/.ssh/<filename>.pem
  example: cp ~/Downloads/main.pem ~/.ssh/main.pem
  ```
  *Note:* Please remember the name of your key filename! You'll need it later.

  * In instances find Security property for following instance. You need to add Inbound rules. 
      * Add rule
      * choose Custom TCP
      * Port Range set as 80 for HTTP
      * Source:
          * if Custom set 0.0.0.0/0
          * or just choose Anywhere
  * Save rules

Now your AWS Instance ready.

## Accessing Remote Ubuntu
---

For connection to remote system change access rights for *.pem file.
```
sudo chmod 0400 ~/.ssh/<filename>.pem
```
Connecting to the system.
```
ssh -i ~/.ssh/<filename>.pem ubuntu@<ip_server>
```
  *Note:* to find ip_server get to your Instance page on AWS and find *Public IPv4 address*

## Setup
---
Clone testify repository.
```
git clone https://gitlab.com/UlrichKh/testify.git
```
Get to testify folder
```
cd testify
```
Change branch to *coop_home_work*
```
git checkout coop_home_work
```

## Install Docker and Docker-compose on remote system
---
*Note:* Before installation it is better to change password.
    ```
    sudo passwd ubuntu
    ```
### Docker installation

```
sudo apt update -y
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" -y
sudo apt update -y
apt-cache policy docker-ce
sudo apt install docker-ce -y
sudo usermod -aG docker ${USER}
su - ${USER}
id -nG
sudo usermod -aG docker ubuntu
```

### Docker-compose installation

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Environment setup
---

Go to testify directory
```
cd testify
```
Rename .env_example to .env
```
cp .env_example .env
```
In this file you'll find environment data which you need to run project. Data XXXX need to be changed to run properly.
  * RUN_MODE - mode which you can choose to run testify. Choose from line above.
  * PORT - port for nginx requests (default=8000)
  * SECRET_KEY - Django secret key (can generate with this [page](https://djecrety.ir))
  * ALLOWED_HOSTS - insert Public IPv4 address and Public IPv4 DNS separated with ':' or any other hosts using same way.
  * DB_USER - username for postgres DB
  * DB_PASSWORD - password for postgres DB
  * DB_HOST - docker posgres container name
  * DB_NAME - name of postgres DB
  * DB_PORT - port for postgres DB
  * WORKERS - number of instances

use *nano .env* to edit .env file.

## Run
---
 
 Run app.
 ```
 docker-compose up
 ```
if you wand to run it as daemon use 
``` docker-compose up -d```

Collect all staticfiles and media.
```
docker-compose exec backend python manage.py collectstatic
```
```
docker-compose exec backend cp -r media/ /var/www/testify/media
```
For database you need to create it in container.
```
docker-compose exec postgresql bash
```
then:
```
su - postgres
psql
```

Creation of database
```
CREATE DATABASE testify; 
CREATE USER testify_admin WITH PASSWORD ;XXXX;
ALTER ROLE testify_admin SET client_encoding TO 'utf8';
ALTER ROLE testify_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE testify_admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE testify TO testify_admin;
ALTER USER testify_admin CREATEDB;

```
*Note:* Insert in this commands your own passwords. And you can change any value for database.

At this moment you need to insert data in *.env* file. 
```
nano .env
```
Next step - is making migration to database
```
docker-compose exec backend python manage.py migrate
```

## Use

At this moment everything ready to use. Please, access your testify with *Public IPv4 DNS*.