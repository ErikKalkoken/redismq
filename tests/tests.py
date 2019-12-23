import os
import sys
import inspect
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
sys.path.append(parentdir)

import unittest
from redis import Redis

from redismq import RedisMQ

class TestPQueue(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestPQueue, cls).setUpClass()

        conn = Redis()
        cls.q = RedisMQ(conn, 'test_queue_0815')

    def setUp(self):
        # empty queue
        while True:
            y = self.q.dequeue()
            if y is None:
                break;
        

    def test_empty_queue_returns_none(self):
        self.assertIsNone(self.q.dequeue())

    def test_empty_queue_has_length_0(self):
        self.assertEqual(self.q.size, 0)

    def test_queue_dequque_one_empty(self):
        x = 'precious'
        self.q.enqueue(x)
        self.assertEqual(self.q.size, 1)
        y = self.q.dequeue()
        self.assertEqual(x, y)


    def test_queue_dequque_one_full(self):
        self.q.enqueue('dummy_100')
        self.q.enqueue('dummy_101')
        self.q.enqueue('dummy_102')
        q_size = self.q.size
        x = 'precious'
        self.q.enqueue(x)
        self.assertEqual(self.q.size, q_size + 1)


    def test_queue_dequque_many(self):
        x_list = ['apple', 'kiwi', 'lemon']
        for x in x_list:
            self.q.enqueue(x)
        self.assertEqual(self.q.size, len(x_list))
        
        y_list = list()
        while True:
            y = self.q.dequeue()
            if y is not None:
                y_list.append(y)
            else:
                break;
        
        self.assertListEqual(x_list, y_list)


    def test_enqueue_bulk(self):
        x_list = ['apple', 'kiwi', 'lemon']
        self.q.enqueue_bulk(x_list)

        y_list = list()
        while True:
            y = self.q.dequeue()
            if y is not None:
                y_list.append(y)
            else:
                break;
        
        self.assertListEqual(x_list, y_list)


    def test_dequque_bulk_normal(self):
        x_list = ['apple', 'kiwi', 'lemon']
        self.q.enqueue_bulk(x_list)
        y_list = self.q.dequeue_bulk()
        self.assertListEqual(x_list, y_list)


    def test_dequque_bulk_empty_queue(self):
        self.assertListEqual(self.q.dequeue_bulk(), [])

    def test_dequque_bulk_limited(self):
        x_list = ['apple', 'kiwi', 'lemon']
        self.q.enqueue_bulk(x_list)
        y_list = self.q.dequeue_bulk(2)
        self.assertListEqual(x_list[:2], y_list)


if __name__ == "__main__":
    unittest.main()