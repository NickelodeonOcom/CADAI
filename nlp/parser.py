import re
from g4f.client import Client

client = Client()  # Only create the client once

def _extract_param(text, param_name, pattern=r'(-?\d+\.?\d*)'):
    """Uses LLM to extract a number for a given parameter name from the text."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": (
                f"In this text: '{text}', extract the value (int or float) for '{param_name}', "
                f"like if I say 'radius of 5', return just 5. No words, just the number."
            )
        }],
        web_search=False
    )
    try:
        return float(response.choices[0].message.content.strip())
    except ValueError:
        return None

def parse_command(text: str) -> list[dict]:
    """Main parser to detect shape, extract its parameters, and additional metadata."""
    commands = []
    text = text.lower().strip()

    # --- Detect shape ---
    shape_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": (
                f"Based on this text: '{text}', what 3D shape is the user referring to? "
                f"Only return the shape name like 'gear', 'cube', 'cylinder', etc."
            )
        }],
        web_search=False
    )
    shape = shape_resp.choices[0].message.content.strip()

    if not shape:
        raise ValueError("Could not detect a shape.")

    command = {'shape': shape, 'params': {}, 'name': text}

    # --- Extract relevant parameter names for this shape ---
    param_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": (
                f"What are the typical parameters needed to describe a '{shape}' in 3D modeling? "
                f"Just list them as space-separated names like: radius height teeth"
            )
        }],
        web_search=False
    )
    param_names = param_resp.choices[0].message.content.strip().split()

    # --- Extract parameter values using LLM ---
    for param_name in param_names:
        value = _extract_param(text, param_name)
        if value is not None:
            command['params'][param_name] = value

    # --- General metadata: color and position ---
    color_match = re.search(r'\b(red|green|blue|yellow|orange|purple|white|black|gray|brown|wooden)\b', text)
    if color_match:
        command['params']['color'] = color_match.group(1)

    pos_match = re.search(r'at\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', text)
    if pos_match:
        command['params']['position'] = [
            float(pos_match.group(1)),
            float(pos_match.group(2)),
            float(pos_match.group(3))
        ]

    commands.append(command)
    return commands

