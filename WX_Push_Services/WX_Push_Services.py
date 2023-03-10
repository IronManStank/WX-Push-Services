#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import json
import requests
import configparser
from retry import retry
from typing import Optional


class Error(Exception):
    pass


class ConfigError(Error):
    '''配置相关错误'''
    pass


class PushConfig(object):
    '''
    配置
    '''
    DEFAULT_INI_PATH = "config.ini"

    def __init__(
        self,
        corp_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        app_id: Optional[str] = None,
        key: Optional[str] = None
    ) -> None:
        '''
        使用环境变量初始化
        注意：未进行检查，但是你可以手动调用 self.check()
        '''
        self.corp_id: str = corp_id or os.environ.get('CORP_ID', '')
        self.app_secret: str = app_secret or os.environ.get('APP_SECRET', '')
        self.app_id: str = app_id or os.environ.get('APP_ID', '')
        self.key: str = key or os.environ.get('WEB_HOOK_BOT', '')

    # 重写 bool(self) 方法
    def __bool__(self):
        return self.check()
    __nozero__ = __bool__

    def check(self) -> bool:
        '''
        检查必要配置是否完善
        '''
        return all([self.corp_id, self.app_secret, self.app_id, self.key])

    def update_from_ini(self, path: Optional[str] = None):
        '''
        从 ini 配置文件更新
        :param path: ini 配置文件位置
        '''
        path = path or self.DEFAULT_INI_PATH
        self = read_ini_config(path)

    @classmethod
    def init_ini_config_file(cls, path: Optional[str] = None):
        '''
        初始化默认配置文件
        '''
        path = path or cls.DEFAULT_INI_PATH
        generate_config(path)


class APP_PUSH(object):
    def __init__(self, config: Optional[PushConfig] = None) -> None:
        """_summary_
        generate a instance of APP_PUSH,init config
        """
        config = config or PushConfig()
        self.touser = "@all"
        self.__config = config
        if not config.check():
            raise ConfigError("配置不完整")

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
            "corpid": self.__config.corp_id,
            "corpsecret": self.__config.app_secret,
        }
        response = requests.post(url, json=params)
        data = json.loads(response.text)

        if data["errmsg"] != "ok":
            raise Exception("Get token Failed!")
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
        # Determine  the send type

        if markdown:
            send_values = {
                "touser": self.touser,
                "msgtype": "markdown",
                "agentid": self.__config.app_id,
                "markdown": {"content": message},
                "safe": "0",
            }
        else:
            send_values = {
                "touser": self.touser,
                "msgtype": "text",
                "agentid": self.__config.app_id,
                "text": {"content": message},
                "safe": "0",
            }

        send_message = json.dumps(send_values)
        response = requests.post(url, send_message)
        status = response.json()["errmsg"]
        if status != "ok":
            # print(response.json())
            raise Exception("Message Sent Failed!")
        else:
            print("Message Sent Successfully!")


def read_ini_config(path: str) -> PushConfig:
    """_summary_
        Read loacl config file
    Returns:
        _type_: PushConfig

    """
    try:
        config = configparser.ConfigParser()
        config.read(path)
        corp_id = config["Config"]["corp_id"]
        app_id = config["Config"]["app_id"]
        app_secret = config["Config"]["app_secret"]
        web_hook_bot_key = config["Config"]["key"]
        return PushConfig(corp_id, app_secret, app_id, web_hook_bot_key)
    except Exception:
        generate_config(path)
        raise ConfigError(
            f"The configuration file {path} already exists. Please check whether the configuration file is correct.")


class WEB_HOOK_PUSH:
    def __init__(self, key: Optional[str]) -> None:
        """_summary_
        init config
        """
        self.header = {"Content-Type": "application/json;charset=UTF-8"}
        self.url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"

        self.key = key or os.environ.get('WEB_HOOK_BOT', '')
        if not self.key:
            raise ConfigError('未设置 WEB_HOOK_BOT')

    @retry(tries=3, delay=1)
    def send_message(self, message, markdown=False) -> None:
        """_summary_

        Args:
            message (str): message body
            markdown (bool, optional): _description_. Defaults to False.

        Raises:
            Exception: Faild and retry
        """
        params = {"key": self.key}
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
        send_data = json.dumps(message_body)
        send_data = requests.post(
            self.url, params=params, data=send_data, headers=self.header
        )
        status = send_data.json()["errmsg"]
        if status != "ok":
            print(send_data)
            raise Exception("Message Sent Failed!")
        else:
            print("Message Sent Successfully!")


def generate_config(path: str) -> None:
    """_summary_
    Generate config file with default content
    """
    try:
        size = os.path.getsize(path)
        if size == 0:
            raise FileNotFoundError
    except FileNotFoundError:
        print("Configuration file is not detected, generating configuration file......")
        config = configparser.ConfigParser()
        config["Config"] = {
            "corp_id": "your corp_id # Enter your enterprise ID of wechat background here.",
            "app_id": "your app_id # Enter your application ID of enterprise wechat background here",
            "app_secret": "your app_secret # Enter your application secret of enterprise wechat background here",
            "key": "your key # Enter the webhook key of the enterprise's wechat group chat robot here",
        }

        with open(path, "w") as f:
            config.write(f)
            # print("Configuration file generated successfully!")
    else:
        pass


def demo():
    # read from os env
    # wxps = APP_PUSH()
    # hookps = WEB_HOOK_PUSH()

    # read from ini
    config = PushConfig()       # 默认初始化读取环境变量
    config.update_from_ini()    # 此时会全部替换参数
    wxps = APP_PUSH(config)     # 使用此配置初始化

    test = (
        "# %s\n" % "Message display test"
        + "## •  TestMode: Markdown \n"
        + "## •  Type: %s \n" % "Message Push"
        + "## •  TestResult: %s \n" % "Pass"
    )
    wxps.send_message(message=test, markdown=False)
    # hookps.send_message(message=test, markdown=False)


if __name__ == "__main__":
    # generate_config()
    demo()
