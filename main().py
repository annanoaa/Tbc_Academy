import requests
import json
import threading
import time

# Lock for thread-safe writing to the file
lock = threading.Lock()

# Fetching method of the data from the URL
def fetchData(url, firstPost):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            with lock:
                with open('post_data.json', 'a') as json_file:
                    if not firstPost[0]:
                        json_file.write(',\n')
                    else:
                        firstPost[0] = False
                    json.dump(data, json_file, indent=4)

    except Exception as e:
        print(f"Error fetching {url}: {e}")

start_time = time.time()

with open('post_data.json', 'w') as json_file:
    json_file.write('[\n')

firstPost = [True]

urls = [f'https://jsonplaceholder.typicode.com/posts/{i}' for i in range(1, 78)]

threads = []
for url in urls:
    thread = threading.Thread(target=fetchData, args=(url, firstPost))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

with open('post_data.json', 'a') as json_file:
    json_file.write('\n]')

end_time = time.time()

print("All posts have been fetched and saved to posts_data.json")
print(f"Total time taken: {end_time - start_time:.2f} seconds")
