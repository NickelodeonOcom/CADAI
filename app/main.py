from app.generator import generate_model
from app.visualizer import render_model

def main():
    prompt = input("CAD: ")
    mesh = generate_model(prompt)
    render_model(mesh)
