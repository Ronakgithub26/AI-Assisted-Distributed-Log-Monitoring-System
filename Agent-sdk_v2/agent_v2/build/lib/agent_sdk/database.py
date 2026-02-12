import time
from sqlalchemy import event
from .event_builder import build_event
from .queue import EventQueue


def extract_query_type(statement):
    if not statement:
        return "UNKNOWN"
    return statement.strip().split()[0].upper()


def extract_table_name(statement):
    try:
        tokens = statement.strip().split()
        if len(tokens) >= 3:
            return tokens[2]
    except Exception:
        pass
    return "UNKNOWN"


def install_sqlalchemy_monitor(engine):

    @event.listens_for(engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        context._query_start_time = time.time()

    @event.listens_for(engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):

        duration_ms = int(
            (time.time() - context._query_start_time) * 1000
        )

        query_type = extract_query_type(statement)
        table = extract_table_name(statement)

        event_obj = build_event(
            event_type="DB_QUERY",
            category="DATABASE",
            status="SUCCESS",
            metrics={
                "duration_ms": duration_ms
            },
            data={
                "query_type": query_type,
                "table": table
            }
        )

        EventQueue.push(event_obj)

    @event.listens_for(engine, "handle_error")
    def handle_error(context):

        duration_ms = 0
        if hasattr(context, "_query_start_time"):
            duration_ms = int(
                (time.time() - context._query_start_time) * 1000
            )

        query_type = extract_query_type(context.statement)
        table = extract_table_name(context.statement)

        event_obj = build_event(
            event_type="DB_ERROR",
            category="DATABASE",
            status="FAILURE",
            metrics={
                "duration_ms": duration_ms
            },
            data={
                "query_type": query_type,
                "table": table,
                "exception_type": type(context.original_exception).__name__,
                "message": str(context.original_exception)
            }
        )

        EventQueue.push(event_obj)
