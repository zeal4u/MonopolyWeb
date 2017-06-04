from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker
from json import JSONEncoder
# important
Base = declarative_base()

"""
ORM manager module
"""


class Player(object):
    """
    test
    """
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.position = 0  # we are same at beginning point

    def where_am_i(self):
        """
        return the string showing player's position
        """
        return "%s is at Node %r" % (self.name, self.position)

    def __repr__(self):
        return "<Record(name=%r, time=%r, steps=%r, mapcode=%r)>" % (self.name,self.time,self.steps,self.mapcode)


class Record(Base):
    """
    :attr name: name of player
    :attr steps: the steps to win a game
    :attr time: the time when won the game
    :attr mapcode: in which map
    """
    __tablename__ = 'records'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(20))
    time = Column(String(40))
    steps = Column(Integer)
    mapcode = Column(Integer)

    def __str__(self):

        return 'Record,{name=%s, time=%s, steps=%d, mapcode=%d}' % (
                self.name, self.time, self.steps, self.mapcode)

    def __repr__(self):
        return "<Record(name=%r, time=%r, steps=%r, mapcode=%r)>" % (self.name,self.time,self.steps,self.mapcode)


class RecordEncoder(JSONEncoder):
    """
    JSONEncoder for class:Record
    """
    def default(self, obj):
        if isinstance(obj, Record):
            return {'name':obj.name,
                    'time':obj.time,
                    'steps':obj.steps,
                    'mapcode':obj.mapcode}
        return JSONEncoder.default(self,obj)


class DBHelper(object):
    """
    Tool class for ORM
    """
    engine = None
    session = None

    @staticmethod
    def get_connect(user='jsz', passwd='123456', db='monopoly', host='localhost'):
        """
        this is a static method
        :param str user:
        :param str passwd:
        :param str db:
        :param str host:
        :return: the sqlalchemy engine
        """
        # Lazy Connecting
        if not DBHelper.engine:
            DBHelper.engine = create_engine('mysql+mysqlconnector://%s:%s@%s/%s' %
                                            (user, passwd, host, db), echo=True)
        return DBHelper.engine

    @staticmethod
    def get_session():

        if not DBHelper.session:
            Session = sessionmaker(bind=DBHelper.get_connect())  # this is likely a factory
            DBHelper.session = Session()
        return DBHelper.session

    @staticmethod
    def get_all_by_table(tablecls):
        """
        :param TableClass table: object of table class
        :return: all lines in a table
        """
        result = DBHelper.get_session().query(tablecls).all()
        return result

    @staticmethod
    def get_all_from_records_ranked():
        result = DBHelper.get_session().query(Record).order_by(Record.steps).all()
        return result

    @staticmethod
    def get_by_mapcode_from_records_ranked(mapcode,position=10):
        """
        :param position: int
        :param mapcode: int: which map's records you want know
        :return: a list of records
        """
        result = DBHelper.get_session().query(Record).filter(Record.mapcode == mapcode).order_by(Record.steps).all()[0:position]
        DBHelper.close()
        return result

    @staticmethod
    def record_is_broken(steps,mapcode=1):
        """
        This method called must after updated the records
        if steps is equal with recorded first, so it means old record has been broken.
        :param int steps: one round end, the winner's cost
        :param int mapcode: which map
        :return: whether break record
        """
        session = DBHelper.get_session()
        result, = session.query(Record.steps).filter(Record.mapcode == mapcode).order_by(Record.steps).first() # this long shit return a tuple! wtf
        return result == steps

    @staticmethod
    def update_record(winner,steps,time,mapcode=1):
        """
        update the record, must be called before method record_is_broken
        :param Player winner:
        :param int steps:
        :param int mapcode:
        :param str time:
        :return: None
        """
        session = DBHelper.get_session()
        session.add(Record(name=winner.name,steps=steps,mapcode=mapcode,time=time))
        session.commit()

    @staticmethod
    def close():
        if DBHelper.session:
            DBHelper.session.close()
        if DBHelper.engine:
            DBHelper.engine = None
#
# # if tables have not been created then create them
# Base.metadata.create_all(DBHelper.get_connect())
#
