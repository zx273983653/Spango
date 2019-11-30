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
            'update_time': time.time()
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

    # 更新session时间
    @staticmethod
    def init_expires(session_id):
        s_ = Session.get_session(session_id)
        if s_:
            Session.lock.acquire()
            s_['update_time'] = time.time()
            Session.lock.release()
            return s_

    # 移除过期session
    @staticmethod
    def rm_expires():
        Session.lock.acquire()
        rm_lst = []
        for s_ in Session.s_lst:
            if float(time.time() - s_.get('update_time')) >= Session.expires * 60:
                rm_lst.append(s_)
        for rm_s_ in rm_lst:
            Session.s_lst.remove(rm_s_)
        Session.lock.release()
