from vedo import Cube, Sphere, Cylinder, Mesh, Assembly

def generate_and_add_to_scene(commands: list[dict], scene: Assembly):
    """
    Generates meshes from a list of commands and adds them to a vedo Assembly.
    
    Args:
        commands (list[dict]): The list of structured commands from the parser.
        scene (vedo.Assembly): The scene to add the new objects to.
    """
    for command in commands:
        shape = command.get('shape')
        params = command.get('params', {})
        name = command.get('name', 'Unnamed Object')

        mesh = None
        # --- Create Shape ---
        if shape == 'cube':
            side = params.get('side', 1.0)
            mesh = Cube(side=side)
        elif shape == 'sphere':
            radius = params.get('radius', 1.0)
            mesh = Sphere(r=radius)
        elif shape == 'cylinder':
            radius = params.get('radius', 1.0)
            height = params.get('height', radius * 2) # Default height
            mesh = Cylinder(r=radius, height=height)
        else:
            print(f"Warning: Shape '{shape}' is not supported. Skipping.")
            continue
        
        # --- Apply Properties and Transformations ---
        if mesh:
            mesh.name = name # Assign name for the scene graph
            
            # Set color
            color = params.get('color', 'lightblue') # Default color
            mesh.color(color)
            
            # Set position
            position = params.get('position')
            if position:
                mesh.pos(position)
            
            # Improve lighting
            mesh.compute_normals().phong().lighting('glossy')
            
            # Add the finalized mesh to the scene
            scene.add(mesh)
