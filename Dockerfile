FROM python:3
ADD * /
RUN pip3 install tabulate
RUN pip3 install bs4

CMD [ "python3", "./app.py"]