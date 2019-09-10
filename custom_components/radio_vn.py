##=== Play radio VN by exlab ===#
##=== version 1.0 07/02/2019 ===#

##==================#
##Config in configuration.yaml file for Home Assistant
##radio_vn:
##
##Code in script
##play_radiovn:
##  sequence:
##    - service: radio_vn.play
##      data:
##        entity_id: media_player.room_player
##        channel: 'VOV2' # optional, default: 'VOV3' #list channel: VOV1, VOV2, VOV3, VOVGT-HN, VOVGT-HCM

# Declare variables
DOMAIN = 'radio_vn'
SERVICE_RADIO_PLAY = 'play'

# data service
CONF_PLAYER_ID = 'entity_id'
CONF_CHANNEL= 'channel'

# const data
url = {'VOV1':'https://vov.vn/RadioPlayer.vov?c=vov1', 'VOV2':'https://vov.vn/RadioPlayer.vov?c=vov2', 'VOV3':'https://vov.vn/RadioPlayer.vov?c=vov3', 'VOVGT-HN':'https://vov.vn/RadioPlayer.vov?c=vovgt', 'VOVGT-HCM':'https://vov.vn/RadioPlayer.vov?c=vovgtsg'}
prefix_url = 'https://5a6872aace0ce.streamlock.net/'
match_text = 'MakeRadio'

import requests
def get_link_radio(_channel):
    res = requests.get(url.get(_channel)).text
    i = res.find(match_text)
    ii = res.find(';',i)
    ext_url = (res[i:ii].split(',')[1].replace("'","").strip())
    radio_link = prefix_url + ext_url
    return radio_link

def setup(hass, config):

    def play_radio(data_call):
        # Get data service
        media_id = data_call.data.get(CONF_PLAYER_ID)
        print(media_id)
        channel  = str(data_call.data.get(CONF_CHANNEL, 'VOV3'))
        print(channel)
        # get link of radio
        uri = get_link_radio(channel)
        print(uri)
        # service data for 'CALL SERVICE' in Home Assistant
        service_data = {'entity_id': media_id, 'media_content_id': uri, 'media_content_type': 'audio/mp3'}
        # Call service from Home Assistant
        hass.services.call('media_player', 'play_media', service_data)
        
    hass.services.register(DOMAIN, SERVICE_RADIO_PLAY, play_radio)
    return True
