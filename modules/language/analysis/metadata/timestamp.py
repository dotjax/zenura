from datetime import datetime

def generate(_):
    return datetime.now().strftime("%Y%m%d_%H%M%S")