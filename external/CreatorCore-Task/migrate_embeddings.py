from app import app, db, model, Generation

if __name__ == '__main__':
    with app.app_context():
        # Find generations without embeddings
        gens_without_emb = Generation.query.filter(Generation.embedding.is_(None)).all()
        
        for gen in gens_without_emb:
            # Generate embedding
            emb = model.encode(gen.text).tolist()
            gen.embedding = emb
            # Score is already default 0.0
        
        db.session.commit()
        print(f"Migrated embeddings for {len(gens_without_emb)} records")