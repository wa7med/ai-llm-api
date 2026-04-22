import logging

logging.basicConfig(level=logging.INFO)

def log_request(input_text, output):
    logging.info(f"INPUT: {input_text}")
    logging.info(f"OUTPUT: {output}")
