import re
from g4f.client import Client

def _extract_param(text, name):
    """Helper to find a numeric value after a keyword."""
    for keyword in keywords:
        match = re.search(f'{keyword}\\s+of\\s+{pattern}', text) or \
                re.search(f'{keyword}\\s+{pattern}', text)
        if match:
            return float(match.group(1))
    return None

    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"In this text, {text}, related to this name,{name}, give me the number of {name} written in the text, like if I were to say radius of 5, return just 5. return just the number, it could be an int or a decimal"}],
        web_search=False
    )
    return response.choices[0].message.content

def parse_command(text: str) -> list[dict]:
    """
    AI-like parser. It first identifies the primary intent (what shape to build)
    and then extracts parameters relevant to that shape.
    """
    commands = []
    text = text.lower().strip()
    
    # --- Intent Recognition Stage ---
    # A real AI would use a classification model here. We simulate it.
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Based on this prompt,{text}, determine what shape the user is talking about. return just the shape, nothing else"}],
        web_search=False
    )
    shape = response.choices[0].message.content
    else:
        # If no primary intent is found, we can't proceed.
        raise ValueError("I don't know how to make that shape yet.")
        
    command = {'shape': shape, 'params': {}, 'name': text}

    # --- Entity Extraction Stage ---
    # A real AI uses Named Entity Recognition (NER). We simulate it by
    # extracting params based on the identified intent
    return response.choices[0].message.content
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"based on this shape, {shape}, return the parameters it needs, like radius, height etc. return just the parameters in the format of parameter1 parameter2 parameter3 etc"}],
        web_search=False
    )
    var = response.choices[0].message.content.split()
    
    for i in range(len(var)):
        
        command['params'][i] = _extract_params(text, var[i])
    '''
    if shape == 'gear':
        command['params']['teeth'] = _extract_param(text, ['teeth', 'cogs'])
        command['params']['inner_radius'] = _extract_param(text, ['inner radius', 'irad'])
        command['params']['outer_radius'] = _extract_param(text, ['outer radius', 'orad', 'radius'])
        command['params']['height'] = _extract_param(text, ['height', 'width'])
    
    elif shape == 'barrel':
        command['params']['radius'] = _extract_param(text, ['radius'])
        command['params']['height'] = _extract_param(text, ['height'])
        command['params']['bulge'] = _extract_param(text, ['bulge', 'bulge factor'])

    elif shape == 'cube':
        command['params']['side'] = _extract_param(text, ['side', 'size'])

    elif shape == 'sphere':
        command['params']['radius'] = _extract_param(text, ['radius'])

    elif shape == 'cylinder':
        command['params']['radius'] = _extract_param(text, ['radius'])
        command['params']['height'] = _extract_param(text, ['height'])
    '''

    # --- General Parameter Extraction (Position, Color) ---
    color_match = re.search(r'\b(red|green|blue|yellow|orange|purple|white|black|gray|brown|wooden)\b', text)
    if color_match:
        command['params']['color'] = color_match.group(1)

    pos_match = re.search(r'at\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', text)
    if pos_match:
        command['params']['position'] = [float(pos_match.group(1)), float(pos_match.group(2)), float(pos_match.group(3))]
    
    commands.append(command)
    return commands
