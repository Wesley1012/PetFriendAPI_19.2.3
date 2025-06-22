import json
import time
from functools import wraps

def api_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        # signature = ", ".join(args_repr + kwargs_repr)
        log_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "function": func.__name__,
            "request": {
                "headers": f"{args_repr[1]}",
                "params": args_repr[2:],
                "filters": kwargs_repr,

            },
        }

        status_code, response = func(*args, **kwargs)
        # if "pets" in response:
        #     response = response["pets"][0:5]

        log_data["response"] = {
            "status_code": status_code,
            "body": response
        }
        end_str = f"{"=" * 200}"
        with open("log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(log_data, indent=4, ensure_ascii=False) + "\n" + end_str)
        return status_code, response

    return wrapper
