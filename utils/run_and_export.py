# Set-ups
import jupytext
import nbformat
from nbclient import NotebookClient
from nbconvert import MarkdownExporter
import sys
import os


# Get paths
in_path = os.path.join('/sandbox', sys.argv[1])
out_path = os.path.join('/sandbox', sys.argv[2])

# Read file
if in_path.rsplit('.', 1)[1].lower() == 'py':
    nb = jupytext.read(open(in_path))

else:
    nb = nbformat.read(open(in_path), as_version=4)

# Run file as notebook
client = NotebookClient(nb, timeout=60, kernel_name='python3')
client.execute()

# Export as Markdown file
md_exporter = MarkdownExporter()
body, _ = md_exporter.from_notebook_node(nb)

with open(out_path, "w") as f:
    f.write(body)

