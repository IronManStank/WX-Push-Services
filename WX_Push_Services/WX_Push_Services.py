#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import json
import requests
import configparser
from retry import retry
<<<<<<< HEAD
import argparse
import traceback
=======
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
>>>>>>> 46b6b1af0161de3a88764aa2bc31d29ff2002717


class APP_PUSH(object):
    def __init__(self, config: Optional[PushConfig] = None) -> None:
        """_summary_
        generate a instance of APP_PUSH,init config
        """
        config = config or PushConfig()
        self.touser = "@all"
<<<<<<< HEAD
        try:
            # Read environment variables
            self.__corp_id = os.environ["CORP_ID"]
            self.__app_secret = os.environ["APP_SECRET"]
            self.__app_id = os.environ["APP_ID"]

        except KeyError:
            # Read local configuration file
            print(
                "System environment variables were not detected, reading configuration file......"
            )
            config = self.get_app_config()

            self.__app_id, self.__app_secret, self.__corp_id = config
=======
        self.__config = config
        if not config.check():
            raise ConfigError("配置不完整")
>>>>>>> 46b6b1af0161de3a88764aa2bc31d29ff2002717

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

<<<<<<< HEAD
    @staticmethod
    def get_app_config() -> tuple:
        """_summary_
            Read loacl config file
        Returns:
            _type_: tuple

        """
        try:
            config = configparser.ConfigParser()
            config.read(cl_argparse().config_file)
            corp_id = config["Config"]["CORP_ID"]
            app_id = config["Config"]["APP_ID"]
            app_secret = config["Config"]["APP_SECRET"]
            if app_id and app_secret and corp_id:
                return app_id, app_secret, corp_id
            else:
                raise ValueError(
                    "APP Configuration file error, please check the configuration file format"
                )
        except Exception:
            generate_config()
=======

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
>>>>>>> 46b6b1af0161de3a88764aa2bc31d29ff2002717


class WEB_HOOK_PUSH:
    def __init__(self, key: Optional[str]) -> None:
        """_summary_
        init config
        """
        self.header = {"Content-Type": "application/json;charset=UTF-8"}
        self.url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"
<<<<<<< HEAD
        try:
            self.key = os.environ["WEB_HOOK_BOT_KEY"]
        except KeyError:
            print(
                "No environment variables detected. Trying to use the local configuration file......"
            )
            self.key = self.get_web_hook_config()
=======

        self.key = key or os.environ.get('WEB_HOOK_BOT', '')
        if not self.key:
            raise ConfigError('未设置 WEB_HOOK_BOT')
>>>>>>> 46b6b1af0161de3a88764aa2bc31d29ff2002717

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

<<<<<<< HEAD
    @staticmethod
    def get_web_hook_config() -> str:
        """_summary_

        Returns:
            str: hook key
        """
        try:
            config = configparser.ConfigParser()
            config.read(cl_argparse().config_file)
            web_hook_bot_key = config["Config"]["WEB_HOOK_BOT_KEY"]
            if web_hook_bot_key:
                return web_hook_bot_key
            else:
                raise ValueError(
                    "WEB_HOOK_BOT_KEY Configuration file error, please check the configuration file!"
                )
        except Exception as e:
            generate_config()


def generate_config() -> None:
=======

def generate_config(path: str) -> None:
>>>>>>> 46b6b1af0161de3a88764aa2bc31d29ff2002717
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
            "CORP_ID": "your corp_id # Enter your enterprise ID of wechat background here.",
            "APP_ID": "your app_id # Enter your application ID of enterprise wechat background here",
            "APP_SECRET": "your app_secret # Enter your application secret of enterprise wechat background here",
            "WEB_HOOK_BOT_KEY": "your key # Enter the webhook key of the enterprise's wechat group chat robot here",
        }

        with open(path, "w") as f:
            config.write(f)
            # print("Configuration file generated successfully!")
    else:
        pass


<<<<<<< HEAD
def Send_Message_App(message="test", markdown=False) -> None:
    wxps = APP_PUSH()
    wxps.send_message(message, markdown)


def Send_Message_Webhook(message="test", markdown=False) -> None:
    wxps = WEB_HOOK_PUSH()
    wxps.send_message(message, markdown)


def cl_argparse() -> argparse.Namespace:
    parse = argparse.ArgumentParser(description="Weixin Message Push Service Help")
    parse.add_argument(
        "-cf",
        "--config_file",
        help="Config file path. The default path is './config.ini'",
        default="./config.ini",
    )
    parse.add_argument(
        "-mf",
        "--message_file",
        help="Input your message file path here. The default path is './output.log'. The program will auto resolve information from your file to string.",
        default="./output.log",
    )
    parse.add_argument(
        "-f",
        "--message_from_file",
        help="Determain the message source, string or file. If you using this option,the -mf param is needed!",
        type=bool,
        default=True,
    )
    parse.add_argument(
        "-m",
        "--message_str",
        help="Send your message. If you wanna use a file as message source, please use -mf params!",
        type=str,
        default="Change your message via -m or -mf params!",
    )
    parse.add_argument(
        "-a",
        "--app_method",
        help="Push message through app method via command line. Using app push method as default. If you want to change message push method, you should specific -w params.",
        type=bool,
        default=True,
    )
    parse.add_argument(
        "-w",
        "--web_hook_method",
        help="Swith message push method as web_hook_push method.",
        type=bool,
        default=False,
    )
    parse.add_argument(
        "-mds",
        "--markdown_signal",
        help="Swith message the message type to mardown.",
        type=bool,
        default=False,
    )
    return parse.parse_args()


def Send_File_Mesage(file_path) -> None:
    markdown_signal = cl_argparse().markdown_signal

    with open(file_path, "r") as f:
        message = f.read()

        if cl_argparse().web_hook_method:
            Send_Message_Webhook(message, markdown_signal)
        else:
            Send_Message_App(message, markdown_signal)


def Send_Message() -> None:
    message = cl_argparse().message_str
    markdown_signal = cl_argparse().markdown_signal
    try:
        if cl_argparse().message_from_file:
            Send_File_Mesage(cl_argparse().message_file)
        else:
            if cl_argparse().web_hook_method:
                Send_Message_Webhook(message, markdown_signal)
            else:
                Send_Message_App(message, markdown_signal)

    except Exception as e:
        traceback.print_exc()


def demo():
    # You can integrade the code into your own project as follow:
=======
def demo():
    # read from os env
    # wxps = APP_PUSH()
    # hookps = WEB_HOOK_PUSH()

    # read from ini
    config = PushConfig()       # 默认初始化读取环境变量
    config.update_from_ini()    # 此时会全部替换参数
    wxps = APP_PUSH(config)     # 使用此配置初始化

>>>>>>> 46b6b1af0161de3a88764aa2bc31d29ff2002717
    test = (
        "# %s\n" % "Message display test"
        + "## •  TestMode: Markdown \n"
        + "## •  Type: %s \n" % "Message Push"
        + "## •  TestResult: %s \n" % "Pass"
    )
    # You also can use the demo below to test the message push function.
    # test = (
    #     "# %s\n" % "Message display test"
    #     + "## •  TestMode: Markdown \n"
    #     + "## •  Type: %s \n" % "Message Push"
    #     + "## •  TestResult: %s \n" % "Pass"
    # )
    # Send_Message(test)
    push = APP_PUSH()
    push.send_message(test, markdown=True)
    
    # From now on (Version 1.0.5), you can use the command line to send the contents of the file to your Wechat. The specific operations are as follows:
    
if __name__ == "__main__":
    Send_Message()

    # demo()
