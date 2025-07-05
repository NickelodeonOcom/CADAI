from app.prompts import clean_prompt
import trimesh

def generate_model(prompt: str):
    clean = clean_prompt(prompt)

    # Placeholder logic: return a box for now
    if "cylinder" in clean:
        mesh = trimesh.creation.cylinder(radius=1.0, height=2.0)
    elif "sphere" in clean:
        mesh = trimesh.creation.icosphere(subdivisions=3, radius=1.0)
    else:
        mesh = trimesh.creation.box(extents=[1, 2, 3])

    return mesh
