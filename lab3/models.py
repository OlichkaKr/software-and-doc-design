from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from config import session, Base


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    public_display_name = Column(String, nullable=False)
    about_me = Column(String)
    profile_link = Column(String)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    followers = relationship('Follow', foreign_keys='Follow.id_follower', back_populates='follower')
    following_users = relationship('Follow', foreign_keys='Follow.id_following', back_populates='following')
    purchase = relationship('PurchaseSettings', back_populates='user')
    sites = relationship('Website', back_populates='author')
    comments = relationship('Comment', back_populates='author')

    def __init__(self, first_name, last_name, public_display_name, about_me, profile_link, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.public_display_name = public_display_name
        self.about_me = about_me
        self.profile_link = profile_link
        self.email = email
        self.password = password


    @staticmethod
    def post_data(data):
        check = session.query(User).filter_by(public_display_name=data['public_display_name'])
        if check == None:
            raise Exception('This username is in use. Please, enter another username')
        else:
            public_display_name = data['public_display_name']
            last_user = session.query(User).order_by(User.id.desc()).first()
            session.add(User(first_name=data["first_name"], last_name=data['last_name'], public_display_name=public_display_name,
                               about_me=data['about_me'], profile_link=data['profile_link'], email=data['email'], password=data['password']))
            session.commit()
            last_user = session.query(User).order_by(User.id.desc()).first()
            session.add(PurchaseSettings(id=last_user.id, credit_card='', id_user=last_user.id, id_plan=1))
            session.commit()
        

    def put_data(self, data):
        if data['first_name']:
            self.first_name = data['first_name']
        if data['last_name']:
            self.last_name = data['last_name']
        if data['public_display_name']:
            self.public_display_name = data['public_display_name']
        if data['about_me']:
            self.about_me = data['about_me']
        if data['profile_link']:
            self.profile_link = data['profile_link']
        if data['email']:
            self.email = data['email']
        if data['password']:
            self.password = data['password']
        print(self.last_name)
        session.commit()

    def delete_data(self):
        for uf in self.followers:
            session.delete(uf)
            session.commit
        for ufu in self.following_users:
            session.delete(ufu)
            session.commit()
        session.delete(session.query(PurchaseSettings).filter_by(id_user=self.id).first())
        session.commit()
        for s in self.sites:
            session.delete(s)
            session.commit()
        session.delete(self)
        session.commit()

    def serialize(self):
        

        return {
            'id': self.id,
            'serial_number': self.serial_number,
            'country':  loc.country,
            'city': loc.city,
            'address': loc.address,
            'room_name': loc.room_name,
            'connection_type': conn.connection_type
        }


class Follow(Base):
    __tablename__ = 'Follow'

    id = Column(Integer, primary_key=True)
    id_follower = Column(Integer, ForeignKey('User.id'))
    follower = relationship(User, foreign_keys='Follow.id_follower', back_populates='followers')
    id_following = Column(Integer, ForeignKey('User.id'))
    following = relationship(User, foreign_keys='Follow.id_following', back_populates='following_users')
    
    def __init__(self, id, id_follower, id_following):
        self.id = id
        self.id_follower = id_follower
        self.id_following = id_following


class PurchaseSettings(Base):
    __tablename__ = 'PurchaseSettings'

    id = Column(Integer, primary_key=True)
    credit_card = Column(Integer)
    id_user = Column(Integer, ForeignKey('User.id'))
    user = relationship('User', back_populates='purchase')
    id_plan = Column(Integer, ForeignKey('PurchasePlan.id'))
    plan = relationship('PurchasePlan', back_populates='purcaseSettings')

    def __init__(self, id, credit_card, id_user, id_plan):
        self.id = id
        self.credit_card = credit_card
        self.id_user = id_user
        self.id_plan = id_plan


class PurchasePlan(Base):
    __tablename__ = 'PurchasePlan'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    purcaseSettings = relationship('PurchaseSettings', back_populates='plan')

    def __init__(self, id, title, price, description):
        self.id = id
        self.title = title
        self.price = price
        self.description = description


class ContentBlock(Base):
    __tablename__ = 'ContentBlock'

    id = Column(Integer, primary_key=True)
    image = Column(String)
    text = Column(String)
    site = relationship('Website')
    id_website = Column(Integer, ForeignKey('Website.id'))
    website = relationship('Website', back_populates='content_blocks')

    def __init__(self, id, image, text, id_website):
        self.id = id
        self.image = image
        self.text = text
        self.id_website = id_website


class Website(Base):
    __tablename__ = 'Website'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    id_author = Column(Integer, ForeignKey('User.id'))
    author = relationship('User', back_populates='sites')
    content_blocks = relationship('ContentBlock', back_populates='website')
    site_settings = relationship('SiteSettings', back_populates='website')
    comments = relationship('Comment', back_populates='website')

    def __init__(self, id, title, id_author):
        self.id = id
        self.title = title
        self.id_author = id_author


class SiteSettings(Base):
    __tablename__ = 'SiteSettings'

    id = Column(Integer, primary_key=True)
    visibility = Column(String, nullable=False)
    permalink = Column(String)
    allow_comment = Column(Integer, nullable=False)
    id_website = Column(Integer, ForeignKey('Website.id'))
    website = relationship('Website', back_populates='site_settings')

    def __init__(self, id, visibility, permalink, allow_comment, id_website):
        self.id = id
        self.visibility = visibility
        self.permalink = permalink
        self.allow_comment = allow_comment
        self.id_website = id_website


class Comment(Base):
    __tablename__ = 'Comment'

    id = Column(Integer, primary_key=True)
    body = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    id_author = Column(Integer, ForeignKey('User.id'))
    author = relationship('User', back_populates='comments')
    id_website = Column(Integer, ForeignKey('Website.id'))
    website = relationship('Website', back_populates='comments')

    def __init__(self, id, body, timestamp, id_author, id_website):
        self.id = id
        self.body = body
        self.timestamp = timestamp
        self.id_author = id_author
        self.id_website = id_website