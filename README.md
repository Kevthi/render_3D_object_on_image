# Overlay Object on Image

A Python application that overlays a 3D object onto a specified image, allowing interactive manipulation of the 3D model's position, scale, and rotation using keyboard controls.

## Features
- **3D Object Overlay**: Seamlessly overlays a 3D model onto a chosen image.
- **Interactive Controls**: Manipulate the 3D object's position, scale, and rotation in real-time.

## Installation


Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Change the `image_path` to the path of the image you want to render on.
   ```python
   image_path = "your_image.jpg"
   ```

2. Change the `object_path` to the path of the 3D model you want to overlay.
   ```python
   object_path = "your_model.obj"
   ```

3. Run the script:
   ```bash
   python combine_3D_image.py
   ```

## Controls
- **Move the object**:
  - `w`: Move up
  - `s`: Move down
  - `a`: Move left
  - `d`: Move right

- **Rotate the object**:
  - `u` / `i`: Rotate along the X-axis
  - `j` / `k`: Rotate along the Y-axis
  - `n` / `m`: Rotate along the Z-axis

- **Change the size of the object**:
  - `+` : Scale up
  - `-` : Scale down

- **Quit the application**:
  - `esp` : end the application

## Requirements
- Python 3.6+
- OpenCV
- Trimesh
- PyRender
- NumPy

## Notes
- Ensure the image and 3D model paths are correct before running the script.
- You may need to adjust the scaling factor or camera position to ensure the 3D model appears correctly over the image.



