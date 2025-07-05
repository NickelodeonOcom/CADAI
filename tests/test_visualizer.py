from app.visualizer import render_model
import trimesh

def test_render():
    box = trimesh.creation.box()
    try:
        render_model(box)
    except Exception:
        assert False, "Rendering failed"
