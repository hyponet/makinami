FROM python:2.7.9

MAINTAINER Hypo i@ihypo.net

# 复制文件
RUN mkdir -p ~/makinami
WORKDIR ~/makinami
COPY . ~/makinami

# 安装依赖
RUN pip install -r requirements.txt

CMD python ~/makinami/manage.py start

EXPOSE 5000
