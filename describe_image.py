from PIL import Image
import sys

def analyze(img_path):
    img = Image.open(img_path).convert("RGB")
    width, height = img.size
    print(f"Image size: {width}x{height}")
    # Sample top-center, bottom-center, left, right, etc.
    print("Center pixel:", img.getpixel((width//2, height//2)))
    print("Top-left pixel:", img.getpixel((10, 10)))
    
analyze(sys.argv[1])
