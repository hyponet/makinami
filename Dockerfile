FROM ubuntu

MAINTAINER Hypo i@ihypo.net

# 复制文件
RUN mkdir -p ~/makinami
ADD app ~/makinami
COPY config.py ~/makinami
COPY manage.py ~/makinami

# 安装依赖
RUN apt-get update
RUN apt-get install python-pip
RUN pip install -r requirements.txt

CMD python ~/makinami/manage.py start

EXPOSE 5000
