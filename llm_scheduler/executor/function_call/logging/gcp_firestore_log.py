# Cloud firestore logging for the executor
import json
import time
from datetime import datetime
from google.cloud import firestore
from llm_scheduler.execution_environment.execution_environment import get_execution_id

# TODO(yaoyiheng): This should query environment config file to
#                  figure out which project collection to write to
def gcp_firestore_log(request: str) -> str:
    """Write a document to a Firestore collection.
    
    Args:
        request: JSON string containing:
            - collection: Name of the Firestore collection
            - document_id: Optional ID for the document. If not provided, one will be generated
            - data: Dict of data to write to the document
            
    Returns:
        JSON string containing:
            - status: "success" or "error"
            - document_id: ID of the created document
            - error: Error message if status is "error"
    """
    try:
        # Parse request
        request_data = json.loads(request)
        collection = request_data.get('collection')
        data = request_data.get('data', {})
        
        if not collection:
            raise ValueError("Collection name is required")
            
        # Add metadata
        data['timestamp'] = datetime.now().isoformat()

        # Add execution batch id
        data['execution_id'] = get_execution_id()

        # Initialize Firestore client
        db = firestore.Client()
        
        # Get collection reference
        collection_ref = db.collection(collection)
        
        # Create document
        doc_ref = collection_ref.document()
        
        # Write data
        doc_ref.set(data)
        
        # Return success response
        response = {
            'status': 'success',
            'document_id': doc_ref.id
        }

    except Exception as e:
        # Return error response
        response = {
            'status': 'error',
            'error': str(e)
        }
    
    return json.dumps(response)
