FROM python:3-alpine3.15
WORKDIR /PROJECTWEB.TWO
COPY . /PROJECTWEB.TWO/
RUN pip install -r requirements.txt
CMD ["gunicorn", "--no-sendfile","--bind", "0.0.0.0:3000", "run:app"]
