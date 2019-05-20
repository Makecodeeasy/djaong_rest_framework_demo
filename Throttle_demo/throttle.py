# -*- coding:utf-8 -*- 
# author: yanzhengbin@bianfeng.com

import time

from rest_framework.throttling import BaseThrottle

request_log = dict()


class UserListThrottle(BaseThrottle):
    def __init__(self):
        self.record = None

    def allow_request(self, request, view):
        """
        限制10秒内匿名用户只能访问三次
        """
        remote_addr = self.get_ident(request)  # 获取标识(匿名用户用的表示是IP)
        current_timestamp = time.time()
        if remote_addr not in request_log:
            self.record = [current_timestamp, ]
            request_log[remote_addr] = self.record
            return True
        else:
            self.record = request_log[remote_addr]
            while self.record and self.record[-1] + 10 < current_timestamp:
                self.record.pop()

            if len(self.record) < 3:
                self.record.insert(0, current_timestamp)
                request_log[remote_addr] = self.record
                return True
            return False

    def wait(self):
        delay = time.time() - self.record[-1]
        return 10 - int(delay)


