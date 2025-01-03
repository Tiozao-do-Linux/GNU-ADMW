FROM ubuntu:22.04
WORKDIR /app

COPY . ./
RUN apt update
RUN apt -y install --no-install-recommends python3-pip python3-venv
RUN python3 -m venv .venv
RUN . .venv/bin/activate
RUN pip3 install -r requirements.txt
EXPOSE 8080
CMD ["python3","GNU-ADMW.py"]