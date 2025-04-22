from typing import List, Union

# Sway Tree types
SwayNode = {
    "id": int,
    "name": str,
    "type": str,
    "focused": bool,
    "marks": List[str],
    "nodes": List["SwayNode"],
    # ...other properties
}
