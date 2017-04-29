# -*- coding: utf-8 -*-
"""
    flask._compat
    ~~~~~~~~~~~~~
    :copyright: (c) 2015 by Sudip Das.
"""
import sys

PY2 = sys.version_info[0] == 2
_identity = lambda x: x


if not PY2:
    text_type = str
    string_types = (str,)
    integer_types = (int,)

    iterkeys = lambda d: iter(d.keys())
    itervalues = lambda d: iter(d.values())
    iteritems = lambda d: iter(d.items())

    from io import StringIO

    def reraise(tp, value, tb=None):
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value

    implements_to_string = _identity

else:
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)

    iterkeys = lambda d: d.iterkeys()
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()

    from cStringIO import StringIO

    exec('def reraise(tp, value, tb=None):\n raise tp, value, tb')

    def implements_to_string(cls):
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda x: x.__unicode__().encode('utf-8')
        return cls


def with_metaclass(meta, *bases):
    
    class metaclass(type):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)
    return type.__new__(metaclass, 'temporary_class', (), {})



BROKEN_PYPY_CTXMGR_EXIT = False
if hasattr(sys, 'pypy_version_info'):
    class _Mgr(object):
        def __enter__(self):
            return self
        def __exit__(self, *args):
            sys.exc_clear()
    try:
        try:
            with _Mgr():
                raise AssertionError()
        except:
            raise
    except TypeError:
        BROKEN_PYPY_CTXMGR_EXIT = True
    except AssertionError:
        pass
