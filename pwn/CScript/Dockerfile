FROM --platform=amd64 gcc:13.2.0@sha256:f993601701a37bef71e7f8fc1ef9410b09b15556f4371b06dcc10202cc81f9ea

WORKDIR /app

COPY . /app

RUN g++ -shared -fPIC -o libengine.so engine.cpp -Wall -Werror

RUN g++ -o runner runner.cpp -lengine -L/app -Wall -Werror -fno-toplevel-reorder

CMD ["/app/runner", "/app/source.txt"]

RUN groupdel staff

ENV LD_LIBRARY_PATH=/app
