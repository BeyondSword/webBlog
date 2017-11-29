from playhouse.flask_utils import (FlaskDB)
from playhouse.sqlite_ext import *
from peewee import *
import datetime
from test.log import logger, set_log

#predefine the base class
flask_db = FlaskDB()

#create tables for blog
def create_tables():
    database = flask_db.database
    database.connect()
    try:
        database.create_tables([Entry, User], True)
    except OperationalError:
        print "tables already exist"
        return

class BaseModel(flask_db.Model):
    class Meta:
        database = flask_db.database

#store user infomation, include username & password
class User(BaseModel):
    id = IntegerField(primary_key = True)
    username = CharField(null = True, unique = True)
    password = TextField(null = True)

    #register new user
    @classmethod
    def register(cls, username, password):
        #check if the user exist
        try :
            User.get(User.username == username)
        except DoesNotExist:
            return "User " + username + "does not exist"
        else :
            hash_passwd = hashlib.sha256(password).digest()
            User.create(username = username, password = hash_passwd)
            return "User registered successfully!"

    #modify password
    @classmethod
    def passwd_modify(cls, username, password):
        #check if the user exist
        try:
            result = User.get(User.username == username)
        except DoesNotExist:
            return "User " + username + "does not exist"
        else:
            hash_passwd = hashlib.sha256(password).digest()
            User.update(password = hash_passwd).where(username == username)
            return "Password modified successfully!"

    #check if the user exist & the password is compatible
    @classmethod
    def identify(cls, username, password):
        try:
            result = User.get(User.username == username)
            if hashlib.sha256(password).digest() == result.password:
                return True
            else:
                logger.info("The password of" + username + "is wrong")
            return False
        except DoesNotExist:
            return "User " + username + "does not exist" 
class Entry(BaseModel):
    title = CharField()
    slug = CharField(unique=True)
    content = TextField()
    published = BooleanField(index=True)
    timestamp = DateTimeField(default=datetime.datetime.now, index=True)

    #override save()
    def save_for(self, *args, **kwargs):
        if not self.slug:
            self.slug = (re.sub('[^\w]+', '-', self.title.lower())).encode("utf-8")
        logger.info(self.slug, " ", self.content, " ", self.title)
        ret = super(Entry, self).save(*args, **kwargs)

        # Store search content.
        # self.update_search_index()
        return ret

    def update_search_index(self):
        try:
            fts_entry = FTSEntry.get(FTSEntry.entry_id == self.id)
        except FTSEntry.DoesNotExist:
            fts_entry = FTSEntry(entry_id=self.id)
            force_insert = True
        else:
            force_insert = False
        fts_entry.content = '\n'.join((self.title, self.content))
        fts_entry.save(force_insert=force_insert)

    @classmethod
    def public(cls):
        return Entry.select().where(Entry.published == True)

    @classmethod
    def search(cls, query):
        words = [word.strip() for word in query.split() if word.strip()]
        if not words:
            # Return empty query.
            return Entry.select().where(Entry.id == 0)
        else:
            search = ' '.join(words)

        return (FTSEntry
                .select(
                    FTSEntry,
                    Entry,
                    FTSEntry.rank().alias('score'))
                .join(Entry, on=(FTSEntry.entry_id == Entry.id).alias('entry'))
                .where(
                    (Entry.published == True) &
                    (FTSEntry.match(search)))
                .order_by(SQL('score').desc()))
class FTSEntry(FTSModel):
    entry_id = IntegerField()
    content = TextField()

    class Meta:
        database = flask_db.database
