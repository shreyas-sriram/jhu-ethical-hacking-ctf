# Snake-game

Contains the code and builds for **Snake game**. All compiled binaries will be hosted at `www.nidavellir.snap/ctf-files`.

This is a snake game written in Go which sends a GET request to `development-valknut.nidavellir.snap` everytime the snake eats the food.

## Vulnerabilities

> None

## Path to pwn

- set proxy (Burp Suite or similar) for all terminal applications and run the game

```
$ env HTTP_PROXY=http://127.0.0.1:8080 ./snake-*
```

- discover the subdomain `development-valknut.nidavellir.snap` by viewing the requests in the proxy
