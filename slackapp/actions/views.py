from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.http import HttpResponse, JsonResponse
import slack
from .praw_logic import praw_query


@csrf_exempt
def event_hook(request):
    client = slack.WebClient(token=settings.BOT_USER_ACCESS_TOKEN)
    json_dict = json.loads(request.body.decode('utf-8'))
    print(json_dict)
    if json_dict['token'] != settings.VERIFICATION_TOKEN:
        return HttpResponse(status=403)

    if 'type' in json_dict:
        if json_dict['type'] == 'url_verification':
            response_dict = {"challenge": json_dict['challenge']}
            return JsonResponse(response_dict, safe=False)

    if 'event' in json_dict:
        print(json_dict)
        event_msg = json_dict['event']
        if ('subtype' in event_msg) and (event_msg['subtype'] == 'bot_message'):
            return HttpResponse(status=200)

        if event_msg['type'] == 'message':
            user = event_msg['user']
            channel = event_msg['channel']
            praw_query(event_msg['text'])

            response_msg = ":wave:, An ELI5 response <@%s>" % praw_query(
                event_msg['text'])
            client.chat_postMessage(channel=channel, text=response_msg)
            return HttpResponse(status=200)
    return HttpResponse(status=200)


{'token': 'vn1Nm3JnE0X7ocZOv2T8xzws', 'team_id': 'T013ADFGK4L', 'api_app_id': 'A012Y4MC17Z',
 'event': {'client_msg_id': 'f0c859f5-8d5c-4abc-ad9e-e89cbcb73ae1', 'type': 'message', 'text': 'transformer', 'user': 'U013U3E7JPJ', 'ts': '1589159493.011400', 'team': 'T013ADFGK4L',
           'blocks': [{'type': 'rich_text', 'block_id': 'UwGV1', 'elements': [{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'transformer'}]}]}],
           'channel': 'D012Y4Q56MV', 'event_ts': '1589159493.011400', 'channel_type': 'im'},
 'type': 'event_callback', 'event_id': 'Ev013D5NNFJP', 'event_time': 1589159493, 'authed_users': ['U013BFCCZEH']}
