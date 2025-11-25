def chunk_text(text, source, chunk_size=500):
    return [{"content": text[i:i+chunk_size], "metadata": {"source": source}}
            for i in range(0, len(text), chunk_size)]

