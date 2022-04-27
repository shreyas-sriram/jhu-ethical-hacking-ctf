# Machine Setup

## Ubuntu Server Setup
1. Install [Ubuntu Server VM](https://ubuntu.com/download/server) with default user `user:user` and hostname as `nidavellir`

2. Increase filesystem space - refer to [this answer on StackOverflow](https://askubuntu.com/questions/1106795/ubuntu-server-18-04-lvm-out-of-space-with-improper-default-partitioning)

## Wordle Setup

1. Copy `wordle.py` to `/home/user/wordle.py`

2. Change permissions

```
$ sudo chmod 660 /home/user/wordle.py
```

3. Add the program to `systemd` using the following configuration

```
# /etc/systemd/system/wordle.service

[Unit]
Description=Wordle
After=multi-user.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /home/user/wordle.py

[Install]
WantedBy=multi-user.target
```

3. Load, enable and start the service

```
$ sudo systemctl daemon-reload
$ sudo systemctl enable wordle.service
$ sudo systemctl start wordle.service
```

## Install and Setup Apache

1. Install Apache2

```
$ sudo apt update
$ sudo apt install apache2
```

2. Check the status of the service and test the connection

```
$ sudo systemctl status apache2
$ curl <ip>
```

3. Install WSGI

```
$ sudo apt-get install libapache2-mod-wsgi-py3
$ sudo a2enmod wsgi
```

## Install pip3

1. Install pip3

```
$ sudo apt-get install python3-pip
```

## Setup Websites

### Main (www.nidavellir.snap)

1. Copy `main/*` to `/var/www/main/`

2. Copy `forensics/stormbreaker.jpeg` and `snake-game/binaries/*` to `/var/www/main/ctf-files/`

2. Install a virtual environment

```
$ sudo pip3 install virtualenv
$ sudo virtualenv venv
$ source venv/bin/activate
```

3. Install requirements

```
$ pip3 install -r requirements.txt
```

4. Exit virtualenv

```
$ deactivate
```

### Development (development-valknut.nidavellir.snap)

1. Copy `development/*` to `/var/www/development-valknut/`

2. Install a virtual environment

```
$ sudo pip3 install virtualenv
$ sudo virtualenv venv
$ source venv/bin/activate
```

3. Install requirements

```
$ pip3 install -r requirements.txt
```

4. Exit virtualenv

```
$ deactivate
```

### Secret (localhost:3000)

> Used by development-valknut.nidavellir.snap

1. Copy `development/.secret` to `/var/www/secret/`

### Internal (internal-valknut.nidavellir.snap)

1. Copy `internal/leaked-git/*` to `/var/www/internal-valknut/.git/`

## Apache Configurations

1. Copy `apache/*` to `/etc/apache2/sites-available/`

2. Update ownership for website files

```
$ sudo chown -R www-data:www-data /var/www/development-valknut /var/www/internal-valknut /var/www/main /var/www/secret
```

3. Enable the sites

```
$ sudo a2ensite 000-default.conf default-ssl.conf development.nidavellir.com.conf internal.nidavellir.com.conf localhost.conf main.nidavellir.com.conf
$ sudo systemctl restart apache2
```

## Setup Stormbreaker

1. Build `internal/main.go` and create binary `stormbreaker`

```
$ go build -o stormbreaker internal/main.go
```

2. Create directory `/opt/binaries/` and copy `stormbreaker` to `/opt/binaries/`

3. Set as executable

```
$ sudo chmod +x /opt/binaries/stormbreaker
```

4. Update ownership and permissions

```
$ sudo chown root:user /opt/binaries/stormbreaker
$ sudo chmod 750 /opt/binaries/stormbreaker
```

5. Set SUID bit

```
$ sudo chmod u+s /opt/binaries/stormbreaker
```

## Setup Admin Password File

1. Copy `internal/.passwd` to `/root/`

2. Change permissions

```
$ sudo chmod 660 /root/.passwd
```

## Setup Flags

1. Copy `flags/user.txt` to `/home/user/`

2. Copy `flags/root.txt` to `/root/`

3. Change permissions

```
$ sudo chmod 660 /home/user/user.txt /root/root.txt
```

## Update System Accounts and Permissions

1. Update `user` password

```
# user:dinklage

$ passwd user
```

2. Update `root` password

```
# root:sexy-ping

$ sudo passwd root
```

3. Remove `user` from `sudoers` group

```
$ sudo deluser user sudo
```

Happy hacking! :skull_and_crossbones:
