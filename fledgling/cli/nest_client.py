# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from requests import request

from fledgling.app.entity.plan import Plan
from fledgling.app.entity.task import Task
from fledgling.repository.nest_gateway import INestGateway


class IEnigmaMachine(ABC):
    @abstractmethod
    def decrypt(self, cipher_text):
        pass

    @abstractmethod
    def encrypt(self, plain_text):
        pass


class NestClient(INestGateway):
    def __init__(self, *, hostname, enigma_machine, port, protocol):
        assert isinstance(enigma_machine, IEnigmaMachine)
        self.cookies = None
        self.enigma_machine = enigma_machine
        self.url_prefix = '{}://{}:{}'.format(protocol, hostname, port)

    def login(self, *, email, password):
        response = request(
            json={
                'email': email,
                'password': password,
            },
            method='POST',
            url='{}/user/login'.format(self.url_prefix),
        )
        self.cookies = response.cookies

    def plan_create(self, *, repeat_type=None, task_id, trigger_time) -> int:
        json = {
            'repeat_type': repeat_type,
            'task_id': task_id,
            'trigger_time': trigger_time,
        }
        url = '{}/plan'.format(self.url_prefix)
        response = request(
            cookies=self.cookies,
            json=json,
            method='POST',
            url=url,
        )
        return response.json()['id']

    def plan_list(self, *, page, per_page):
        params = {
            'page': page,
            'per_page': per_page,
        }
        url = '{}/plan'.format(self.url_prefix)
        response = request(
            cookies=self.cookies,
            method='GET',
            params=params,
            url=url,
        )
        plans = response.json()['plans']
        return [Plan.new(
            id_=plan['id'],
            repeat_type=plan['repeat_type'],
            task_id=plan['task_id'],
            trigger_time=plan['trigger_time'],
        ) for plan in plans]

    def plan_pop(self):
        url = '{}/plan/pop'.format(self.url_prefix)
        json = {
            'size': 1,
        }
        response = request(
            cookies=self.cookies,
            json=json,
            method='POST',
            url=url,
        )
        print('response.json()', response.json())
        plans = response.json()['plans']
        if len(plans) == 0:
            return None
        return Plan.new(
            task_id=plans[0]['task_id'],
            trigger_time=plans[0]['trigger_time'],
        )

    def task_create(self, *, brief):
        url = '{}/task'.format(self.url_prefix)
        crypted_brief = self.enigma_machine.encrypt(brief)
        response = request(
            cookies=self.cookies,
            json={
                'brief': crypted_brief,
            },
            method='POST',
            url=url,
        )
        id_ = response.json()['id']
        return id_

    def task_get_by_id(self, id_):
        url = '{}/task/{}'.format(self.url_prefix, id_)
        response = request(
            cookies=self.cookies,
            method='GET',
            url=url,
        )
        task = response.json()['task']
        if not task:
            return None
        brief = self.enigma_machine.decrypt(task['brief'])
        return Task.new(
            brief=brief,
            id_=task['id'],
        )

    def task_list(self, *, page, per_page):
        params = {
            'page': page,
            'per_page': per_page,
        }
        url = '{}/task'.format(self.url_prefix)
        response = request(
            cookies=self.cookies,
            params=params,
            method='GET',
            url=url,
        )
        tasks = response.json()['tasks']
        return [Task.new(
            brief=self.enigma_machine.decrypt(task['brief']),
            id_=task['id'],
        ) for task in tasks]
