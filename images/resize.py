from PIL import Image

# Open the original image
img = Image.open("Divergence_CavityFlow.png")

# Define the max width you want
max_width = 400

# Compute the proportional height
w_percent = max_width / float(img.size[0])
new_height = int(float(img.size[1]) * w_percent)

# Resize with aspect ratio preserved
img_resized = img.resize((max_width, new_height), Image.LANCZOS)

# Save the resized image
img_resized.save("Divergence_CavityFlow_small.png")
