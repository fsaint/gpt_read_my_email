import yaml
from rich.console import Console
from rich.syntax import Syntax
from html import unescape




def print_yaml_highlighted(obj):
    """
    Convert a Python object to a YAML string and print it with syntax highlighting.

    Args:
    obj (Any): The Python object to be converted to YAML.
    """
    # Convert the object to a YAML-formatted string
    yaml_str = yaml.dump(obj, sort_keys=False)
    
    # Create a Syntax object with YAML syntax highlighting
    syntax = Syntax(yaml_str, "yaml", theme="monokai", line_numbers=True)
    
    # Create a Console object and print the Syntax object
    console = Console()
    console.print(syntax)

