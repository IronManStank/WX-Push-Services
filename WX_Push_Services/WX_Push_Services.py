#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import json
import requests
import configparser
from retry import retry
import argparse
import traceback


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
                "System environment variables were not detected, reading configuration file......"
            )
            config = self.get_app_config()

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
                "agentid": self.__config.app_id,
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


class WEB_HOOK_PUSH:
    def __init__(self) -> None:
        """_summary_
        init config
        """
        self.header = {"Content-Type": "application/json;charset=UTF-8"}
        self.url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"
        try:
            self.key = os.environ["WEB_HOOK_BOT_KEY"]
        except KeyError:
            print(
                "No environment variables detected. Trying to use the local configuration file......"
            )
            self.key = self.get_web_hook_config()

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
    """_summary_
    Generate config file with default content
    """
    try:
        size = os.path.getsize(cl_argparse().config_file)
        if size == 0:
            raise FileNotFoundError
    except FileNotFoundError:
        print("Configuration file was not detected, generating configuration file......")
        config = configparser.ConfigParser()
        config["Config"] = {
            "CORP_ID": "your corp_id # Enter your enterprise ID of wechat background here.",
            "APP_ID": "your app_id # Enter your application ID of enterprise wechat background here",
            "APP_SECRET": "your app_secret # Enter your application secret of enterprise wechat background here",
            "WEB_HOOK_BOT_KEY": "your key # Enter the webhook key of the enterprise's wechat group chat robot here",
        }

        with open(cl_argparse().config_file, "w") as f:
            config.write(f)
            # print("Configuration file generated successfully!")
    else:
        pass


def Send_Message_App(message="test", markdown=False) -> None:
    wxps = APP_PUSH()
    wxps.send_message(message, markdown)


def Send_Message_Webhook(message="test", markdown=False) -> None:
    wxps = WEB_HOOK_PUSH()
    wxps.send_message(message, markdown)


def cl_argparse() -> argparse.Namespace:
    parse = argparse.ArgumentParser(
        description="Weixin Message Push Service Help")
    parse.add_argument(
        "-cf",
        "--config_file",
        help="Config file path. The default path is './config.ini'",
        default="./config.ini",
    )

    parse.add_argument(
        "-w",
        "--web_hook_method",
        help="Push message through app method via command line. Using app push method as default. If you want to change message push method, you should specific -a params.",
        action="store_true",
    )

    parse.add_argument(
        "-mds",
        "--markdown_signal",
        help="Swith message the message type to mardown.",
        action="store_true",
    )
    parse.add_argument(
        "-df",
        "--message_from_file",
        help="Determain the message source, string or file. If you using this option,the -mf param is needed!",
        action="store_false",
        # required=True,
    )
    group = parse.add_mutually_exclusive_group()
    group.add_argument(
        "-m",
        "--message_str",
        help="Send your message. If you wanna use a file as message source, please use -mf params!",
        type=str,
        default="Change your message via -m or -mf params!",
        # required=True,
    )
    group.add_argument(
        "-mf",
        "--message_file",
        help="Input your message file path here. The default path is './output.log'. The program will auto resolve information from your file to string.",
        default="./output.log",
        # exclusive=True,
    )
    situation1 = (parse.parse_args().message_from_file == False) and (
        parse.parse_args().message_str == "Change your message via -m or -mf params!"
    )
    situation2 = (notparse.parse_args().message_str !=
                  "Change your message via -m or -mf params!")
    if situation1 or situation2:
        raise Exception(
            "The -m and -df option must be used together! Please check your input!")

    else:
        pass
    # situation1 =(
    #
    # ) and (parse.parse_args().message_file == "./output.log")
    # # situation2 =
    # if situation1:
    #     pass
    # else:
    #     raise Exception("The -m and -df option must be used together! Please check your input!")

    return parse.parse_args()


def Send_File_Mesage(file_path) -> None:
    markdown_signal = cl_argparse().markdown_signal
    try:
        with open(file_path, "r") as f:
            message = f.read()

            if cl_argparse().web_hook_method:
                Send_Message_Webhook(message, markdown_signal)
            else:
                Send_Message_App(message, markdown_signal)
    except FileNotFoundError as e:
        print(
            "Please specific the message file to be sent. The default file was not detected: . /output.log"
        )


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
