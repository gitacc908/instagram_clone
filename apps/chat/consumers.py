import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from apps.chat.models import Room, Message
from apps.users.templatetags.user_tags import get_user_photo


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.user_inbox = None  # new

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['username']
        self.room_group_name = f'chat_{self.room_name}'
        print(self.scope['user'])

        self.room = Room.objects.get(name=self.room_name)
        self.user = self.scope['user']
        self.user_inbox = f'inbox_{self.user.username}'  # new

        # connection has to be accepted
        self.accept()
        print(self.room)
        
        if self.room_name == 'common':
            # join the room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name,
            )
        
        # im in my direct
        if self.room_name == self.user.username:
            # -------------------- new --------------------
                # create a user inbox for private messages
            async_to_sync(self.channel_layer.group_add)(
                self.user_inbox,
                self.channel_name,
            )
            # ---------------- end of new ----------------

        if self.room_name == 'common':
            # send the user list to the newly joined user
            self.send(json.dumps({
                'type': 'user_list',
                'users': [user.username for user in self.room.online.all()],
            }))
    
            # send the join event to the room
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'user': self.user.username,
                }
            )
            self.room.online.add(self.user)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )
        print('disconnected')

         
        if self.room_name == self.user.username: 
            # delete the user inbox for private messages
            async_to_sync(self.channel_layer.group_add)(
                self.user_inbox,
                self.channel_name,
            )
            # ---------------- end of new ----------------

        if self.room_name == 'common':
            # -------------------- new --------------------

            # send the leave event to the room
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'user': self.user.username,
                }
            )
            self.room.online.remove(self.user)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if not self.user.is_authenticated:
            return

        # # -------------------- new --------------------
        if message.startswith('/pm '):
            split = message.split(' ', 2)
            target = split[1]
            target_msg = split[2]
            # send private message to the target
            async_to_sync(self.channel_layer.group_send)(
                f'inbox_{target}',
                {
                    'type': 'private_message',
                    'user': {
                        'username': self.user.username,
                        'image': get_user_photo(self.user)
                    },
                    'message': target_msg,
                }
            )
            # send private message delivered to the user
            self.send(json.dumps({
                'type': 'private_message_delivered',
                'target': target,
                'message': target_msg,
            }))
            # return
        # ---------------- end of new ----------------

        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': {
                    'username': self.user.username,
                    'image': get_user_photo(self.user)
                },
                'message': message,
            }
        )
        # Message.objects.create(user=self.user, room=self.room, content=message)

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def user_join(self, event):
        self.send(text_data=json.dumps(event))

    def user_leave(self, event):
        self.send(text_data=json.dumps(event))

    def private_message(self, event):
        self.send(text_data=json.dumps(event))

    def private_message_delivered(self, event):
        self.send(text_data=json.dumps(event))



class PrivateChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.user_inbox = None  # new

    def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['username']
        # self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']
        self.user_inbox = f'inbox_{self.user.username}'
        self.room = Room.objects.get(name=self.user.username)

        # connection has to be accepted
        self.accept()
        print(self.room)
        
        # if self.room_name == 'common':
            # join the room group
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name,
        # )
        
            # -------------------- new --------------------
                # create a user inbox for private messages
        async_to_sync(self.channel_layer.group_add)(
            self.user_inbox,
            self.channel_name,
        )
            # ---------------- end of new ----------------
    

    def disconnect(self, close_code):
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name,
        #     self.channel_name,
        # )
        print('disconnected')

         
            # delete the user inbox for private messages
        async_to_sync(self.channel_layer.group_discard)(
            self.user_inbox,
            self.channel_name,
        )


    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if not self.user.is_authenticated:
            return

        print(self.user)

        # # -------------------- new --------------------
        if message.startswith('/pm '):
            print('message has been send')
            split = message.split(' ', 2)
            target = split[1]
            target_msg = split[2]
            # send private message to the target
            async_to_sync(self.channel_layer.group_send)(
                f'inbox_{target}',
                {
                    'type': 'private_message',
                    'user': {
                        'username': self.user.username,
                        'image': get_user_photo(self.user)
                    },
                    'message': target_msg,
                }
            )
            # send private message delivered to the user
            self.send(json.dumps({
                'type': 'private_message_delivered',
                'target': target,
                'message': target_msg,
            }))
            # return
        # ---------------- end of new ----------------

    def private_message(self, event):
        self.send(text_data=json.dumps(event))

    def private_message_delivered(self, event):
        self.send(text_data=json.dumps(event))