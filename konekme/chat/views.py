from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
# Create your views here.


#Required in receiving and sending messages
import json, requests, random, re
from pprint import pprint
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

verify_token = '5244680129'
page_access_token = 'EAACscMDU9jMBAO3ZBn9kaHTu6k2gzpqZCshlqvRCKjTPSZCHv8arv6wATx0ZCFCLPWG63icCPRZBpRHVrUdC7xap8dZChwHkGEZBZAdt4GYjAEQJIOekfDApYmgj2lqncmdKkBtkN101BTzM028fAUfwgB3Ek19IOP7xJnUvq9f2zgZDZD'

class index(generic.View):
    def get(self, request, *args, **kwargs):
            if self.request.GET['hub.verify_token']  == '5244680129':
                return HttpResponse(self.request.GET['hub.challenge'])
            else:
                return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    pprint(message)
                    post_facebook_messages(message['sender']['id'], message['message']['text'])
        return HttpResponse()

def post_facebook_messages(fbid, received_messages):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+page_access_token
    response_msg = json.dumps({"recipient": {"id":fbid}, "message":{"text":received_messages}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())
