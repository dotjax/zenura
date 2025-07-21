import os
from datetime import datetime

def text_to_file(text=None):
    if text is None:
        text = input("Enter text: ")
    
    # Create data/input directory if it doesn't exist
    os.makedirs("data/input", exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/input/text_{timestamp}.py"
    
    raw = text.encode('utf-8')
    zfill_w = 8

    print("Analysis:")
    prev_unit = None
    units = list(raw)
    
    # Build analysis data and collect delta/xor values
    analysis_lines = []
    delta_values = []
    xor_values = []
    
    for unit in units:
        char = chr(unit)
        analysis_lines.append(f'{char}: {unit} (dec) = {bin(unit)[2:].zfill(zfill_w)} (bin)')
        print(f"{char}: {unit} (dec) = {bin(unit)[2:].zfill(zfill_w)} (bin)")
        
        if prev_unit is not None:
            diff = unit - prev_unit
            xorv = unit ^ prev_unit
            delta_values.append(diff)
            xor_values.append(xorv)
            analysis_lines.append(f'  Delta from {chr(prev_unit)}: {diff} steps')
            analysis_lines.append(f'  XOR pattern: {bin(xorv)[2:].zfill(zfill_w)}')
            print(f"  Delta from {chr(prev_unit)}: {diff} steps")
            print(f"  XOR pattern: {bin(xorv)[2:].zfill(zfill_w)}")
        prev_unit = unit

    # Create file content
    file_content = f'''generated = "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
original_text = "{text}"
byte_count = {len(units)}

analysis = [
{chr(10).join(f'    "{line}",' for line in analysis_lines)}
]

text = """{text}"""
byte_values = {units}
encoding = "utf-8"
delta = {delta_values}
xor = {xor_values}
'''

    # Write to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(file_content)
    
    print(f"\nSaved to: {filename}")
    return units