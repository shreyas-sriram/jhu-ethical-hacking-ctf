# Internal

Contains the versioning history (.git) for **mjolnir** binary or similar. Will be hosted at `internal.nidavellir.snap/.git`.

The original binary will be available only to `localhost`, while the contents of `.git` will be publicly available.

The binary returns the number of characters in a file. It takes 2 input - filename and character.

Example
```
// contents of file /root/password.txt (all unique characters)
// password will be of a fixed format (xxxx-xxxx)
page-mint

// running binary
./mjolnir "/root/password.txt" "a"
1
```

## Vulnerabilities

- SUID binary

## Path to pwn

- read characters from the admin password text file using the binary
- smartly formulate words in the given format and characters
- login as `root`
