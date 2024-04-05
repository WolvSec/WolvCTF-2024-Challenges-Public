FROM mcr.microsoft.com/azureml/pytorch-1.7-ubuntu18.04-py37-cpu-inference:latest

WORKDIR /app

USER root
RUN useradd -ms /bin/bash chall

# Do the pip install before copying the app so that changing the app source
# and rebuilding the image will not suffer this install every time.
COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY app/. .

USER root
RUN chown -R chall /app
USER chall

CMD [ "python3", "-u", "-m" , "flask", "run", "--host=0.0.0.0"]