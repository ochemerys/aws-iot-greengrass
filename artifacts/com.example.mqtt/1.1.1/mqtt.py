from awsiot import greengrasscoreipc
from awsiot.greengrasscoreipc import client as Client
from awsiot.greengrasscoreipc.model import (
    IoTCoreMessage,
    QOS,
    SubscribeToIoTCoreRequest,
    PublishToIoTCoreRequest
)

print("---connecting---")
client = greengrasscoreipc.connect()
print("---connected---")

echo_response_topic = "test/send"

def send_iot_core_message(topic: str, message: str):
    try:
        request = PublishToIoTCoreRequest()
        request.topic_name = topic
        request.payload = bytes(message, "utf-8")
        request.qos = QOS.AT_MOST_ONCE
        operation = client.new_publish_to_iot_core()
        operation.activate(request)

        print("Publishing")
        future = operation.get_response()
        future.result(10)
        print("Published")
    except Exception as e:
        print(e)


#Code to subscribe to topic from 
class SubscriptionHandler(Client.SubscribeToIoTCoreStreamHandler):
    def __init__(self):
        super().__init__()

    def on_stream_event(self, event: IoTCoreMessage) -> None:
        try:
            print('----- on sub event -----')
            message = str(event.message.payload, "utf-8")
            topic_name = event.message.topic_name
            print(f"Received message {message} on topic {topic_name}")

            print(f"Received message on topic {topic_name}. Forwarding to {echo_response_topic}")
            send_iot_core_message(topic=echo_response_topic, message=message)
        except Exception as e:
            print(e)

    def on_stream_error(self, error: Exception) -> bool:
        # Handle error.
        print("----- error ------")
        return True  # Return True to close stream, False to keep stream open.

    def on_stream_closed(self) -> None:
        # Handle close.
        print("----- closed -----")
        pass

request = SubscribeToIoTCoreRequest()
request.topic_name = "test/receive"
request.qos = QOS.AT_MOST_ONCE
handler = SubscriptionHandler()
operation = client.new_subscribe_to_iot_core(handler)

print("Subscribing")
future = operation.activate(request)
future.result(10)
print("Subscribed!")

# Keep the main thread alive, or the process will exit.
while True:
    #time.sleep(10)
    pass
