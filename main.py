import cv2
import numpy as np
import sys
import os  # Imported to create the 'frames' folder

def calculate_energy(image):
    """
    Step 1: Calculate the 'energy' of the image.
    High energy = Edges (important).
    Low energy = Smooth areas (sky, flat walls).
    """
    # Converts image to grayscale for easier analysis
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Uses Sobel filters to identify edges in X and Y directions
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    # Combines gradients to form the final energy map
    energy_map = np.abs(sobel_x) + np.abs(sobel_y)
    return energy_map

def find_vertical_seam(energy_map):
    """
    Step 2: Dynamic Programming to find the path of least energy.
    """
    rows, cols = energy_map.shape
    
    # Creates a DP matrix to store cumulative energy costs
    dp = energy_map.copy()
    
    # Creates a 'backtrack' matrix to remember the path taken
    backtrack = np.zeros_like(dp, dtype=np.int32)

    # Loops through rows starting from the second one down to the bottom
    for i in range(1, rows):
        for j in range(cols):
            # Handles boundary conditions (left and right edges)
            if j == 0:
                idx = np.argmin(dp[i-1, j:j+2]) 
                backtrack[i, j] = j + idx
                min_energy = dp[i-1, j + idx]
            elif j == cols - 1:
                idx = np.argmin(dp[i-1, j-1:j+1]) 
                backtrack[i, j] = j - 1 + idx
                min_energy = dp[i-1, j - 1 + idx]
            else:
                idx = np.argmin(dp[i-1, j-1:j+2])
                backtrack[i, j] = j - 1 + idx
                min_energy = dp[i-1, j - 1 + idx]
            
            dp[i, j] += min_energy

    # Backtracks from the bottom to find the full path of the seam
    seam = []
    j = np.argmin(dp[-1]) 
    for i in range(rows - 1, -1, -1):
        seam.append((i, j))
        j = backtrack[i, j]
    
    return seam

def remove_vertical_seam(image, seam):
    """
    Step 3: Remove the pixels identified in the seam.
    """
    rows, cols, _ = image.shape
    new_image = np.zeros((rows, cols - 1, 3), dtype=np.uint8)
    
    for i, j in seam:
        new_image[i, :j] = image[i, :j]
        new_image[i, j:] = image[i, j+1:]
        
    return new_image

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Loads the input image
    print("Loading image...")
    # MAKE SURE YOUR FILE IS NAMED 'input.jpg' OR CHANGE THIS LINE
    input_img = cv2.imread('input.jpg')
    
    if input_img is None:
        print("Error: Could not load input.jpg")
        sys.exit()

    # --- SETUP ANIMATION FOLDER ---
    if not os.path.exists('frames'):
        os.makedirs('frames')
        print("Created 'frames' folder.")
    else:
        print("Using existing 'frames' folder.")
    # ------------------------------

    # Resizes the image to a smaller width for faster processing
    height, width = input_img.shape[:2]
    new_width = 400
    new_height = int(height * (new_width / width))
    print(f"Resizing image to {new_width}x{new_height}...")
    input_img = cv2.resize(input_img, (new_width, new_height))

    # Sets number of seams (Higher number = longer video)
    SCALE_AMOUNT = 100 
    current_img = input_img.copy()

    print(f"Starting Seam Carving. Saving {SCALE_AMOUNT} frames...")

    for i in range(SCALE_AMOUNT):
        # 1. Calculates energy
        energy = calculate_energy(current_img)
        
        # 2. Finds the seam
        seam = find_vertical_seam(energy)
        
        # 3. Removes the seam
        current_img = remove_vertical_seam(current_img, seam)
        
        # --- SAVE FRAME FOR VIDEO ---
        # Saves as frame_000.jpg, frame_001.jpg, etc.
        filename = f"frames/frame_{i:03d}.jpg"
        cv2.imwrite(filename, current_img)
        # ----------------------------
        
        if i % 10 == 0:
            print(f"Saved frame {i}/{SCALE_AMOUNT}")
            
    print("Done! Check the 'frames' folder.")
