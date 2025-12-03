from rag import SimpleRAG

if __name__ == "__main__":
    rag = SimpleRAG()
    rag.ingest("""
    This is Deepanshu's meeting note about the ISRO project.
    Key points:
    - Launch window scheduled for March.
    - Fuel checks must be completed by Jan 15.
    - Next sync-up meeting on Monday morning.
    """)

    question = "When is the fuel check supposed to be completed?"
    print("\nQUESTION:", question)

    result = rag.query(question)
    print("\nRETRIEVED MEMORY:\n", result)
