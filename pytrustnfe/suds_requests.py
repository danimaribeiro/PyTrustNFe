import functools
import requests
import suds.transport as transport
import traceback
from six import StringIO


__all__ = ['RequestsTransport']


def handle_errors(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.HTTPError as e:
            buf = StringIO(e.response.content)
            raise transport.TransportError(
                'Error in requests\n' + traceback.format_exc(),
                e.response.status_code,
                buf,
            )
        except requests.RequestException:
            raise transport.TransportError(
                'Error in requests\n' + traceback.format_exc(),
                000,
            )
    return wrapper


class RequestsTransport(transport.Transport):
    def __init__(self, session=None):
        transport.Transport.__init__(self)
        self._session = session or requests.Session()

    @handle_errors
    def open(self, request):
        resp = self._session.get(request.url)
        resp.raise_for_status()
        return StringIO(resp.content)

    @handle_errors
    def send(self, request):
        resp = self._session.post(
            request.url,
            data=request.message,
            headers=request.headers,
        )
        if resp.headers.get('content-type') not in ('text/xml',
                                                    'application/soap+xml'):
            resp.raise_for_status()
        return transport.Reply(
            resp.status_code,
            resp.headers,
            resp.content,
        )
