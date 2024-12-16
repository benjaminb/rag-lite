import chromadb


def main():
    client = chromadb.PersistentClient(path='/mnt/efs/chroma'),
    client.delete_collection('general')


if __name__ == "__main__":
    main()
