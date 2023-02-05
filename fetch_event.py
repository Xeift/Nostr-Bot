'''
this script will get all new post from selected relay.
'''
import json
import ssl
import time
from nostr.filter import Filter, Filters
from nostr.event import EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType

filters = Filters([Filter(since=int(time.time()), kinds=[EventKind.TEXT_NOTE])])# enter filter condition
subscription_id = ''# any string
request = [ClientMessageType.REQUEST, subscription_id]
request.extend(filters.to_json_array())

relay_manager = RelayManager()
relay_manager.add_relay('wss://relay.snort.social')# add relay

relay_manager.add_subscription(subscription_id, filters)
relay_manager.open_connections({'cert_reqs': ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
time.sleep(1.25)# allow the connections to open

message = json.dumps(request)
relay_manager.publish_message(message)
time.sleep(1)# allow the messages to send

while relay_manager.message_pool.has_events():
    event_msg = relay_manager.message_pool.get_event()
    print(event_msg.event.content)
    print(event_msg.event.id)
    time.sleep(3)
  
relay_manager.close_connections()
print('finish')