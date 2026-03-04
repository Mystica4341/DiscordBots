import os
import requests
from urllib.parse import urlparse, unquote
fileURL = 'https://tiebapic.baidu.com/forum/pic/item/01491410b912c8fc4ab4f6d1ba039245d78821ad.jpg?tbpicau=2026-02-23-05_d289d54c5ad58172a9971543150d5f76'
#fileURL = 'https://tiebapic.baidu.com/forum/pic/item/34d2ea12c8fcc3ce267c261ed445d688d53f20a6.jpg?tbpicau=2026-02-23-05_86c8235b205657a5a7fba8350ef3958d'
print("Downloading file from URL:", fileURL)
response = requests.get(fileURL, stream=True)
file_content = response.content
# Check file type from URL

# URL parsing to get the file name
parsed_url = urlparse(fileURL)

# Lấy phần đường dẫn và giải mã (unquote) nếu có ký tự đặc biệt
# Phần này tự động loại bỏ mọi thứ sau dấu '?'
path = unquote(parsed_url.path)

file_name = os.path.basename(path)
print(f"File name: {file_name}, {fileURL}")
with open(file_name, "wb") as temp_file:
  temp_file.write(file_content)