import hashlib
import random
import time
import threading
from spango.service.constant import Constant


class Session:

    @staticmethod
    def set_up():
        Session.expires = Constant.session_expires
        Session.s_lst = []
        Session.lock = threading.Lock()

    @staticmethod
    def create_session():
        ra = str(random.randint(1000, 100000))
        session_id = hashlib.md5(ra.encode()).hexdigest()
        session = {
            'id': session_id,
            'expires': Session.expires,
            'cre_time': time.time()
        }
        Session.lock.acquire()
        Session.s_lst.append(session)
        Session.lock.release()
        return session, session_id

    @staticmethod
    def get_session(session_id):
        Session.lock.acquire()
        for s_ in Session.s_lst:
            if session_id == s_.get('id'):
                Session.lock.release()
                return s_
        Session.lock.release()

    @staticmethod
    def init_expires(session_id):
        s_ = Session.get_session(session_id)
        if s_:
            s_['expires'] = Session.expires
            print('1111111', 'session过期时间已更新')
            return True
        else:
            return False

    @staticmethod
    def rm_expires():
        Session.lock.acquire()
        for s_ in Session.s_lst:
            cre_time = s_.get('cre_time')
            if int(time.time() - cre_time) >= Session.expires * 60:
                Session.s_lst.remove(s_)
        Session.lock.release()
