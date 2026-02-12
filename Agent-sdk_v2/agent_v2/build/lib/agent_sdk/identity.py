import socket
import platform
import os
import uuid


class Identity:

    _cached_identity = None

    @classmethod
    def collect(cls, api_key, app_version="1.0.0", region="unknown"):

        if cls._cached_identity:
            return cls._cached_identity

        hostname = socket.gethostname()

        try:
            ip = socket.gethostbyname(hostname)
        except Exception:
            ip = "unknown"

        cls._cached_identity = {
            "api_key": api_key,
            "hostname": hostname,
            "ip": ip,
            "region": region,
            "os": platform.system(),
            "os_version": platform.release(),
            "python_version": platform.python_version(),
            "process_id": os.getpid(),
            "app_version": app_version,
            "instance_id": str(uuid.uuid4())
        }

        return cls._cached_identity
