import os
import json
import requests
import configparser
from retry import retry


class APP_PUSH(object):
    def __init__(self) -> None:
        """_summary_
        generate a instance of APP_PUSH,init config
        """
        self.touser = "@all"
        try:
            # 环境变量读取
            self.__corp_id = os.environ["CORP_ID"]
            self.__app_secret = os.environ["APP_SECRET"]
            self.__app_id = os.environ["APP_ID"]

        except KeyError:
            # 本地读取
            print("未检测到环境变量，尝试使用本地配置文件中")
            config = self.get_config()
            print(config)
            self.__app_id, self.__app_secret, self.__corp_id = config

    @retry(tries=3, delay=1)
    def _get_token(self) -> str:
        """_summary_

        Raises:
            Exception: get token error and retry

        Returns:
            str: token
        """
        url = r"https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            "corpid": self.__corp_id,
            "corpsecret": self.__app_secret,
        }
        response = requests.post(url, params)
        data = json.loads(response.text)

        if data["errmsg"] != "ok":
            print(data)
            raise Exception("获取token失败")
        else:
            data = json.loads(response.text)
            return data["access_token"]

    @retry(tries=3, delay=1)
    def send_message(self, message, markdown=False) -> None:
        """_summary_

        Args:
            message (_type_): string
            markdown (bool, optional): _description_. Defaults to False.

        Raises:
            Exception: Senderror and retry
        """
        url = (
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
            + self._get_token()
        )
        # 判断发送类型
        if markdown:
            send_values = {
                "touser": self.touser,
                "msgtype": "markdown",
                "agentid": self.__app_id,
                "markdown": {"content": message},
                "safe": "0",
            }
        else:
            send_values = {
                "touser": self.touser,
                "msgtype": "text",
                "agentid": self.__app_id,
                "text": {"content": message},
                "safe": "0",
            }

        send_message = json.dumps(send_values).encode("utf-8")
        response = requests.post(url, send_message)
        status = response.json()["errmsg"]
        if status != "ok":
            # print(response.json())
            raise Exception("消息发送失败")
        else:
            print("消息发送成功")

    @staticmethod
    def get_config() -> tuple:
        """_summary_
            获取本地配置文件中的配置信息
        Returns:
            _type_: tuple

        """
        try:
            config = configparser.ConfigParser()
            config.read("config.ini")
            corp_id = config["Config"]["corp_id"]
            app_id = config["Config"]["app_id"]
            app_secret = config["Config"]["app_secret"]
            return app_id, app_secret, corp_id
        except Exception as e:
            print(f"未检测到本地配置文件! 请配置必要文件！Err: {e}")


class WEB_HOOK_PUSH:
    def __init__(self) -> None:
        """_summary_
        init config
        """
        self.header = {"Content-Type": "application/json;charset=UTF-8"}
        self.url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send'
        try:
            self.key = os.environ["WEB_HOOK_BOT"]
        except KeyError:
            print("未检测到环境变量，尝试使用本地配置文件中")
            self.key = self.get_config()

    @retry(tries=3, delay=1)
    def send_message(self, message, markdown=False) -> None:
        """_summary_

        Args:
            message (str): message body
            markdown (bool, optional): _description_. Defaults to False.

        Raises:
            Exception: Faild and retry
        """
        params = {'key': self.key}
        if markdown:
            message_body = {
                "msgtype": "markdown",
                "markdown": {"content": message},
                "at": {"atMobiles": [], "isAtAll": False},
            }
        else:
            message_body = {
                "msgtype": "text",
                "text": {"content": message},
                "at": {"atMobiles": [], "isAtAll": False},
            }
        send_data = json.dumps(message_body).encode("utf-8")
        send_data = requests.post(
            self.url, params=params, data=send_data, headers=self.header)
        status = send_data.json()["errmsg"]
        if status != "ok":
            print(send_data)
            raise Exception("消息发送失败")
        else:
            print("消息发送成功")

    @staticmethod
    def get_config() -> str:
        """_summary_

        Returns:
            str: hook key
        """
        try:
            config = configparser.ConfigParser()
            config.read("./config.ini")
            web_hook_bot = config["Config"]["key"]
            print(web_hook_bot)
            return web_hook_bot
        except Exception as e:
            print("未检测到本地配置文件! 请配置必要文件！")


def demo():
    # wxps = APP_PUSH()
    hookps = WEB_HOOK_PUSH()

    test = (
        "# %s\n" % "消息推送展示项目：企业微信"
        + "## •  环境：测试环境 \n"
        + "## •  类型：%s \n" % "消息推送"
        + "## •  测试结果：%s \n" % "通过"
    )
    # wxps.send_message(message=test, markdown=False)
    hookps.send_message(message=test, markdown=False)


if __name__ == "__main__":
    demo()
