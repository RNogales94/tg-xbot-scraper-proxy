
import pymongo
from datetime import datetime
import os

print('Setting up config')
print(os.environ['MONGO_USER'])


class Xbotdb():
    def __init__(self):
        mongo_user = os.environ['MONGO_USER']
        mongo_pass = os.environ['MONGO_PASS']
        mongo_uri = f'mongodb://{mongo_user}:{mongo_pass}@frankfurt-xbot-shard-00-00-uoquw.mongodb.net:27017,frankfurt-xbot-shard-00-01-uoquw.mongodb.net:27017,frankfurt-xbot-shard-00-02-uoquw.mongodb.net:27017/test?ssl=true&replicaSet=Frankfurt-xbot-shard-0&authSource=admin&retryWrites=true'
        client = pymongo.MongoClient(mongo_uri)
        db = client.xbotdb
        self.products = db.get_collection('products')
        self.users = db.get_collection('users')

    def count_product(self):
        return self.products.count()

    def insert_product(self, product, use_timestamp=True, telegram_name=None):
        p = product.to_dict()

        if use_timestamp:
            p['timestamp'] = datetime.now().timestamp()
        if telegram_name is not None:
            p['origin'] = telegram_name

        self.products.insert_one(p)

    def get_products(self, skip=0, limit=20, origin=None, new_first=True):
        query_filter = {}
        projection = {'_id': 0}

        if origin is not None:
            query_filter = {'origin': origin}

        if new_first:
            natural = -1
        else:
            natural = 1

        results = self.products.find(query_filter, projection).sort('timestamp', natural).skip(skip)

        if limit is not None:
            results = results.limit(limit)

        return list(results)

    def get_chat_ids(self):
        chat_ids = list(self.users.find({}, {'_id': 0, 'chatId': 1}))
        chat_ids = [u.get('chatId', '') for u in chat_ids]
        return chat_ids

    def get_usernames_list(self):
        usernames = list(self.users.find({}, {'_id': 0, 'telegramName': 1}))
        usernames = [u['telegramName'] for u in usernames]
        return usernames

    def exist_user(self, telegram_name):
        user = self.users.find_one({'telegramName': telegram_name})
        return user is not None

    def get_user_type(self, telegram_name):
        type = self.users.find_one({'telegramName': telegram_name})['type']
        return type

    def insert_user(self, user):
        u = user.to_dict()
        self.users.insert_one(u)

    def update_user_tag(self, telegram_name, new_amazon_tag):
        self.users.update_one({'telegramName': telegram_name}, {"$set": {"amazonTag": new_amazon_tag}})

    def get_user_referral(self, telegram_name):
        return self.users.find_one({'telegramName': telegram_name})['referrals']

    def get_amazon_tag(self, telegram_name):
        user = self.users.find_one({'telegramName': telegram_name})
        if user is not None:
            amazon_tag = user['amazonTag']
        else:
            amazon_tag = None
        return amazon_tag

    def get_channels_associates(self, telegram_name):
        return self.users.find_one({'telegramName': telegram_name})['telegramChannels']


if __name__ == '__main__':
    client = pymongo.MongoClient(
        "mongodb://kay:myRealPassword@mycluster0-shard-00-00.mongodb.net:27017,mycluster0-shard-00-01.mongodb.net:27017,mycluster0-shard-00-02.mongodb.net:27017/admin?ssl=true&replicaSet=Mycluster0-shard-0&authSource=admin")
    db = client.test