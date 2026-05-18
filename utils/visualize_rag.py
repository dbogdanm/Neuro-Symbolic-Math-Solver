import chromadb
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import os
import argparse

def visualize_embeddings(db_path="./chroma_db_reguli", collection_name="reguli_matematice", output_file="rag_visualization.png", dims=2):
    print(f"Loading ChromaDB from {db_path}...")
    if not os.path.exists(db_path):
        print(f"Error: Database path '{db_path}' does not exist.")
        return

    client = chromadb.PersistentClient(path=db_path)
    
    try:
        collection = client.get_collection(name=collection_name)
    except Exception as e:
        print(f"Error: Could not find collection '{collection_name}': {e}")
        collections = client.list_collections()
        if collections:
            print(f"Available collections: {[c.name for c in collections]}")
        return

    count = collection.count()
    print(f"Retrieving data from collection '{collection_name}' ({count} items)...")
    if count == 0:
        print("Collection is empty.")
        return

    data = collection.get(include=['embeddings', 'metadatas', 'documents'])
    
    embeddings = data.get('embeddings')
    if embeddings is None or len(embeddings) == 0:
        print("No embeddings found in the database. Ensure they are stored.")
        return
    
    embeddings = np.array(embeddings)
    print(f"Embeddings shape: {embeddings.shape}")

    # Use PCA to reduce dimensions if they are too high, then t-SNE for better 2D/3D layout
    print(f"Reducing dimensions to {dims}D...")
    if embeddings.shape[1] > 50:
        pca = PCA(n_components=50)
        embeddings_reduced = pca.fit_transform(embeddings)
    else:
        embeddings_reduced = embeddings
    
    tsne = TSNE(n_components=dims, random_state=42, perplexity=min(30, len(embeddings)-1))
    embeddings_low_dim = tsne.fit_transform(embeddings_reduced)

    print("Plotting...")
    fig = plt.figure(figsize=(12, 10))
    
    if dims == 3:
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(embeddings_low_dim[:, 0], embeddings_low_dim[:, 1], embeddings_low_dim[:, 2], 
                            alpha=0.6, c=np.arange(len(embeddings)), cmap='viridis', edgecolors='w', s=50)
        ax.set_xlabel("t-SNE 1")
        ax.set_ylabel("t-SNE 2")
        ax.set_zlabel("t-SNE 3")
        fig.colorbar(scatter, label='Index')
    else:
        plt.scatter(embeddings_low_dim[:, 0], embeddings_low_dim[:, 1], 
                    alpha=0.6, c=np.arange(len(embeddings)), cmap='viridis', edgecolors='w', s=50)
        plt.xlabel("t-SNE 1")
        plt.ylabel("t-SNE 2")
        plt.colorbar(label='Index')

    # Optionally add some labels for a few points
    num_labels = min(8, len(embeddings))  # Reduced number of labels
    indices = np.random.choice(len(embeddings), num_labels, replace=False)
    for i in indices:
        # Shorter label text (max 20 chars) to prevent overlap
        label = data['documents'][i][:20].strip() + "..."
        if dims == 3:
            ax.text(embeddings_low_dim[i, 0], embeddings_low_dim[i, 1], embeddings_low_dim[i, 2], 
                    label, fontsize=7, fontweight='bold', alpha=0.9, 
                    bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', pad=0.1))
        else:
            plt.annotate(label, (embeddings_low_dim[i, 0], embeddings_low_dim[i, 1]), 
                         fontsize=7, alpha=0.8, fontweight='bold')

    plt.title(f"{dims}D Visualization of RAG Embeddings ({collection_name})")
    plt.grid(True, linestyle='--', alpha=0.5)
    
    output_path = os.path.join(os.getcwd(), output_file)
    plt.savefig(output_path)
    print(f"Visualization saved to {output_path}")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize ChromaDB embeddings in 2D or 3D.")
    parser.add_argument("--db", type=str, default="./chroma_db_reguli", help="Path to ChromaDB persistent storage.")
    parser.add_argument("--col", type=str, default="reguli_matematice", help="Collection name.")
    parser.add_argument("--out", type=str, default="rag_visualization_3d.png", help="Output image file.")
    parser.add_argument("--dims", type=int, default=3, choices=[2, 3], help="Number of dimensions (2 or 3).")
    
    args = parser.parse_args()
    
    # Change directory to the inner project folder if needed
    inner_dir = "Neuro-Symbolic-Math-Solver"
    if os.path.exists(inner_dir) and os.path.isdir(inner_dir):
        os.chdir(inner_dir)
        # Adjust default paths if we just changed dir
        if args.db.startswith("./"):
            args.db = args.db # remains same relative to new cwd
    
    visualize_embeddings(db_path=args.db, collection_name=args.col, output_file=args.out, dims=args.dims)
