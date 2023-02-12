'''bot will respond to post which contain keyword in NORMAL_RESPONSE_DATA'''
import os
import time

from nostr.event import Event
from nostr.key import PrivateKey

NOSTR_PRIVATE_KEY = PrivateKey.from_nsec(os.environ['NOSTR_PRIVATE_KEY'])
NOSTR_PUBLICE_KEY = NOSTR_PRIVATE_KEY.public_key.hex()
AUTHOR_INFO = '\nbot by xeift.eth\nhttps://github.com/Xeift/Nostr-Bot'
NORMAL_RESPONSE_DATA = {
    "GM": "Good Morning!\nhttps://www.vobss.com/wp-content/uploads/2021/12/good-morning-anime-meme-vobss-9.jpg",
    "Hello": "Hello!\nhttps://media.tenor.com/3g3D1mECft0AAAAC/anime-hi.gif",
    "GN": "Good Night! Have a good dream\nhttps://pbs.twimg.com/media/EPMSrKIWsAE3PdD.jpg"
}

'''----------------------------------------FUNCTIONS----------------------------------------'''
def execute_resp(event_msg, relay_manager):
    if event_msg.event.public_key == NOSTR_PUBLICE_KEY or event_msg.event.public_key == 'ee8bf9594fbf8a3ed277b9fb60da8d963f7fd2f889315163761c90e91ca71277': return False # do not reply to messages sent by ourself
    for keyword in NORMAL_RESPONSE_DATA:
        if keyword in event_msg.event.content: normal_response(event_msg, relay_manager, NORMAL_RESPONSE_DATA[keyword])

        
def sign_and_publish_event(event, relay_manager):
    NOSTR_PRIVATE_KEY.sign_event(event)
    relay_manager.publish_event(event)
    time.sleep(1)# allow the messages to send
'''----------------------------------------FUNCTIONS----------------------------------------'''



'''----------------------------------------RESPONSES----------------------------------------'''
def normal_response(event_msg, relay_manager, resp):
    event = Event(
        public_key = NOSTR_PUBLICE_KEY,
        content = f'#[1]\n{resp}{AUTHOR_INFO}',  # message you want to send in the post
        tags = [
            ['e', event_msg.event.id, ''], # the post id you want to reply. 'e' stands for "event", read nip-01 for futher information.
            ['p', event_msg.event.public_key, ''] # the user you want to mention. 'p' stands for "pubkey", read nip-08 for futher information.
        ]
    )
    sign_and_publish_event(event, relay_manager)
'''----------------------------------------RESPONSES----------------------------------------'''
