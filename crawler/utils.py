import re
from urllib.parse import urlparse

def is_same_domain(base_url, target_url):
    return urlparse(base_url).netloc == urlparse(target_url).netloc

def normalize_phone(number):
    digits = re.sub(r'\D', '', number)

    if len(digits) == 10:
        return '+91' + digits
    elif digits.startswith('91') and len(digits) == 12:
        return '+' + digits
    elif number.startswith('+'):
        return '+' + digits
    
    return None

def extract_phone_numbers(text):
    # Regex for finding phone numbers
    pattern = r'\+?\d[\d\s\-]{8,}\d'
    matches = re.findall(pattern, text)
    
    formatted_numbers = set()
    for match in matches:
        normalized = normalize_phone(match)
        if normalized:
            formatted_numbers.add(normalized)
            
    return list(formatted_numbers)
