FROM python:3.12.2

RUN groupadd -r admin && useradd -r -g admin admin
RUN groupadd -r ctf && useradd -r -g ctf ctf

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY app.py .
COPY flag.txt .
COPY index.html .
RUN chown admin:admin . && chmod 444 .
RUN chown admin:admin flag.txt && chmod 444 flag.txt
RUN chown admin:admin app.py && chmod 444 app.py
RUN chown admin:admin index.html && chmod 444 index.html

RUN rm -f /bin/chmod /usr/bin/chmod /bin/chown /usr/bin/chown /usr/bin/curl usr/bin/apt-get

USER ctf

CMD [ "python3", "-u", "-m" , "flask", "run", "--host=0.0.0.0"]

