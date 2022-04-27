# Forensics

Contains the code for **Forensic challenges**. Image `stormbreaker.jpeg` will be hosted at `www.nidavellir.snap/ctf-files`.

Solve the challenge to obtain the password for `guest` user and login at `development-valknut.nidavellir.snap`.

## Vulnerabilities

- Information in image EXIF data
- Steganography

## Path to pwn

- run `exiftool` on the image to obtain a DES-encrypted password

```
$ exiftool stormbreaker.jpeg
...
Author                          : DES-12ed102cd7c746f3cbe0fb380a8bfcef
Comment                         : iv-000000000000000
...
```

- decrypt the DES password using the `secret` received in Wordle challenge - [CyberChef Solution](https://gchq.github.io/CyberChef/#recipe=DES_Decrypt(%7B'option':'UTF8','string':'dinklage'%7D,%7B'option':'Hex','string':'000000000000000'%7D,'CBC','Hex','Raw')&input=MTJlZDEwMmNkN2M3NDZmM2NiZTBmYjM4MGE4YmZjZWY)

- run `steghide` to extract hidden DES-encrypted `guest` password

```
$ steghide extract -sf stormbreaker.jpeg
Enter passphrase: <nil>
wrote extracted data to "guest-password.enc".

$ cat guest-password.enc 
ddcccaf9151c1b10cf82e13597f2313c
```

- decrypt the DES password using the `key` received in previous step - [CyberChef Solution](https://gchq.github.io/CyberChef/#recipe=DES_Decrypt(%7B'option':'UTF8','string':'draupnir'%7D,%7B'option':'Hex','string':'000000000000000'%7D,'CBC','Hex','Raw')&input=ZGRjY2NhZjkxNTFjMWIxMGNmODJlMTM1OTdmMjMxM2M)

```
guest:grooooooooT
```
