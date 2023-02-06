import os
import time
import requests

from nostr.event import Event
from nostr.key import PrivateKey

NOSTR_PRIVATE_KEY = PrivateKey.from_nsec(os.environ['NOSTR_PRIVATE_KEY'])
NOSTR_PUBLICE_KEY = NOSTR_PRIVATE_KEY.public_key.hex()
ETHERSCAN_API_KEY = os.environ['ETHERSCAN_API_KEY']
AUTHOR_INFO = '\nbot by xeift.eth\nhttps://github.com/Xeift/Nostr-Bot'

'''----------------------------------------FUNCTIONS----------------------------------------'''
def execute_cmds(event_msg, relay_manager):
    if event_msg.event.public_key == NOSTR_PUBLICE_KEY: return False # do not reply to messages sent by ourself
    if event_msg.event.content == '//help': help(event_msg, relay_manager)
    elif event_msg.event.content == '//gas': gas(event_msg, relay_manager)

        
def sign_and_publish_event(event, relay_manager):
    NOSTR_PRIVATE_KEY.sign_event(event)
    relay_manager.publish_event(event)
    time.sleep(1)# allow the messages to send
'''----------------------------------------FUNCTIONS----------------------------------------'''



'''----------------------------------------COMMANDS----------------------------------------'''
def help(event_msg, relay_manager):
    event = Event(
        public_key = NOSTR_PUBLICE_KEY,
        content = f'#[1]\nhelp command!{AUTHOR_INFO}',  # message you want to send in the post
        tags = [
            ['e', event_msg.event.id, ''], # the post id you want to reply. 'e' stands for "event", read nip-01 for futher information.
            ['p', event_msg.event.public_key, ''] # the user you want to mention. 'p' stands for "pubkey", read nip-08 for futher information.
        ]
    )
    sign_and_publish_event(event, relay_manager)


def gas(event_msg, relay_manager):
    url = f'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}'
    r = requests.get(url).json()['result']
    event = Event(
        public_key = NOSTR_PUBLICE_KEY,
        content = f"#[1]\nEthereum gas:\n🐢{r['SafeGasPrice']} 🚗{r['ProposeGasPrice']} 🚀{r['FastGasPrice']}{AUTHOR_INFO}",  # message you want to send in the post
        tags = [
            ['e', event_msg.event.id, ''], # the post id you want to reply. 'e' stands for "event", read nip-01 for futher information.
            ['p', event_msg.event.public_key, ''] # the user you want to mention. 'p' stands for "pubkey", read nip-08 for futher information.
        ]
    )
    sign_and_publish_event(event, relay_manager)
'''----------------------------------------COMMANDS----------------------------------------'''