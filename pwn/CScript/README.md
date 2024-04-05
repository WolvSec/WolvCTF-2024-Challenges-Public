# CScript
## Value: 500
## Solve Count: 4
## Description:
Scripting done right.

# Build
Either
```
cd challenge
scuba build
```
or
```
docker run -v=`pwd`/challenge:`pwd`/challenge:z -w `pwd`/challenge gcc:13.2.0@sha256:f993601701a37bef71e7f8fc1ef9410b09b15556f4371b06dcc10202cc81f9ea /bin/sh -c 'g++ --static -o chal engine.cpp runner.cpp -Wall -Werror -fno-toplevel-reorder -fPIC'
```
Verify
```
sha256sum chal  # expecting 8ae8eb916b6f740b79f17ef8669222f0ceba14a4d3a761f012ea8158ab614b10
```
Optionally deploy with kctf. The healthy/unhealthy status in kctf will tell you if the challenge is currently exploitable or not.

# To Distribute
ONLY challenge/chal and optionally challenge/Dockerfile
