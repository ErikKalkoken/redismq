from redis import Redis
from redismq import RedisMQ

conn = Redis()
q = RedisMQ(conn, 'example_queue')
q.enqueue('Hello, World!')
message = q.dequeue()
print(message)
