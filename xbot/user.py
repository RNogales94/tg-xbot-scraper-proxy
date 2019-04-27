import hashlib
from datetime import datetime


def create_token(user_name):
    hasher = hashlib.sha256()
    hasher.update(user_name.encode())
    return hasher.hexdigest()


class User:
    """
    Examples
    telegram_name: RNogales
    telegram_channels: ['@canalejemplo', '@chollos']
    """
    def __init__(self, telegram_name=None, chat_id=None, amazon_tag=None, telegram_channels=[], referrals=[]):
        self.telegram_name = telegram_name
        self.amazon_tag = amazon_tag
        self.type = 'free'
        self.telegram_channels = telegram_channels
        self.token = create_token(self.telegram_name)
        self.chat_id = chat_id
        self.creation_timestamp = datetime.now().timestamp()
        self.referrals = referrals
        self.last_modify = self.creation_timestamp

    def __str__(self):
        return f'User: [{self.telegram_name}, {self.amazon_tag}, {self.telegram_channels},{self.referrals}, {self.token} ]'

    def to_dict(self):
        u = {'telegramName': self.telegram_name,
             'amazonTag': self.amazon_tag,
             'telegramChannels': self.telegram_channels,
             'referrals': self.referrals,
             'token': self.token,
             'chatId': self.chat_id,
             'creationTimestamp': self.creation_timestamp,
             'lastModify': self.last_modify,
             }
        return u



