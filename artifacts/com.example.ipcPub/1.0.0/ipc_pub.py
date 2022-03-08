import time

import awsiot.greengrasscoreipc
from awsiot.greengrasscoreipc.model import (
    PublishToTopicRequest,
    PublishMessage,
    BinaryMessage
)

ipc_client = awsiot.greengrasscoreipc.connect()

topic = "ipc/pi"
message = "ipc pub event"
TIMEOUT = 10

def publish_event():
    print('button pressed')
    request = PublishToTopicRequest()
    request.topic = topic
    publish_message = PublishMessage()
    publish_message.binary_message = BinaryMessage()
    publish_message.binary_message.message = bytes(message, "utf-8")
    request.publish_message = publish_message
    operation = ipc_client.new_publish_to_topic()
    operation.activate(request)
    future = operation.get_response()
    future.result(TIMEOUT)


print("pub event started")

t_end = time.time() + 60 * 60
seconds = 0
start = time.time()
while time.time() < t_end:
    end = time.time()
    if end - start >= 1:
        start = end
        seconds += 1
        publish_event()
        print("---- event seconds {} published -----".format(seconds))
