FROM ubuntu

MAINTAINER Hypo i@ihypo.net

# 复制文件
RUN mkdir -p ~/makinami
COPY config.py ~/makinami
COPY manage.py ~/makinami
COPY requirenments.txt ~/makinami
COPY app/ ~/makinami

# 安装依赖
RUN apt-get update
RUN apt-get install pip
RUN pip install -r requirements.txt

CMD python manage.py start
