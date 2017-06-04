from nose.tools import *
from bin.stuff import *
from sqlalchemy.orm import sessionmaker

from tests.tools import debug


@debug(True)
def test_connect():
    "test the connection of mysql"
    DBHelper.get_connect()


@debug(False)
def test_create_a_record():
    "test create a record in db"
    Session = sessionmaker(bind=DBHelper.get_connect()) # this is likely a factory
    session = Session()

    add_record = Record(name='JiangShizhi',time='1970-01-01 00:00:00',steps=10000,mapcode=0)
    session.add(add_record)
    session.commit()

    get_record = session.query(Record).filter_by(name='JiangShizhi').first()
    assert_equal(get_record,add_record)


@debug(False)
def test_add_records():
    "test add records"
    session = DBHelper.get_session()
    records = []
    for index in range(1,11):
        records.append(Record(name='jsz',time='2016-10-19-14-30',steps=index,mapcode=1))
    session.add_all(records)
    session.commit()

    result = session.query(Record).all()
    assert_equal(result,records)

@debug(False)
def test_get_all_from_records_ranked():
    "test get ranked records"
    records = []
    for index in range(1, 11):
        records.append(Record(name='jsz', time='2016-10-19-14-30', steps=index, mapcode=1))
    assert_equal(DBHelper.get_all_from_records_ranked(),records)


@debug(False)
def test_get_by_mapcode_from_records_ranked():
    assert_equal(DBHelper.get_by_mapcode_from_records_ranked(1)[0].mapcode,1)


@debug(False)
def test_record_is_broken():
    result = DBHelper.record_is_broken(6)
    assert_equal(True,result)

