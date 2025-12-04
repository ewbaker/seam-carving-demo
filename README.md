# Seam Carving (Content-Aware Image Resizing)

This project is a Python implementation of the **Seam Carving algorithm** (based on the 2007 paper by Avidan & Shamir). It intelligently resizes images by removing "low-energy" paths of pixels rather than scaling or cropping, preserving important content like faces or objects.

## Files Included
- `main.py`: The core algorithm implementation.
- `input_castle.jpg`: A sample image that works well (Success Case).
- `input_crowd.jpg`: A sample image that demonstrates limitations (Failure Case).
- `requirements.txt`: Dependencies.

## How to Run the Code

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Select Your Image**
   The script looks for a file specifically named `input.jpg`. You must rename one of the provided samples to run the demo:
   *   To run the Castle demo: Rename `input_castle.jpg` -> `input.jpg`
   *   To run the Crowd demo: Rename `input_crowd.jpg` -> `input.jpg`

3. **Run the Script**
   ```bash
   python main.py
   ```

4. **View the Output**
   *   `output.jpg`: The final resized image will be saved in the main folder.
   *   `frames/` folder: The script generates individual frames here showing the seam removal process (used for creating animation videos).
   *   *Note: The script automatically resizes inputs to 400px width for performance demonstration.*

## Algorithm Overview
- **Energy Calculation:** Converts image to grayscale and uses Sobel filters to calculate pixel importance.
- **Seam Identification:** Uses Dynamic Programming (DP) to find the vertical path of lowest cumulative energy from top to bottom.
- **Seam Removal:** Removes the identified path and shifts pixels to close the gap.

## Limitations
The algorithm performs poorly on "high-energy" images where edge detail is uniformly distributed (e.g., dense crowds or close-up faces), resulting in distortion of important features.