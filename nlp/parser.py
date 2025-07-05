import re

def parse_command(text: str) -> list[dict]:
    """
    An advanced, rule-based parser to extract multiple commands from natural language.
    It identifies shapes, colors, sizes, positions, and rotations.
    
    Args:
        text (str): The user's input string.
        
    Returns:
        list[dict]: A list of structured command dictionaries.
    """
    commands = []
    # Split text into sentences or phrases that might contain an object description.
    # This regex splits by periods, "and a", "and then a", etc., while keeping delimiters.
    sentences = re.split(r'(\.|\s+and a\s+|\s+and then a\s+)', text, flags=re.IGNORECASE)
    
    # Re-join sentences to handle splits correctly
    full_sentences = []
    temp_sentence = ""
    for s in sentences:
        temp_sentence += s
        if re.match(r'(\.|\s+and a\s+|\s+and then a\s+)', s):
            full_sentences.append(temp_sentence)
            temp_sentence = ""
    if temp_sentence:
        full_sentences.append(temp_sentence)

    for sentence in full_sentences:
        sentence = sentence.lower().strip()
        if not sentence:
            continue

        # --- Identify Shape ---
        shape_match = re.search(r'\b(cube|sphere|cylinder)\b', sentence)
        if not shape_match:
            continue
        
        shape = shape_match.group(1)
        command = {'shape': shape, 'params': {}, 'name': sentence}

        # --- Identify Parameters based on Shape ---
        if shape == 'cube':
            side_match = re.search(r'(side|size)\s+of\s+(\d+\.?\d*)', sentence) or \
                         re.search(r'(side|size)\s+(\d+\.?\d*)', sentence)
            if side_match:
                command['params']['side'] = float(side_match.group(2))
        
        elif shape == 'sphere':
            radius_match = re.search(r'radius\s+of\s+(\d+\.?\d*)', sentence) or \
                           re.search(r'radius\s+(\d+\.?\d*)', sentence)
            if radius_match:
                command['params']['radius'] = float(radius_match.group(2))

        elif shape == 'cylinder':
            radius_match = re.search(r'radius\s+(\d+\.?\d*)', sentence)
            height_match = re.search(r'height\s+(\d+\.?\d*)', sentence)
            if radius_match:
                command['params']['radius'] = float(radius_match.group(1))
            if height_match:
                command['params']['height'] = float(height_match.group(1))

        # --- Identify Common Attributes (Color, Position, Rotation) ---
        color_match = re.search(r'\b(red|green|blue|yellow|orange|purple|white|black|gray)\b', sentence)
        if color_match:
            command['params']['color'] = color_match.group(1)

        pos_match = re.search(r'at\s+(position\s+)?(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', sentence)
        if pos_match:
            command['params']['position'] = [float(pos_match.group(2)), float(pos_match.group(3)), float(pos_match.group(4))]
        
        commands.append(command)
        
    return commands
