from PIL import Image
import logging
import hashlib

logging.basicConfig(level=logging.INFO)


def check_hash(file_name, file_hash):
    f = open(file_name, 'rb')
    d = f.read()
    # if hash == hashlib.sha256(d).hexdigest():
    #     return True
    f_hash = hashlib.sha256(d).hexdigest()
    logging.info(f'New file hash: \t{f_hash}')
    logging.info(f'Old file hash: \t{file_hash}')
    if file_hash == f_hash:
        return True
    return False


# This properties should be written inside the image file
# Note that this is just a demo and needs further developments
# File length in Bytes
file_length = 458053
# It should be original file name
export_file = "dcx_re.pdf"
# SHA256
file_sha256 = '953ffebe8456f93ad2cf79e097f0de8b9883702646af3089790d34a5e8dedf07'

recovery_img = 'dcx2.png'
img = Image.open(recovery_img)
pixel = img.load()
recovery_file = open(export_file, 'wb')

# # Logs
logs = open('img2dcx.txt', 'wb')
pos = 0
finished = False
for i in range(img.height):
    for j in range(img.width):
        recovery_file.write(pixel[j, i].to_bytes(1, 'big'))
        if pos < 10:
            logs.write(f'({j}, {i}) {pixel[j, i]}\n'.encode())
        pos += 1
        if pos == file_length:
            finished = True
            break
    if finished:
        break
logs.close()
logging.info(f'Pixels read: pos is {pos}')

img.close()
recovery_file.close()

if check_hash(export_file, file_sha256):
    print("Done.")
else:
    print("Error.")
