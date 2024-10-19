import logging
import io, sys, os
from colorama import init

def setup_logging():
    db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database')
    log_path = os.path.join(db_dir, 'error_log.txt')
    logging.basicConfig(filename=log_path, level=logging.ERROR, format='%(asctime)s - %(message)s')

def setup_encoding():
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

def setup_colorama():
    init(autoreset=True)
