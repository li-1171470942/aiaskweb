from setuptools import setup, find_packages

setup(
    name='SCWECweb',  # 将此替换为你的项目名称
    version='0.1.0',  # 项目版本号
    packages=find_packages(),  # 自动发现项目中的所有包
    include_package_data=True,  # 包含 MANIFEST.in 中指定的文件
    install_requires=[  # 你的项目依赖的第三方库
        'appdirs==1.4.4',
        'asgiref==3.7.2',  # ASGI references - 版本号根据你的实际更改
        'attrs==23.1.0',
        'beautifulsoup4==4.12.2',
        'blinker==1.9.0',
        'Brotli==1.0.9',
        'bs4==0.0.2',
        'certifi==2023.9.20',
        'cffi==1.15.1',
        'channels==4.2.0',
        'charset-normalizer==2.1.1',
        'click==8.1.7',
        'colorama==0.4.6',
        'cssselect==1.2.0',
        'Django==4.2.16',
        'exceptiongroup==1.1.3',
        'fake-useragent==1.5.1',
        'Flask==3.1.0',
        'h11==0.14.0',
        'idna==3.4',
        'importlib_metadata==8.5.0',
        'importlib_resources==6.4.5',
        'itsdangerous==2.2.0',
        'Jinja2==3.1.4',
        'lxml==5.3.0',
        'lxml_html_clean==0.4.1',
        'MarkupSafe==3.0.2',
        'numpy==2.0.2',
        'outcome==1.1.0',
        'packaging==24.2',
        'panda==0.3.1',
        'pandas==2.2.3',
        'parse==1.20.2',
        'pycparser==2.21',
        'pyee==11.1.1',
        'pyppeteer==2.0.0',
        'pyquery==2.0.1',
        'PySocks==1.7.1',
        'python-dateutil==2.9.0.post0',
        'python-dotenv==1.0.1',
        'pytz==2024.2',
        'requests==2.31.0',
        'requests-html==0.10.0',
        'selenium==4.17.0',
        'six==1.16.0',
        'sniffio==1.3.0',
        'sortedcontainers==2.4.0',
        'soupsieve==2.4.1',
        'sqlparse==0.4.4',
        'tqdm==4.67.0',
        'trio==0.21.0',
        'trio-websocket==0.9.2',
        'typing_extensions==4.6.0',
        'tzdata==2024.2',
        'urllib3==1.26.20',
        'w3lib==2.2.1',
        'webdriver-manager==4.0.2',
        'websocket-client==1.5.2',
        'websockets==10.4',
        'Werkzeug==3.1.3',
        'win-inet-pton==1.1.0',
        'wsproto==1.0.0',
        'zipp==3.21.0',
    ],
    entry_points={
        'console_scripts': [
            # 根据实情添加你的项目的可执行脚本入口
            # 'python manage.py runserver'
        ],
    },
    author='Li xin l32524',  # 填写作者信息
    author_email='1171470942@qq.com',  # 填写邮箱地址
    description='AI summarization tool for community wireless experience cases',  # 项目描述
    url='https://github.com/users/li-1171470942/projects/4',  # 项目的主页
    classifiers=[
        'Development Status :: 3 - Alpha',  # 开发阶段
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # 或其他许可证
        'Programming Language :: Python :: 3.9',
    ],
    license='MIT',  # 项目的许可协议
    python_requires='>=3.9',  # Python 版本要求
)