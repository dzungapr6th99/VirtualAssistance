from typing import List


def chunk_text(text:str, max_chars: int=1000, overlap:int=200)-> List[str]:
    words = text.split()
    chunks = List[str] = []
    current: List[str] = []

    def current_len():
        return sum(len(w) for w in current) + max(0, len(current) -1)
    
    for w in words:
        if (current_len() + 1 + len(w)) > max_chars:
            chunk = " ".join(current).strip()
            if chunk:
                chunks.append(chunk)
            if overlap > 0 and chunk:
                tail = chunk[-overlap:]
                current = tail.split()
            else:
                current = []
        current.append(w)
    
    if current: 
        chunks.append(" ".join(current).strip())
    
    return chunks

