from requests_toolbelt.utils import dump

from requests.adapters import HTTPAdapter

DEFAULT_TIMEOUT = 5  # seconds


def logging_hook(response, *args, **kwargs):
    """
    Hook for loggin request, use as:
    http = Session()
    http.hooks["response"] = [logging_hook]
    """
    data = dump.dump_all(response)
    print(data.decode("utf-8"))


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)
