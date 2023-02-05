'''
this script is the combination of `fetch_event.py` and `reply_event.py`,
it will reply every new post which contain specific keyword.
there are 2 commands in this script, `//help` and `//gas`
`//help` will return a simple help message,
`//gas` will return ethereum gas.
'''
import json
import ssl
import time
from nostr.filter import Filter, Filters
from nostr.event import EventKind, Event
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.key import PrivateKey

'''                    function                    '''
def is_spam_post(post_content):
    spam_keyword = [
        'Make sure you sub to my channel bras',
        'MemeBook', 
        'web3social',
        'web3社交+投研'
    ]
    for w in spam_keyword:
        if w in post_content:
            return True
    return False
'''                    function                    '''

filters = Filters(
    [Filter(since=int(time.time()),
            kinds=[EventKind.TEXT_NOTE])])  # enter filter condition
subscription_id = ''  # any string
request = [ClientMessageType.REQUEST, subscription_id]
request.extend(filters.to_json_array())

relay_manager = RelayManager()
relay_manager.add_relay('wss://relay.snort.social')  # add relay

relay_manager.add_subscription(subscription_id, filters)
relay_manager.open_connections(
    {'cert_reqs':
     ssl.CERT_NONE})  # NOTE: This disables ssl certificate verification
time.sleep(1.25)  # allow the connections to open

message = json.dumps(request)
relay_manager.publish_message(message)
time.sleep(1)  # allow the messages to send

while 1:
    while relay_manager.message_pool.has_events():
        event_msg = relay_manager.message_pool.get_event()

        if is_spam_post(event_msg.event.content) == False:
            if '//help' in event_msg.event.content: # help command
                print(event_msg.event.content)
                print(event_msg.event.id)
                private_key = PrivateKey.from_nsec(
                    'nsec1z0zvk9wvpa6e9m6gzk2fa2rhrp4ge9qtc2cjgmx4msfm3jj2g27s67m0px'
                )
                event = Event(
                    public_key=private_key.public_key.hex(),
                    content='this is a demo help command\nbot by xeift.eth\nhttps://github.com/Xeift/Nostr-Bot',  # message you want to send in the post
                    tags=[ ['e', event_msg.event.id, ''] ]  # the post id you want to reply. 'e' stands for event, read nip-01 for futher information.
                )
                private_key.sign_event(event)
    
                relay_manager.publish_event(event)
                time.sleep(1)# allow the messages to send

            if '//gas' in event_msg.event.content: # help command
                import requests
                url = 'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey='
                r = requests.get(url).json()['result']
   
                print(event_msg.event.content)
                print(event_msg.event.id)
                private_key = PrivateKey.from_nsec(
                    'nsec1cuwt3ffzrywnj7p73gewv3af93vc5huxd6mumpvl3kn8n907v0wq8782zk'
                )
                event = Event(
                    public_key=private_key.public_key.hex(),
                    content=f"🐢{r['SafeGasPrice']} 🚗{r['ProposeGasPrice']} 🚀{r['FastGasPrice']}\nbot by xeift.eth\nhttps://github.com/Xeift/Nostr-Bot",  # message you want to send in the post
                    tags=[
                        ['e', event_msg.event.id, '']
                    ]  # the post id you want to reply. 'e' stands for event, read nip-01 for futher information.
                )
                private_key.sign_event(event)
    
                relay_manager.publish_event(event)
                time.sleep(1)# allow the messages to send
                
            #if 'your_command_name12345' in event_msg.event.content:
                # print('add code here')
            else:# for debug
                print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(event_msg.event.created_at + 8 * 60 * 60))} {event_msg.event.content[:10]}')

relay_manager.close_connections()
print('finish')