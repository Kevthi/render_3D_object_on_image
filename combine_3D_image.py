import cv2
import trimesh
import pyrender
import numpy as np

def main():
    # Load the image
    image_path = "robot_cell.jpg" #Change to the path of the image file
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image file not found at {image_path}")

    # Ensure the image has an alpha channel
    image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # Load the 3D object on the image
    object_path = "assembly_stiffener_stp.obj"  #Change to the path of the 3D object file
    try:
        mesh = trimesh.load(object_path)
        if mesh.is_empty:
            raise ValueError(f"The object file at {object_path} is empty or invalid.")

        # Scale the mesh
        mesh.apply_scale(0.05)

        # Create a scene and add the mesh
        scene = pyrender.Scene(bg_color=[0.0, 0.0, 0.0, 0.0])
        mesh_pyrender = pyrender.Mesh.from_trimesh(mesh, smooth=False)
        mesh_node = scene.add(mesh_pyrender)

        # Add lighting to the scene
        light = pyrender.DirectionalLight(color=np.ones(3), intensity=3.0)
        light_pose = trimesh.transformations.translation_matrix([0, 0, 5.0])
        scene.add(light, pose=light_pose)

        # Set up the camera
        camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
        camera_pose = trimesh.transformations.translation_matrix([0, 0, 5.0])  # Move camera back
        scene.add(camera, pose=camera_pose)

        # Set up the renderer
        r = pyrender.OffscreenRenderer(viewport_width=image.shape[1],
                                       viewport_height=image.shape[0])

        # Initial transformation parameters
        translation = np.zeros(3)
        rotation = np.eye(4)
        scale = 0.05  # Initialize scale to match mesh scaling

        while True:
            # Render the scene
            color, depth = r.render(scene) #color is the rendered image and depth is the depth map

            # Create alpha mask
            alpha_mask = (depth > 0).astype(np.float32)[..., np.newaxis]

            # Overlay the rendered object onto the image
            color_bgr = cv2.cvtColor(color, cv2.COLOR_RGB2BGR)  # Convert rendered color to BGR
            combined_image = color_bgr.astype(float) * alpha_mask + image_rgba[:, :, :3].astype(float) * (1 - alpha_mask)
            combined_image = combined_image.astype(np.uint8)

            # Display the combined image
            cv2.imshow('Image with 3D Object Overlay', combined_image)
            key = cv2.waitKey(10) 
            # Update transformation based on key input
            if key == ord('w'):
                translation[1] += 0.1  # Move up
            elif key == ord('s'):
                translation[1] -= 0.1  # Move down
            elif key == ord('a'):
                translation[0] -= 0.1  # Move left
            elif key == ord('d'):
                translation[0] += 0.1  # Move right
            #Handle rotation in x-direction
            elif key == ord('u'):
                rot = trimesh.transformations.rotation_matrix(np.radians(5), [1, 0, 0])
                rotation = rot @ rotation
            elif key == ord('i'):
                rot = trimesh.transformations.rotation_matrix(np.radians(-5), [1, 0, 0])
                rotation = rot @ rotation
            #Handle rotation in y-direction
            elif key == ord('j'):
                rot = trimesh.transformations.rotation_matrix(np.radians(5), [0, 1, 0])
                rotation = rot @ rotation
            elif key == ord('k'):
                rot = trimesh.transformations.rotation_matrix(np.radians(-5), [0, 1, 0])
                rotation = rot @ rotation
            #Hanle rotation in z-direction
            elif key == ord('n'):
                rot = trimesh.transformations.rotation_matrix(np.radians(5), [0, 0, 1])
                rotation = rot @ rotation
            elif key == ord('m'):
                rot = trimesh.transformations.rotation_matrix(np.radians(-5), [0, 0, 1])
                rotation = rot @ rotation
            elif key == ord('+'):
                scale += 0.001  # Increase scale
            elif key == ord('-'):
                scale = max(0.01, scale - 0.001)  # Decrease scale with minimum value
            elif key == 27:  # ESC key to exit
                break

            # Update the mesh pose
            mesh_scale = trimesh.transformations.scale_matrix(scale)
            mesh_pose = trimesh.transformations.translation_matrix(translation) @ rotation @ mesh_scale
            scene.set_pose(mesh_node, pose=mesh_pose)

        r.delete()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Failed to load the 3D object: {e}")

if __name__ == "__main__":
    main()
