# Redis Message Queue

This package contains a simple FIFO message queue based on Redis.

![license](https://img.shields.io/github/license/ErikKalkoken/redismq) ![python](https://img.shields.io/badge/python-3.5%20|%203.6%20|%203.7%20|%203.8-informational) ![build](https://api.travis-ci.org/ErikKalkoken/redismq.svg?branch=master) [![codecov](https://codecov.io/gh/ErikKalkoken/redismq/branch/master/graph/badge.svg)](https://codecov.io/gh/ErikKalkoken/redismq)

## Basic example

```python
from redis import Redis
from redismq import RedisMQ

conn = Redis()
q = RedisMQ(conn, 'example_queue')
q.enqueue('Hello, World!')
message = q.dequeue()
print(message)
```

See also the examples folder for examples.
