FROM python:2.7.9

MAINTAINER Hypo i@ihypo.net

RUN mkdir /makinami
WORKDIR /makinami
COPY . /makinami

RUN pip install -r /makinami/requirenments.txt

CMD ["python","/makinami/manage.py","start"]

EXPOSE 5000
