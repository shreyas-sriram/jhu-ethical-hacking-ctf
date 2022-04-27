# Wordle

Contains the code for **Wordle game**. Will be hosted at port `1337`.

Connect to the game using `netcat` and solve it to get a secret key and hint to the next step.

## Vulnerabilities

> None

## Path to pwn

- use brains
- think
- solve

## Deployment in Virtual Machine

Copy `wordle.py` to `/home/user/wordle.py`.

### Start application
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

```
$ sudo systemctl daemon-reload
$ sudo systemctl enable wordle.service
$ sudo systemctl start wordle.service
```
