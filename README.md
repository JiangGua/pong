# Pong

处理 Hyperlink Auditing 请求并记录来源网页、目标网页和点击次数。



## 使用

假设将 Pong 部署在 https://example.pong/ 下。

### Ping 一下

在来源页添加链接：

```html
<a href="https://dest.com" ping="https://example.pong/ping" target="_blank">链接文字</a>
```

试一下：

<a href="https://jianggua.github.io/pong-demo/index.html">链接测试 - Pong</a>



### 统计数据

浏览器访问：

```
https://example.pong/stats
```

试一下：

[Stats - Pong](https://pong-demo.herokuapp.com/stats)



### API

统计数据可通过 API 获取，以后可能可以通过 API 作简单的管理操作。

#### 统计数据

```
GET https://example.pong/api/stats
```

返回一个对象，样例如下：

```javascript
{
    "links":[
        {
            "count":8,
            "link":"https://www.jonbgua.com/",
            "origin":"http://127.0.0.1:5500/index.html"
        },
        {
            "count":4,
            "link":"https://www.baidu.com/",
            "origin":"http://localhost:5500/index.html"
        }
    ]
}
```



试一下：

[Stats - API - Pong](https://pong-demo.herokuapp.com/api/stats)



## 部署

按照常规的 Flask 应用部署流程即可。如希望部署到 Heroku，可参考 [用 GitHub Actions 把项目部署到 Heroku - Jonbgua](https://jonbgua.com/heroku-github-action.html)。



### 环境变量

#### 核心功能

##### ALLOW_PING_FROM_KEYWORD

来源地址关键字白名单。默认为 None，即不管来源网站是啥都予以记录；一旦 `ALLOW_PING_FROM_KEYWORD` 值不为空，则启用白名单，不包含关键字的 Origin 不予理会，以防其它网站盗用本服务。

注：目前只能设置一个关键字。
另注：因为只有关键字匹配这一个识别机制，所以并不能非常精准地只服务于某个网站，只是一定程度上提升了盗用服务的成本。



#### 数据库

```python
MONGO_URI		# MongoDB 地址(形如 mongodb://xxxxx 的一串 URI)
DATABASE_NAME	        # 数据库名称(默认为: "pong")
```



#### 网页

```python
SITE_TITLE		# 站点标题栏(标签页上面那个, 默认为 'Stats - Pong')
SITE_H1			# 站点一级标题(如果不设置此项，则自动使用 SITE_TITLE)
```



## 参考资料

- [Hyperlink Auditing - HTML 规范](https://html.spec.whatwg.org/multipage/links.html#hyperlink-auditing)
