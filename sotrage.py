import os
import logging
from minio import Minio
from minio.error import S3Error

# Setup basic logging to see console outputs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("graphify.storage")

# 1. MinIO Connection Settings 
# (Change these values if your local MinIO container uses different ports/credentials)
MINIO_CLIENT = Minio(
    endpoint=os.getenv("MINIO_ENDPOINT", "localhost:9000"),
    access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
    secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
    secure=os.getenv("MINIO_USE_SSL", "False").lower() in ("true", "1")
)

BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "graphify-code-maps")

def upload_graph_artifacts(context_id: str, git_commit_sha: str = "latest"):
    """
    Uploads graph.html and graph.json from the local graphify-out directory to MinIO.
    """
    # Configuration tracking path roots
    artifacts = {
        "graph.html": {
            "local_path": "graphify-out/graph.html",
            "content_type": "text/html"
        },
        "graph.json": {
            "local_path": "graphify-out/graph.json",
            "content_type": "application/json"
        }
    }
    
    # Verify or create destination target bucket
    try:
        if not MINIO_CLIENT.bucket_exists(BUCKET_NAME):
            MINIO_CLIENT.make_bucket(BUCKET_NAME)
            logger.info(f"Created new MinIO bucket: {BUCKET_NAME}")
    except S3Error as err:
        logger.error(f"Cannot connect to MinIO bucket framework: {err}")
        return False

    upload_errors = 0

    for filename, meta in artifacts.items():
        local_filepath = meta["local_path"]
        
        # Check if graphify has generated the target files yet
        if not os.path.exists(local_filepath):
            logger.warning(f"File variant not found: {local_filepath}. Run your graphify scan extraction first!")
            upload_errors += 1
            continue

        try:
            # Construct folder pathways inside MinIO storage
            primary_destination = f"{context_id}/graph/{filename}"
            history_destination = f"{context_id}/graph/history/{git_commit_sha}_{filename}"

            # Upload Primary Copy
            MINIO_CLIENT.fput_object(
                bucket_name=BUCKET_NAME,
                object_name=primary_destination,
                file_path=local_filepath,
                content_type=meta["content_type"]
            )

            # Upload Historical Copy
            MINIO_CLIENT.fput_object(
                bucket_name=BUCKET_NAME,
                object_name=history_destination,
                file_path=local_filepath,
                content_type=meta["content_type"]
            )
            
            logger.info(f"Successfully sent {filename} tracking variants to MinIO.")

        except S3Error as upload_err:
            logger.error(f"Error transferring {filename} object: {upload_err}")
            upload_errors += 1

    return upload_errors == 0

# ==========================================
# TEST RUNNER BLOCK
# ==========================================
if __name__ == "__main__":
    print("🚀 Running manual architecture upload script verification...")
    
    # Test IDs for indexing simulation
    TEST_CONTEXT = "context_ceo_test"
    TEST_COMMIT = "commit_init_27lakh"
    
    success = upload_graph_artifacts(context_id=TEST_CONTEXT, git_commit_sha=TEST_COMMIT)
    
    if success:
        print("✅ Pipeline Success! Files verified and pushed to MinIO container.")
    else:
        print("❌ Pipeline Completed with errors. Verify local files exist or check connection logs above.")
