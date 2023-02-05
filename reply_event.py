'''
this script will login with your private key and reply to specific post.
'''
import ssl
import time
from nostr.event import Event
from nostr.relay_manager import RelayManager
from nostr.key import PrivateKey

relay_manager = RelayManager()
relay_manager.add_relay('wss://relay.snort.social')
relay_manager.open_connections({'cert_reqs': ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
time.sleep(1.25)# allow the connections to open

private_key = PrivateKey.from_nsec('nsec1z0zvk9wvpa6e9m6gzk2fa2rhrp4ge9qtc2cjgmx4msfm3jj2g27s67m0px')
# private_key = PrivateKey(bytes(bytearray.fromhex('e9e58ae4f3a43fd4917a05f8e33f7ef4b53a9ec21992f48523a14593766dc51a')))
print(private_key)

event = Event(
    public_key = private_key.public_key.hex(), 
    content = 'this is a demo reply script\nbot by xeift.eth\nhttps://github.com/Xeift/Nostr-Bot',# message you want to send in the post
    tags = [ ['e','8de408a85f7d36f19568d2c2b80bacbe21e74dbd5ed7351e422cf5829b8c75ba',''] ]# the post id you want to reply. 'e' stands for event, read nip-01 for futher information.
)
private_key.sign_event(event)

relay_manager.publish_event(event)
time.sleep(1)# allow the messages to send

relay_manager.close_connections()
print('finish')