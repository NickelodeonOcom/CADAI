from app.generator import generate_model

def test_generate_model():
    assert generate_model("a box") is not None
    assert generate_model("a cylinder") is not None


### File: tests/test_visualizer.py
from app.visualizer import render_model
import trimesh

def test_render():
    box = trimesh.creation.box()
    try:
        render_model(box)
    except Exception:
        assert False, "Rendering failed"
