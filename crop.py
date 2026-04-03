from PIL import Image

def crop_banner(image_path, output_path):
    img = Image.open(image_path).convert("RGBA")
    
    # Get the background color from top-left pixel
    bg_color = img.getpixel((0, 0))
    
    # Find bounding box of all pixels that are NOT the background color
    width, height = img.size
    left, top, right, bottom = width, height, 0, 0
    
    # Simple bounding box find
    for x in range(width):
        for y in range(height):
            # Check if pixel is different from bg color
            # Allow some tolerance for anti-aliasing
            p = img.getpixel((x, y))
            # Just simple check if it strongly differs from bg
            if abs(p[0] - bg_color[0]) > 20 or abs(p[1] - bg_color[1]) > 20 or abs(p[2] - bg_color[2]) > 20:
                if x < left: left = x
                if x > right: right = x
                if y < top: top = y
                if y > bottom: bottom = y
                
    # Add a small padding (e.g., 5 pixels) but keep within bounds
    padding = 2
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(width, right + padding)
    bottom = min(height, bottom + padding)
    
    # Crop the image
    cropped = img.crop((left, top, right, bottom))
    cropped.save(output_path)
    print(f"Cropped to ({left}, {top}, {right}, {bottom})")

crop_banner('banner.png', 'banner_cropped.png')
