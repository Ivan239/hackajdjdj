from .engine import get_session

def db_write(function):
    def wrapper(*args, **kwargs):
        session = get_session()
        try:
            result = function(session, *args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    return wrapper


def db_read(function):
    def wrapper(*args, **kwargs):
        session = get_session()
        try:
            return function(session, *args, **kwargs)
        finally:
            session.close()
    return wrapper

@db_write
def new_fingerprint(session, record_id, hash, offset):
    from .models import Fingerprint
    fingerprint = Fingerprint(record_id=record_id, hash=hash, offset=offset)
    session.add(fingerprint)
    return fingerprint

@db_read
def get_fingerprints(session, record_id):
    from .models import Fingerprint
    return session.query(Fingerprint).filter(Fingerprint.record_id == record_id).all()

@db_write
def delete_fingerprints(session, record_id):
    from .models import Fingerprint
    session.query(Fingerprint).filter(Fingerprint.record_id == record_id).delete()
    
@db_write
def new_record(session, record_id):
    from .models import Record
    record = Record(record_id=record_id)
    session.add(record)
    return record

@db_read
def get_record(session, record_id):
    from .models import Record
    return session.query(Record).filter(Record.record_id == record_id).first()

@db_read
def get_records(session):
    from .models import Record
    return session.query(Record).all()

@db_write
def delete_record(session, record_id):
    from .models import Record
    session.query(Record).filter(Record.record_id == record_id).delete()
    
@db_write
def delete_all_records(session):
    from .models import Record
    session.query(Record).delete()
    
@db_write
def delete_all_fingerprints(session):
    from .models import Fingerprint
    session.query(Fingerprint).delete()
    
    