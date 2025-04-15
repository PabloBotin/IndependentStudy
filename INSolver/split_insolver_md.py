import os

# === Settings ===
input_file = "docs/INSolver.md"  # Path to your master md file
output_dir = "docs/sections"     # Destination folder for split files

# === Prepare output directory ===
os.makedirs(output_dir, exist_ok=True)

# === Load the content ===
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# === Section titles to file names mapping ===
sections = {
    "# Introduction": "introduction.md",
    "# Governing Equations": "governing_equations.md",
    "# Discretization": "discretization.md",
    "# Grid Types": "grid_types.md",
    "# Algorithm": "algorithm.md",
    "# Poisson solver": "poisson_solver.md",
    "# Results": "results.md",
    "# Conclusion": "conclusion.md",
}

# === Splitting logic ===
current_file = None
buffer = []

for line in lines:
    line_strip = line.strip()

    if line_strip in sections:
        # Save previous buffer if exists
        if current_file and buffer:
            with open(os.path.join(output_dir, current_file), "w", encoding="utf-8") as f_out:
                f_out.writelines(buffer)
        
        # Start new section
        current_file = sections[line_strip]
        buffer = [line]
    else:
        if buffer is not None:
            buffer.append(line)

# Save the last section
if current_file and buffer:
    with open(os.path.join(output_dir, current_file), "w", encoding="utf-8") as f_out:
        f_out.writelines(buffer)

print("✅ All sections split and saved in", output_dir)
