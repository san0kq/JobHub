import logging


class ContextFormatter(logging.Formatter):
    def format(self, log_record: logging.LogRecord) -> str:
        formatted_message = super().format(record=log_record)
        default_log_record = logging.LogRecord(
            "", 0, "", 0, None, None, None, None, None
        ).__dict__
        default_log_record.update({"message": "", "asctime": ""})

        extra_keys = set(log_record.__dict__) - set(default_log_record)
        if extra_keys:
            context_message = "Context: "
            for key in extra_keys:
                context_message += f"{key}={log_record.__dict__[key]} "
            return formatted_message + " " + context_message
        return formatted_message
