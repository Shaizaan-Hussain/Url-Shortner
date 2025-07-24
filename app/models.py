import threading
import time
import random
import string

class URLStore:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def _generate_short_code(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    def create_short_url(self, original_url):
        with self.lock:
            for code, entry in self.data.items():
                if entry['url'] == original_url:
                    return code
            short_code = self._generate_short_code()
            while short_code in self.data:
                short_code = self._generate_short_code()
            self.data[short_code] = {
                'url': original_url,
                'clicks': 0,
                'created_at': time.strftime('%Y-%m-%dT%H:%M:%S')
            }
            return short_code

    def get_original_url(self, short_code):
        with self.lock:
            return self.data.get(short_code, {}).get('url')

    def increment_clicks(self, short_code):
        with self.lock:
            if short_code in self.data:
                self.data[short_code]['clicks'] += 1

    def get_stats(self, short_code):
        with self.lock:
            if short_code not in self.data:
                return None
            entry = self.data[short_code]
            return {
                'url': entry['url'],
                'clicks': entry['clicks'],
                'created_at': entry['created_at']
            }
