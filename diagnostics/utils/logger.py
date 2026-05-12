import logging

logger = logging.getLogger('diagnostics')

def log_diagnostic_event(user_id, body_part, message):
    logger.info(f"User {user_id} - Body Part: {body_part} - {message}")
