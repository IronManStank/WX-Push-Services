#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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
            # Read environment variables
            self.__corp_id = os.environ["CORP_ID"]
            self.__app_secret = os.environ["APP_SECRET"]
            self.__app_id = os.environ["APP_ID"]

        except KeyError:
            # Read local configuration file
            print(
                "Configuration file is not detected, generating configuration file......"
            )
            config = self.get_config()
            
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

        send_message = json.dumps(send_values)
        response = requests.post(url, send_message)
        status = response.json()["errmsg"]
        if status != "ok":
            # print(response.json())
            raise Exception("Message Sent Failed!")
        else:
            print("Message Sent Successfully!")

    @staticmethod
    def get_config() -> tuple:
        """_summary_
            Read loacl config file
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
        except Exception:
            generate_config()


class WEB_HOOK_PUSH:
    def __init__(self) -> None:
        """_summary_
        init config
        """
        self.header = {"Content-Type": "application/json;charset=UTF-8"}
        self.url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"
        try:
            self.key = os.environ["WEB_HOOK_BOT"]
        except KeyError:
            print(
                "No environment variables detected. Trying to use the local configuration file......"
            )
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

    @staticmethod
    def get_config() -> str:
        """_summary_

        Returns:
            str: hook key
        """
        try:
            config = configparser.ConfigParser()
            config.read("./config.ini")
            web_hook_bot_key = config["Config"]["key"]

            return web_hook_bot_key
        except Exception as e:
            generate_config()


def generate_config() -> None:
    """_summary_
    Generate config file......
    """
    try:
        size = os.path.getsize("./config.ini")
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

        with open("./config.ini", "w") as f:
            config.write(f)
            print("Configuration file generated successfully!")
    else:
        print(
            "The configuration file already exists. Please check whether the configuration file is correct."
        )


def demo():
    wxps = APP_PUSH()
    # hookps = WEB_HOOK_PUSH()

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
