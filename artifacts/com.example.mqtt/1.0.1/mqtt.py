from awsiot import greengrasscoreipc
from awsiot.greengrasscoreipc import client as Client
from awsiot.greengrasscoreipc.model import (
    IoTCoreMessage,
    QOS,
    SubscribeToIoTCoreRequest
)

print("---connecting---")
client = greengrasscoreipc.connect()
print("---connected---")

#Code to subscribe to topic from 
class SubscriptionHandler(Client.SubscribeToIoTCoreStreamHandler):
    def __init__(self):
        super().__init__()

    def on_stream_event(self, event: IoTCoreMessage) -> None:
        try:
            message = str(event.message.payload, "utf-8")
            topic_name = event.message.topic_name
            print(f"Received message {message} on topic {topic_name}")
            # # Handle message.
            # jsonmsg = json.loads(message)

        except:
            pass

    def on_stream_error(self, error: Exception) -> bool:
        # Handle error.
        print("----- error ------")
        return True  # Return True to close stream, False to keep stream open.

    def on_stream_closed(self) -> None:
        # Handle close.
        print("----- closed -----")
        pass

request = SubscribeToIoTCoreRequest()
request.topic_name = "mqtt/pi"
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
