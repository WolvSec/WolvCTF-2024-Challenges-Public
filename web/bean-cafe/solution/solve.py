import requests

"""
General solve approach:

1. Use google to find two images that get put into the desired prediction categories.
2. Review this: https://github.com/corkami/collisions/tree/master?tab=readme-ov-file
3. Run a command something like this:
(assumes your images are jpgs)

python3 jpg.py /Users/sambrow/Downloads/leafs/healthy.jpg /Users/sambrow/Downloads/leafs/rust.jpg

4. This will output (in the current directory) files named:

collision1.jpg
collision2.jpg

5. Double-check which is which and submit them in the correct position for the flag.
"""

def send_files(url, file_paths):
    files = {
        key: open(file_path, 'rb') 
        for key, file_path in file_paths.items()
    }
    
    try:
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            if 'flag_9RzYDbk4p3LzZhXdgKcVQ.jpg' in response.text:
                print("Solved: bean-cafe")
            else:
                print("bean-cafe: Flag not detected!")
        else:
            print("Failed to upload files. Status code:", response.status_code)
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    finally:
        for file in files.values():
            file.close()


# Specify the file paths and corresponding form field names
file_paths = {
    'healthyLeaf': 'healthy.jpg',
    'rustLeaf': 'rust.jpg'
}
# url = 'http://172.17.0.2:5000/submit'
url = 'https://bean-cafe-okntin33tq-ul.a.run.app/submit'

send_files(url, file_paths)
