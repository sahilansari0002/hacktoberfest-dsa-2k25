import requests
from threading import Thread
import os

def download_chunk(url, start, end, index):
    headers = {'Range': f'bytes={start}-{end}'}
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        with open(f'chunk_{index}', 'wb') as f:
            f.write(response.content)
        print(f"Chunk {index} downloaded: {start}-{end}")
    except Exception as e:
        print(f"Error downloading chunk {index}: {e}")

def merge_chunks(num_chunks, output_file='output_file'):
    with open(output_file, 'wb') as outfile:
        for i in range(num_chunks):
            chunk_file = f'chunk_{i}'
            with open(chunk_file, 'rb') as infile:
                outfile.write(infile.read())
            os.remove(chunk_file)
    print(f"All chunks merged into {output_file}")

def download_file_multithreaded(url, num_threads=4):
    response = requests.head(url)
    file_size = int(response.headers.get('Content-Length', 0))
    print(f"Total file size: {file_size} bytes")

    chunk_size = file_size // num_threads
    threads = []

    for i in range(num_threads):
        start = i * chunk_size
        end = file_size - 1 if i == num_threads - 1 else (start + chunk_size - 1)
        thread = Thread(target=download_chunk, args=(url, start, end, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    merge_chunks(num_threads)

# Example usage
# download_file_multithreaded('https://example.com/largefile.zip', num_threads=4)
