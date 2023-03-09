from distutils.core import setup,Extension
import setuptools

setup(name='WX_Push_Services',
      version='1.0.0',
      author='Super.S',
      author_email='1157723200@qq.com',
      packages=['WX_Push_Services'],
      scripts=['WX_Push_Services/WX_Push_Services.py'],
      url='https://github.com/IronManStank/QYWX_PushService',
      license='Apache License',
      description='Push message to wechat',
      long_description='README.md',
      install_requires=['requests==2.28.2','retry==0.9.2'],
      platforms='any',
      longs_description_content_type='text/markdown',
      keywords=['wechat','push','message','qywx','wxpusher'])
      