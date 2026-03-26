
class TextChunker:

    def __init__(self, chunk_size=400, overlap=80):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str):

        # Split text into paragraphs
        paragraphs = text.split("\n")

        # Merge paragraphs into chunks
        chunks = []
        current_chunk = ""

        for para in paragraphs:
            if len(para.strip()) < 50:
                continue

            if len(current_chunk) + len(para) < self.chunk_size:
                current_chunk += (" " + para)

            else:
                chunks.append(current_chunk.strip())
                current_chunk = para
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Return the final chunks
        return chunks
