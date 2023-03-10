# 怎样使用微信以及微信推送服务

- [怎样使用微信以及微信推送服务](#怎样使用微信以及微信推送服务)
  - [实现微信推送服务的两种方式](#实现微信推送服务的两种方式)
- [使用方式](#使用方式)
    - [1. 注册企业微信，获取必要token](#1-注册企业微信获取必要token)
    - [2. 安装python运行库](#2-安装python运行库)
    - [3. 运行示例`demo`](#3-运行示例demo)
  - [注意事项](#注意事项)



## 主要用途



## 实现微信推送服务的两种方式

1. 调用企业微信应用

使用该种方法时请按照下文方式获得必要token。

2. 使用`web hook`调用企业微信机器人

使用该种方式时仅需要知道企业微信机器人的`web hook key`。在使用之前，请确保已在企业微信群里中添加企业微信机器人，并按照下文方法获得`web hook key`。

# 使用方式

### 1. 注册企业微信，获取必要token

- 使用企业微信应用时获取以下信息：

注册网址：https://work.weixin.qq.com/

1. 获取企业ID

![image-20230225000159967](https://s2.loli.net/2023/02/25/9V3l5IGvZiFqMRu.png)

在仓库`secrets`中添加如下变量：`CORP_ID=your_id`

2. 添加应用并获取下述变量

![image-20230225100535470](https://s2.loli.net/2023/02/25/XaTm65MjOE3A8iJ.png)

![image-20230225100751916](https://s2.loli.net/2023/02/25/bkJGwyzZfgIOa7R.png)

在仓库`secrets`中添加：`APP_SECRET=your_app_secret`以及`APP_ID=your_app_id`

- 使用机器人`webhook`方式时，请添加以下变量：

![image-20230225101235709](https://s2.loli.net/2023/02/25/gOtL3dmJqpBDWIh.png)

![image-20230225101249931](https://s2.loli.net/2023/02/25/bghHpI3UDvq29lM.png)

找到群聊，在其中点击机器人配置，获取`webhookkey`中`key`字段；在仓库中添加`key=your_web_hook_key`

至此，必要信息已手机完毕。

### 2. 安装python运行库

执行`pip install -r requirments.txt`

### 3. 生成并填写配置文件

初次运行`main.py`中的`demo`，会在当前目录下生成`config.ini`配置文件，如下面代码所示：

```ini
[Config]
corp_id = your corp_id # Enter your enterprise ID of wechat background here.
app_id = your app_id # Enter your application ID of enterprise wechat background here
app_secret = your app_secret # Enter your application secret of enterprise wechat background here
# 使用APP_PUSH方式时以上必填
# 使用WEB_HOOK_PUSH方式仅需填写下述消息
key = your key # Enter the webhook key of the enterprise's wechat group chat robot here

```

依次按照`# .......`中的提示填写必要信息。

### 3. 运行示例 `demo`
在`main.py`中再次运行示例`demo`
```python
    config = PushConfig()       # 默认初始化读取环境变量
    config.update_from_ini()    # 此时会全部替换参数   
    # wxps = APP_PUSH()
    hookps = WEB_HOOK_PUSH(config.key)    # 使用此配置初始化

    test = (
        "# 企业微信消息测试"
        + "## •  二级标题"
        + "## •  测试通过"
    )
    # wxps.send_message(message=test, markdown=False)
    hookps.send_message(message=test, markdown=False)
```

即可发送成功，此时可在微信中看到相应信息。

## 注意事项

**经过测试。markdown信息并不能在微信查看。只能在企业微信查看。所以，如果想要在微信查看，需要将markdown类型消息改为text类型**

