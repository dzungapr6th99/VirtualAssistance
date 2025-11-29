from typing import List, Tuple
import re


def parse_markdown_with_sections(md_text: str) -> List[Tuple[str, str]]:
    """
    Return to list (section_title, text_block)
    """
    lines = md_text.replace("\r\n", "\n").split("\n")
    sections: List[Tuple[str, str]] = []
    current_title = "Introduction"
    buffer: List[str] = []
    
    def flush():
        nonlocal buffer, current_title
        if buffer:
            sections.append((current_title, "\n".join(buffer).strip()))
            buffer = []
        
    for line in lines:
        if re.match(r"^#{1,6}\s", line):
            flush()
            current_title = line.lstrip("#").strip()
        else:
            buffer.append(line)

    flush()
    return sections