import subprocess
import sys

result = subprocess.run(
    ['python', 'scripts/frontmatter_validator.py'],
    capture_output=True,
    cwd='d:/AI/task/gongkao-seo'
)
output = result.stdout.decode('utf-8', errors='replace')
stderr = result.stderr.decode('utf-8', errors='replace')
combined = output + stderr

# Write to a result file
with open('d:/AI/task/gongkao-seo/validate_result.txt', 'w', encoding='utf-8') as f:
    f.write(f"Exit code: {result.returncode}\n")
    f.write("=== STDOUT ===\n")
    f.write(output)
    f.write("\n=== STDERR ===\n")
    f.write(stderr)

print("Done, check validate_result.txt")
print(f"Exit code: {result.returncode}")
# Print last 30 lines
lines = combined.split('\n')
for line in lines[-30:]:
    sys.stdout.buffer.write((line + '\n').encode('utf-8', errors='replace'))
