from .config import AgentConfig
from .sender import Sender
from .exceptions import ExceptionTracker
from .network import install_http_patch
from .logging_capture import install_logging


class Agent:

    _initialized = False

    @classmethod
    def init(
        cls,
        *,
        api_key: str,
        api_secret: str,
        endpoint: str,
        project: str,
        environment: str = "production",

        framework: str | None = None,
        app=None,
        db_engine=None,

        enable_exceptions: bool = True,
        enable_http: bool = True,
        enable_logging: bool = True,
        enable_performance: bool = False
    ):

        if cls._initialized:
            return

        # ----------------------------
        # Core Configuration
        # ----------------------------
        AgentConfig.api_key = api_key
        AgentConfig.api_secret = api_secret
        AgentConfig.endpoint = endpoint
        AgentConfig.project = project
        AgentConfig.environment = environment

        # ----------------------------
        # Install Core Modules
        # ----------------------------
        if enable_exceptions:
            ExceptionTracker.install()

        if enable_http:
            install_http_patch()

        if enable_logging:
            install_logging()

        # ----------------------------
        # Framework Integration
        # ----------------------------
        if framework and app:

            framework = framework.lower()

            if framework == "flask":
                from .integrations.flask import init_flask
                init_flask(app)

            elif framework == "fastapi":
                from .integrations.fastapi import init_fastapi
                init_fastapi(app)

            elif framework == "django":
                from .integrations.django import init_django
                init_django()

            else:
                raise ValueError(f"Unsupported framework: {framework}")

        # ----------------------------
        # Database Monitoring
        # ----------------------------
        if db_engine:
            from .database import install_sqlalchemy_monitor
            install_sqlalchemy_monitor(db_engine)

        # ----------------------------
        # Performance Module (optional)
        # ----------------------------
        if enable_performance:
            from .performance import monitor_performance
            # decorator-based, no auto-hook required
            # kept for future extension

        # ----------------------------
        # Start Background Sender
        # ----------------------------
        Sender.start()

        cls._initialized = True

