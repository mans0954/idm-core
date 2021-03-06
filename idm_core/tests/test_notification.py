import json

import kombu
from django.apps import apps
from django.db import transaction
from django.test import TransactionTestCase
from kombu.message import Message

from idm_core.person.models import Person


class NotificationTestCase(TransactionTestCase):
    fixtures = ['initial']

    def setUp(self):
        self.broker = apps.get_app_config('idm_broker').broker

    def testPersonCreate(self):
        with self.broker.acquire(block=True) as conn:
            queue = kombu.Queue(exclusive=True).bind(conn)
            queue.declare()
            queue.bind_to(exchange=kombu.Exchange('idm.core.person'), routing_key='#')
            with transaction.atomic():
                person = Person()
                person.save()
            message = queue.get()
            self.assertIsInstance(message, Message)
            self.assertEqual(message.delivery_info['routing_key'],
                             'Person.created.{}'.format(str(person.id)))
            self.assertEqual(message.content_type, 'application/json')
            self.assertEqual(json.loads(message.body.decode())['@type'], 'Person')

    def testPersonCreateDelete(self):
        with self.broker.acquire(block=True) as conn:
            queue = kombu.Queue(exclusive=True).bind(conn)
            queue.declare()
            queue.bind_to(exchange=kombu.Exchange('idm.core.person'), routing_key='#')
            with transaction.atomic():
                person = Person()
                person.save()
                person.delete()
            message = queue.get()
            self.assertIsNone(message)

    def testNoNotifcationWhenNotChanged(self):
        with self.broker.acquire(block=True) as conn:
            with transaction.atomic():
                person = Person()
                person.save()
            queue = kombu.Queue(exclusive=True).bind(conn)
            queue.declare()
            queue.bind_to(exchange=kombu.Exchange('idm.core.person'), routing_key='#')
            with transaction.atomic():
                person.save()
            message = queue.get()
            self.assertIsNone(message)

    def testNotifcationWhenChanged(self):
        with self.broker.acquire(block=True) as conn:
            with transaction.atomic():
                person = Person()
                person.save()
            queue = kombu.Queue(exclusive=True).bind(conn)
            queue.declare()
            queue.bind_to(exchange=kombu.Exchange('idm.core.person'), routing_key='#')
            with transaction.atomic():
                person.deceased = True
                person.save()
            message = queue.get()
            self.assertIsInstance(message, Message)
            self.assertEqual(message.delivery_info['routing_key'],
                             'Person.changed.{}'.format(str(person.id)))
            self.assertEqual(message.content_type, 'application/json')
            self.assertEqual(json.loads(message.body.decode())['deceased'], True)
