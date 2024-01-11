#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : base_java_loader.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2024/1/11

import os
import sys

sys.path.append('..')
try:
    # from base.spider import Spider as BaseSpider
    from base.spider import BaseSpider
except ImportError:
    from t4.base.spider import BaseSpider


class Spider(BaseSpider):  # 元类 默认的元类 type
    jar_path: str = ''
    jClass = None

    def _prepare_env(self, jpype):
        try:
            jpype.startJVM(classpath=[self.jar_path], convertStrings=False)
        except Exception as e:
            self.log(f'jpype.startJVM发送了错误:{e}')

    def init_jar(self, jar_path="./bdys.jar"):
        self.log(f'base_java_loader 初始化jar文件:{jar_path}')
        if not os.path.exists(jar_path):
            raise FileNotFoundError
        self.jar_path = jar_path
        if self.ENV.lower() == 't4':
            import jpype
            self._prepare_env(jpype)
            self.jClass = jpype.JClass
        elif self.ENV.lower() == 't3':
            self.jClass = None

    def init(self, extend=""):
        pass

    def homeContent(self, filter):
        pass

    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        pass

    def detailContent(self, ids):
        pass

    def searchContent(self, key, quick, pg=1):
        pass

    def playerContent(self, flag, id, vipFlags):
        pass

    def localProxy(self, param):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def getName(self):
        pass
