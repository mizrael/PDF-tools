# STEP 1
# import libraries
import fitz  # PyMuPDF
import os
from datetime import datetime

# STEP 2
# create a temporary folder with the current timestamp
current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
temp_folder = os.path.join(os.path.dirname(__file__), current_timestamp)
os.makedirs(temp_folder, exist_ok=True)

# prompt user to specify the file path
file = input("Please enter the full path to the PDF file: ")

# open the file
pdf_file = fitz.open(file)

# STEP 3
# iterate over PDF pages
for page_index in range(len(pdf_file)):

    # get the page itself
    page = pdf_file.load_page(page_index)  # load the page
    image_list = page.get_images(full=True)  # get images on the page

    # printing number of images found in this page
    if image_list:
        print(f"[+] Found a total of {len(image_list)} images on page {page_index}")
    else:
        print("[!] No images found on page", page_index)
    
    for image_index, img in enumerate(image_list, start=1):
        # get the XREF of the image
        xref = img[0]

        # extract the image bytes
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image["image"]

        # get the image extension
        image_ext = base_image["ext"]

        # save the image in the temporary folder
        image_name = os.path.join(temp_folder, f"image{page_index+1}_{image_index}.{image_ext}")
        with open(image_name, "wb") as image_file:
            image_file.write(image_bytes)
            print(f"[+] Image saved as {image_name}")