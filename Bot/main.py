'''
this script will reply every new post which contain specific keyword or execute command
'''
import ssl
import json
import time

from nostr.filter import Filter, Filters
from nostr.event import EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType

from spam_filter import is_spam_post
from commands import execute_cmds
from responses import execute_resp

filters = Filters([  # enter filter condition
    Filter(
        since=int(time.time()),
        kinds=[EventKind.TEXT_NOTE]
    )
])
subscription_id = ''  # any string
request = [
    ClientMessageType.REQUEST, 
    subscription_id
]
request.extend(filters.to_json_array())

relay_manager = RelayManager()
# relay_manager.add_relay('wss://relay.snort.social')  # add relay
relay_manager.add_relay('wss://nostr-pub.wellorder.net')  # add relay
relay_manager.add_subscription(subscription_id, filters)
relay_manager.open_connections({'cert_reqs': ssl.CERT_NONE})  # NOTE: This disables ssl certificate verification
time.sleep(1.25)  # allow the connections to open

message = json.dumps(request)
relay_manager.publish_message(message)
time.sleep(1)  # allow the messages to send
print('bot online')

while 1:
    while relay_manager.message_pool.has_events():
        event_msg = relay_manager.message_pool.get_event()

        if is_spam_post(event_msg.event.content):
            print('spam post blocked')
            continue
            
        execute_cmds(event_msg, relay_manager)
        execute_resp(event_msg, relay_manager)

        print("\n--------------------")
        # print(event_msg.event.public_key)
        # print(event_msg.event.id)
        # print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(event_msg.event.created_at + 8 * 60 * 60))} {event_msg.event.content[:20]}')
        print(event_msg.event.content[0:30])
        print("--------------------\n")
        
relay_manager.close_connections()
print('finish')