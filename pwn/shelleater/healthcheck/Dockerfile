# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
FROM gcr.io/kctf-docker/healthcheck@sha256:6709709a8cfd6e2d743c86d58398c00ca4eb26befd3b1a0a629ab35f91e98ef0

COPY healthcheck_loop.sh healthcheck.py healthz_webserver.py /home/user/
COPY chal /challenge/chal
COPY --from=debian@sha256:36a9d3bcaaec706e27b973bb303018002633fd3be7c2ac367d174bafce52e84e /lib/x86_64-linux-gnu/libc.so.6 /challenge/libc.so.6
# COPY libc.so.6 /challenge/libc.so.6
#/lib/x86_64-linux-gnu/libc.so.6
RUN apt-get update && apt-get install -y python3-pip && pip3 install pwntools

CMD kctf_drop_privs /home/user/healthcheck_loop.sh & /home/user/healthz_webserver.py
