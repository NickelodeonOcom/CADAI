from vedo import Assembly, io

def export_model(scene_object: Assembly, file_path: str):
    """
    Exports a vedo Assembly or Mesh to a specified file path.
    The file format is determined by the file extension.
    
    Args:
        scene_object (vedo.Assembly or vedo.Mesh): The scene/object to export.
        file_path (str): The full path to save the file to.
    """
    if not scene_object or scene_object.npoints == 0:
        print("Error: No model to export.")
        return
        
    try:
        # vedo's write function automatically handles Assemblies
        io.write(scene_object, file_path)
        print(f"Scene successfully exported to {file_path}")
    except Exception as e:
        print(f"An error occurred during export: {e}")
