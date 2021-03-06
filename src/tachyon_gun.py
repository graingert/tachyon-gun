import datetime as dt
from contextlib import contextmanager
from dataclasses import dataclass

import _tachyon_gun


@dataclass
class Warp:
    destination: float
    start_time: float


current_warp = None


@contextmanager
def warp_time(destination):
    global current_warp
    if current_warp is not None:
        raise RuntimeError("Cannot warp during a warp.")

    _tachyon_gun.patch()

    current_warp = Warp(
        destination=destination, start_time=_tachyon_gun.original_time(),
    )
    try:
        yield
    finally:
        current_warp = None


# datetime module


def now(tz=None):
    if current_warp is None:
        return _tachyon_gun.original_now()
    else:
        return dt.datetime.fromtimestamp(time(), tz)


def utcnow():
    if current_warp is None:
        return _tachyon_gun.original_utcnow()
    else:
        return dt.datetime.fromtimestamp(time(), dt.timezone.utc)


# time


def time():
    if current_warp is None:
        return _tachyon_gun.original_time()
    else:
        return current_warp.destination + (
            _tachyon_gun.original_time() - current_warp.start_time
        )


def localtime(secs=None):
    if current_warp is None or secs is not None:
        return _tachyon_gun.original_localtime(secs)
    else:
        return _tachyon_gun.original_localtime(
            current_warp.destination
            + (_tachyon_gun.original_time() - current_warp.start_time)
        )


def gmtime(secs=None):
    if current_warp is None or secs is not None:
        return _tachyon_gun.original_gmtime(secs)
    else:
        return _tachyon_gun.original_gmtime(
            current_warp.destination
            + (_tachyon_gun.original_time() - current_warp.start_time)
        )


def strftime(format, t=None):
    if t is not None:
        return _tachyon_gun.original_strftime(format, t)
    elif current_warp is None:
        return _tachyon_gun.original_strftime(format)
    else:
        return _tachyon_gun.original_strftime(format, localtime())
