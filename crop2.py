from PIL import Image

def crop_center_banner(image_path, output_path):
    # This tries to forcefully crop mostly the middle horizontal strip
    # Assumes the banner is horizontally centered and wide
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    
    left, right = width, 0
    top, bottom = height, 0
    
    # Check pixels along the middle vertical line to find top/bottom of banner
    mid_x = width // 2
    bg_color = img.getpixel((0, 0))
    
    # To avoid noise, let's look for significant color differences
    for y in range(height):
        p = img.getpixel((mid_x, y))
        diff = abs(p[0] - bg_color[0]) + abs(p[1] - bg_color[1]) + abs(p[2] - bg_color[2])
        if diff > 50: # Strong difference
            top = min(top, y)
            bottom = max(bottom, y)
            
    # Check pixels along the middle horizontal line to find left/right of banner
    mid_y = height // 2
    for x in range(width):
        p = img.getpixel((x, mid_y))
        diff = abs(p[0] - bg_color[0]) + abs(p[1] - bg_color[1]) + abs(p[2] - bg_color[2])
        if diff > 50:
            left = min(left, x)
            right = max(right, x)
            
    if right <= left or bottom <= top:
        print("Could not detect inner banner. Skipping crop.")
        img.save(output_path)
    else:
        # Add slight padding
        left = max(0, left - 4)
        top = max(0, top - 4)
        right = min(width, right + 4)
        bottom = min(height, bottom + 4)
        print(f"Cropping to: {left}, {top}, {right}, {bottom}")
        cropped = img.crop((left, top, right, bottom))
        cropped.save(output_path)

crop_center_banner('banner.png', 'banner_cropped.png')

