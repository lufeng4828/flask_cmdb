#coding:utf-8

import os
import json
import traceback
from requests import get, post

__author__ = 'lufeng'

class Automagic(object):
    """
    无法用言语表达的一个类
    """

    def __init__(self, clientref, base):
        self.base = base
        self.clientref = clientref

    def __getattr__(self, name):
        base2 = self.base[:]
        base2.append(name)
        return Automagic(self.clientref, base2)

    def __call__(self, *args, **kargs):
        if not self.base:
            raise AttributeError("something wrong here in Automagic __call__")
        if len(self.base) < 2:
            raise AttributeError("no method called: %s" % ".".join(self.base))
        func = "/".join(self.base[0:])
        return self.clientref.call_func(func, *args, **kargs)


class CMDB(object):
    """
    cmdb客户端链接工具
    """
    def __init__(self, app=None, host=None, secretid=None, signature=None):
        self.app = app
        self.host = host
        self.secretid = secretid
        self.signature = signature

    def get_resource(self, path, *args, **kwargs):
        try:
            headers = {
                "x-secretid": self.secretid,
                "x-signature": self.signature
            }
            if args:
                headers.update({"Content-Type": "application/json"})
            if args:
                body = json.dumps(args[0])
            else:
                body = kwargs

            res = post("{0}/resource/v1/{1}.json".format(self.host, path), data=body, headers=headers)
            return res.json()
        except ValueError:
            if self.app:
                self.app.logger.error(res.text)
            else:
                print res.text
        except:
            if self.app:
                self.app.logger.error(traceback.format_exc())
            else:
                print traceback.format_exc()
            return {}

    def get_email(self, um):
        emails = set([])
        result = self.get_resource("entity/search", {"schema": "user", "q": "attributes.um:%s" % um})
        if result.get("success"):
            for res in result["data"]["content"]:
                email = res.get("attributes", {}).get("email")
                for e in email:
                    if e:
                        emails.add(e)
        return list(emails)

    def get_department(self, um):
        """
        department
        :param um:
        :return:
        """
        if not um:
            return ''
        result = self.get_resource("entity/search", {"schema": "user", "q": "attributes.um:%s" % um})
        if result.get("success") and result["data"]["content"]:
            entity = result["data"]["content"][0]
            attr = entity.get("attributes", {})
            return attr.get("department", '')
        else:
            return ''

    def get_department_users(self, um):
        """
        获取部门用户列表
        :param um:
        :return:
        """
        users = set([])
        department = self.get_department(um)
        if not department:
            return list(users)
        result = self.get_resource("entity/search", {"schema": "user", "q": u"attributes.department:%s" % department})
        if result.get("success") and result["data"]["content"]:
            for ent in result["data"]["content"]:
                users.add(ent["attributes"]["um"])
        return list(users)

    def get_contact(self, um):
        """
        获取姓名和联系电话
        :param um:
        :return:
        """
        phone = set([])
        result = self.get_resource("entity/search", {"schema": "user", "q": "attributes.um:%s" % um})
        if result.get("success") and result["data"]["content"]:
            entity = result["data"]["content"][0]
            attr = entity.get("attributes", {})
            for p in attr.get("phone", []):
                if p:
                    phone.add(p)
            user = {
                "name": attr.get("name"),
                "phone": list(phone)
            }
            return user
        else:
            return None

    def get_name(self, um):
        """

        """
        if not um:
            return ''
        result = self.get_resource("entity/search", {"schema": "user", "q": "attributes.um:%s" % um})
        if result.get("success") and result["data"]["content"]:
            entity = result["data"]["content"][0]
            attr = entity.get("attributes", {})
            return attr.get("name", '')
        else:
            return ''

    def get_minions(self, um):
        """
        获取直接下属列表
        :param um:
        :return:
        """
        return []

    def is_op(self, um):
        """
        获取直接下属列表
        :param um:
        :return:
        """
        return False

    def init_app(self, app):
        """
        初始化cmdb客户端
        """
        self.app = app
        self.host = self.app.config.get("CMDB_URL")
        self.secretid = self.app.config.get("CMDB_SECRET_ID")
        self.signature = self.app.config.get("CMDB_SIGNATURE")
        if not all([self.host, self.secretid, self.signature]):
            raise Exception(u"all CMDB_URL,CMDB_SECRET_ID,CMDB_SIGNATURE is required")

    def call_func(self, func, *args, **kwargs):
        """
        """
        return self.get_resource(func, *args, **kwargs)

    def __getattr__(self, name):
        return Automagic(self, [name])