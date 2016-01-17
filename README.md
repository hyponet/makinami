# Makinami

Makinami是为VJ提供微服务的爬虫模块，采用RESTful设计，可以独立运行，也可以认为是一个独立完整的程序。既使得VJ主程序可以与爬虫模块分离，多地部署，也方便众OJ爱好者直接使用，不必再重复造轮子。

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

## 快速参与开发

### 增添新OJ支持

+ 在config的ojs中添加对应的 `oj_code`
+ 在/app/api中添加对应的API文件，提供api规范的实现
+ 在/app/illustrious/spiders添加对应的爬虫文件，实现：
  - init爬虫： 爬取所有的题目
  - problem爬虫： 根据 problemid 爬取单个题目
  - result爬虫： 根据 runid 爬取运行结果
  - user爬虫： 根据 username ， password 爬取用户信息

参考样例文件：
- API文件：/app/api/poj.py
- 爬虫文件：/app/illustrious/spiders/poj.py

## Q&A

+ 如果原OJ中增添的新题目怎么及时更新？

本来打算每日把原OJ所有的题目更新，但感觉做的无用功更多。因此init爬虫只在服务启动时使用，之后的新增题目和更新题目都采用“用后更新”的方式。
对于原OJ添加了新的题目。因为Makinami对于外部请求只会返回数据库中的信息，因此，对于数据库中没有的内容，将会返回 `status: 404`，然后运行爬虫尝试爬取，如果有新题目，就入库保存。

+ 如果原OJ中题目有变动，怎么处理？

首先，在项目启动后，会立刻更新爬取所支持OJ的所有题目。在外部每次请求获得题目信息时，先将数据库中的题目信息返回，然后验证爬取时间，如果已经超过 7d 则新开辟进程，重新爬取该题目（用后爬取）。

+ 如果提交题目后，运行结果未及时得出怎么处理？

爬虫会把未得到结果的runid开辟新进程，循环爬取，直到得到结果（持久化）或超时（30min），持久化后将保存在数据库中。
外部根据runid查询结果的请求，以数据库优先，如果数据库中不存在，则再将该runid开辟进程，循环爬取。

![Makinami](http://i4.tietuku.com/0b48773a298723da.png)

