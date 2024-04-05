# Pwn: babypwn2
## Value: 50
## Solve Count: 182
## Description:
A harder babypwn.

# Build
Either
```
cd challenge
scuba build
```
or
```
docker run -v=`pwd`/challenge:`pwd`/challenge:z -w `pwd`/challenge gcc:8 /bin/sh -c 'gcc -Wno-deprecated-declarations -no-pie -fno-stack-protector -o chal main.c -Wall -Werror -std=c89'
```
Verify
```
sha256sum chal  # expecting 202c0149ee8e872b19056f79536ac876856bdaf8b5b970766f03c2492eb6e1f0
```
Optionally deploy with kctf. The healthy/unhealthy status in kctf will tell you if the challenge is currently exploitable or not.

# To Distribute
ONLY challenge/chal and optionally challenge/Dockerfile
