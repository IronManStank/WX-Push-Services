from distutils.core import setup, Extension
import setuptools
import os

try:
    import pypandoc
    import pandoc

    long_description = open(file="README.rst", mode="r", encoding="utf-8").read()
    # pypandoc.convert_file('README.md','rst')
    # open(file='README.md',mode='r',encoding='utf-8').read()
    print(long_description)
except Exception as e:
    print(e)
    long_description = open(file="README.rst", mode="r", encoding="utf-8").read()

from os import path

this_directory = path.abspath(path.dirname(__file__))

setup(
    name="WX_Push_Services",
    version="1.0.9",
    author="Super.S",
    author_email="1157723200@qq.com",
    packages=["WX_Push_Services"],
    scripts=["WX_Push_Services/WX_Push_Services.py"],
    url="https://github.com/IronManStank/QYWX_PushService",
    license="MIT License",
    description="Push message to wechat",
    long_description=long_description,
    longs_description_content_type="text/x-rst",
    install_requires=["requests==2.28.2", "retry==0.9.2"],
    platforms="any",
    keywords=["wechat", "push", "message", "qywx", "wxpusher"],
    entry_points={"console_scripts": ["wx-push-services=wx_push_services.cli:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)


