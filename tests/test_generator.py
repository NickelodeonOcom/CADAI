from app.generator import generate_model

def test_generate_model():
    assert generate_model("a box") is not None
    assert generate_model("a cylinder") is not None
