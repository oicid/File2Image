from PIL import Image
import os
import logging

logging.basicConfig(level=logging.INFO)

original_file = "dcx.pdf"
end_file = 'dcx2.png'

data_file = open(original_file, 'rb')
file_size = os.path.getsize(original_file)
logging.info(f'File size of {original_file}: {file_size}')

# Demo: assume the size of new image is 512 * 512
width = 256
height = (file_size // 3) // width + 1
logging.info(f"Size of image: {width} in width, {height} in height")

# Set initial pixel as 0 (white)
# img = Image.new("L", (width, height), 0)
img = Image.new("RGB", (width, height), (0, 0, 0))
pixel = img.load()

# # Logs
logs = open('dcx2img.txt', 'wb')
pos = 0
while byte_file := data_file.read(3):
    try:
        pixel[pos % width, pos // width] = (byte_file[0], byte_file[1], byte_file[2])
    except IndexError:
        if file_size % 3 == 2:
            pixel[pos % width, pos // width] = (byte_file[0], byte_file[1], 0)
        else:
            pixel[pos % width, pos // width] = (byte_file[0], 0, 0)
    if pos < 10:
        # print(f'({pos}, 0) {pixel[pos, 0]}')
        logs.write(f'({pos % width}, {pos // height}) {pixel[pos % width, pos // height]} {byte_file}\n'.encode())
    pos += 1
logs.close()
logging.info(f"Pixels set: pos is {pos}")

# # Check
for i in range(10):
    print(f'({i}, 0) {pixel[i, 0]}')

data_file.close()
img.save(end_file)
img.close()
print("Done.")

check_img = Image.open(end_file)
check_pixel = check_img.load()
for i in range(10):
    print(f'({i}, 0) {check_pixel[i, 0]}')
check_img.close()
