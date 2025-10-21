import requests
from threading import Thread

def download_chunk(url, start, end, i):
    headers = {'Range': f'bytes={start}-{end}'}
    r = requests.get(url, headers=headers, stream=True)
    with open(f'chunk_{i}', 'wb') as f:
        f.write(r.content)

# Split a large file URL into N threads
