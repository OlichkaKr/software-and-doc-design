import os
import re

from config import Session, engine, Base
from models import Comment, ContentBlock, Follow, PurchasePlan, PurchaseSettings, SiteSettings, User, Website

# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()


def get_or_create(session, model, **kwargs):
    # print(kwargs['id'])
    instance = session.query(model).filter_by(id=kwargs['id']).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def read_csv_file():
    # module_dir = os.path.dirname(__file__)
    file_path = os.path.join(os.path.dirname(__file__), 'generated.csv')
    with open(file_path, 'r+') as file:
        buffer = file.read()

        first = re.split(r'PurchasePlan\n', buffer)[1]
        sec = re.split(r'.*\nUser\n', first)[0]
        purchase_plans = sec.split('\n')
        for i in range(0, len(purchase_plans)):
            values = purchase_plans[i].split(',')
            if purchase_plans[i] != '':
                get_or_create(session, PurchasePlan, id=i+1, title=values[0], price=values[1], description=values[2])

        first = re.split(r'User\n', buffer)[1]
        sec = re.split(r'.*\nFollow\n', first)[0]
        users = sec.split('\n')
        for i in range(0, len(users)):
            values = users[i].split(',')
            if users[i] != '':
                get_or_create(session, User, id=i+1, first_name=values[0], last_name=values[1], public_display_name=values[2],
                                about_me=values[3], profile_link=values[4], email=values[5], password=values[6])

        first = re.split(r'Follow\n', buffer)[1]
        sec = re.split(r'.*\nPurchaseSettings\n', first)[0]
        followings = sec.split('\n')
        for i in range(0, len(followings)):
            values = followings[i].split(',')
            if followings[i] != '':
                get_or_create(session, Follow, id=i+1, id_follower=values[0], id_following=values[1])

        first = re.split(r'PurchaseSettings\n', buffer)[1]
        sec = re.split(r'.*\nWebsite\n', first)[0]
        purchase_settings = sec.split('\n')
        for i in range(0, len(purchase_settings)):
            values = purchase_settings[i].split(',')
            if purchase_settings[i] != '':
                get_or_create(session, PurchaseSettings, id=i+1, credit_card=values[0], id_user=values[1], id_plan=values[2])

        first = re.split(r'Website\n', buffer)[1]
        sec = re.split(r'.*\nContentBlock\n', first)[0]
        websites = sec.split('\n')
        for i in range(0, len(websites)):
            values = websites[i].split(',')
            if websites[i] != '':
                get_or_create(session, Website, id=i+1, title=values[0], id_author=values[1])

        first = re.split(r'ContentBlock\n', buffer)[1]
        sec = re.split(r'.*\nSiteSettings\n', first)[0]
        content_blocks = sec.split('\n')
        for i in range(0, len(content_blocks)):
            values = content_blocks[i].split(',')
            if content_blocks[i] != '':
                get_or_create(session, ContentBlock, id=i+1, image=values[0], text=values[1], id_website=values[2])

        first = re.split(r'SiteSettings\n', buffer)[1]
        sec = re.split(r'.*\nComment\n', first)[0]
        site_settings = sec.split('\n')
        for i in range(0, len(site_settings)):
            values = site_settings[i].split(',')
            if site_settings[i] != '':
                get_or_create(session, SiteSettings, id=i+1, visibility=values[0], permalink=values[1],
                            allow_comment=values[2], id_website=values[3])

        first = re.split(r'Comment\n', buffer)[1]
        comments = first.split('\n')
        for i in range(0, len(comments)):
            values = comments[i].split(',')
            if comments[i] != '':
                get_or_create(session, Comment, id=i+1, body=values[0], timestamp=values[1],
                            id_author=values[2], id_website=values[3])


if __name__ == "__main__":
    read_csv_file()