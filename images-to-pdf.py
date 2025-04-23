import fitz
import os
from PIL import Image
from io import BytesIO

# Get the folder path from the user
folder_path = input("Enter the folder path containing images: ")

# Get the compression rate from the user
image_quality = input("Enter the image quality (0-100, default is 90): ")
image_quality = int(image_quality) if image_quality.isdigit() else 90

# Create a new PDF document
doc = fitz.open()

# Iterate through all files in the folder
for filename in sorted(os.listdir(folder_path)):
    file_path = os.path.join(folder_path, filename)
    # Check if the file is an image
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        # Open the image and compress it
        with Image.open(file_path) as img:
            img_buffer = BytesIO()
            img.save(img_buffer, format="JPEG", quality=image_quality)
            img_buffer.seek(0)

            # Convert the compressed image to PDF
            imgdoc = fitz.open(stream=img_buffer, filetype="jpeg")
            pdfbytes = imgdoc.convert_to_pdf()
            imgpdf = fitz.open("pdf", pdfbytes)
            doc.insert_pdf(imgpdf)

# Get the destination filename from the user
destination_filename = input("Enter the destination filename for the PDF (leave blank to use the folder name): ")
if not destination_filename:
    destination_filename = os.path.basename(os.path.normpath(folder_path)) + ".pdf"

# Save the combined PDF
doc.save(destination_filename)  # save file