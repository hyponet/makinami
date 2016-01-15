# Makinami

Makinami是为VJ服务的爬虫模块，采用RESTful架构，可以独立运行，也可以认为是一个独立完整的程序。既使得VJ主程序可以与爬虫模块分离，分别部署，也方便众OJ爱好者直接使用，不必再重复造轮子。

## 技术栈

+ flask
+ scrapy
+ mongodb

## 部署

+ 安装mongodb（省略）
+ 安装依赖

```
pip install -r requirenments.txt
```

+ 启动命令

```
python manage.py start
```

## OJ支持列表

| OJ Name         | OJ Code | Language                                        |
| --------------- |:-------:|:-----------------------------------------------:|
| PKU JudgeOnline | poj     | `g++` `gcc` `java` `pascal` `c++` `c` `fortran` |

## API

*oj_code参照上面OJ支持列表*

### 获取题目

```
URI: /<string:oj_code>/problem/<int:problem_id>
method: GET
```

### 提交题目

```
URI: /<string:oj_code>/problem/<int:problem_id>
method: POST
```

### 获得运行结果

```
URI: /<string:oj_code>/run/<int:run_id>
method: GET
```

### 用户验证

```
URI: /<string:oj_code>/user
method: POST
```
## 其他

![Makinami](http://i4.tietuku.com/0b48773a298723da.png)

