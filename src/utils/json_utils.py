"""JSON Utils"""

import json
from typing import Union

import aiofiles


async def read_json_async(file_path: str) -> Union[list, dict]:
    """Open and deserialize a JSON file to a Python object

    Args:
        file_path (`str`): Path to JSON file

    Returns:
        `Union[list, dict]`: Deserialized JSON as a Python object
    """
    async with aiofiles.open(file_path, mode="r", encoding="utf8") as jsonfile:
        raw_json = await jsonfile.read()
    deserialized_json = json.loads(raw_json)
    return deserialized_json


async def write_json_async(file_path: str, content: Union[list, dict]) -> None:
    """Serialize a Python object to a JSON string and write to a file

    Args:
        file_path (`str`): Path to JSON file
        content (`Union[list, dict]`): Python object to convert to JSON
    """
    async with aiofiles.open(file_path, mode="w", encoding="utf8") as jsonfile:
        await jsonfile.write(json.dumps(content, indent=4))
