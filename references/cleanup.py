import os
import cv2
import hashlib

if __name__ == "__main__":
    # Use absolute path relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reference_folder = script_dir + "/"

    # Store hashes of pixel data instead of full images to save memory
    processed_hashes = set()
    deleted_images = 0

    for filename in os.listdir(reference_folder):
        if filename == "cleanup.py" or filename.startswith("."):
            continue

        filepath = reference_folder + filename

        if not os.path.isfile(filepath):
            continue

        image = cv2.imread(filepath)

        # Handle non-image files or corrupted captures gracefully
        if image is None:
            continue

        # Calculate a hash of the pixel buffer
        image_hash = hashlib.md5(image.tobytes()).hexdigest()

        if image_hash in processed_hashes:
            os.remove(filepath)
            deleted_images += 1
        else:
            processed_hashes.add(image_hash)

    # print(f"Deleted {deleted_images} duplicate images.")
