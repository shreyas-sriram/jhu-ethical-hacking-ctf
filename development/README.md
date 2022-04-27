# Development

Contains the development build for **Nidavellir Website**. Will be hosted at `development-valknut.nidavellir.snap`.

## Vulnerabilities

- Misconfigured JWT token
- SSTI

## Path to pwn

- login as `guest` using credentials received in previous step (forensics challenge)
- impersonate `admin` by tampering the JWT token
    - JWT secret key is fetched from a URL provided in the JWT claims
    - attacker hosts their own JWT key and the server uses this key to verify the modified JWT
    - the server finally accepts this JWT as valid
- exploit **SSTI** in API status functionality to get shell as `www-data` on the machine
