import os
import firebase_admin
from firebase_admin import firestore, storage, credentials


current_dir = os.path.dirname(__file__)
firebase_json_path = os.path.join(current_dir, "firebase.json")

# Initialize Firebase Admin SDK
cred = credentials.Certificate(firebase_json_path)
firebase_admin.initialize_app(cred,{
    'storageBucket': 'finalyearproject-8c628.appspot.com' 
})

# Get a Firestore client
db = firestore.client()

# Reference to the Firebase Storage bucket
bucket = storage.bucket()


def read_documents(collection_name, parameters=None):
    print(f"Reading documents for {collection_name}!")
    try:
        # Create a reference to the collection
        collection_ref = db.collection(collection_name)

        if parameters:
            # Query documents based on parameters
            query = collection_ref
            for key, value in parameters.items():
                query = query.where(field_path=key, op_string='==', value=value)

            # Get documents
            documents = query.stream()
        else:
            # List all documents in the collection
            documents = collection_ref.stream()

        # Extract data from documents
        results = []
        for doc in documents:
            results.append(doc.to_dict())

        return results

    except Exception as e:
        print("An error occurred:", e)
        return None
    
def create_document(collection_name, data):
    print(f"Creating document in {collection_name}. Data :\n{data}\n")
    try:
        # Create a reference to the collection
        collection_ref = db.collection(collection_name)

       # Add the document to the collection
        result = collection_ref.add(data)

        # Extract document reference object from the result tuple
        document_ref = result[1]

        print("Document created with ID:", document_ref.id)
        return document_ref.id
        # return result

    except Exception as e:
        print("An error occurred:", e)
        return None

def get_document_by_id(collection_name, document_id):
    print(f"Getting document from {collection_name} with  {document_id}")
    try:
        # Create a reference to the document
        doc_ref = db.collection(collection_name).document(document_id)

        # Get the document
        doc = doc_ref.get()

        # Check if the document exists
        if doc.exists:
            return doc.to_dict()
        else:
            print(f"Document with ID {document_id} does not exist.")
            return None

    except Exception as e:
        print("An error occurred:", e)
        return None
    

def update_document(collection_name, document_id, update_data):
    print(f"Updating document in {collection_name}. ID: {document_id} \n{update_data}\n")
    try:
        # Create a reference to the document
        doc_ref = db.collection(collection_name).document(document_id)

        # Update the document
        doc_ref.update(update_data)

        print(f"Document with ID {document_id} updated successfully.")
        return True

    except Exception as e:
        print("An error occurred:", e)
        return False
    
def read_documents_startswith(collection_name, field_name, prefix):
    print(f"Reading documents in {collection_name}  who's '{field_name}' start's with '{prefix}' ")
    try:

        # Create a reference to the collection
        collection_ref = db.collection(collection_name)

        # Query documents where the field value starts with the prefix
        query = collection_ref.where(field_name, ">=", prefix).where(field_name, "<", prefix + u"\uf8ff")
        documents = query.stream()

        # Extract data from documents
        results = []
        for doc in documents:
            results.append(doc.to_dict())

        return results

    except Exception as e:
        print("An error occurred:", e)
        return None
    
def get_document_id(collection_name, query_params):
    print("Get document ID function called for ${collection_name}. Data : \n{query_params}\n")
    try:
        collection_ref = db.collection(collection_name)
        for field, value in query_params.items():
            collection_ref = collection_ref.where(field, '==', value)
        
        query_ref = collection_ref.stream()
        
        for doc in query_ref:
            return doc.id
        
        return None
    except Exception as e:
        print("An error occurred:", e)
        return "Error in Firebase operation"
    
def upload_to_firebase_storage(file, file_name, type):
    try:
        extension = ""
        if type ==  'profile_pictures':
            extension = 'jpeg'
        else:
            extension = 'pdf'
            
        # Destination path in Firebase Storage
        destination_blob_name = type +  "/" + file_name + "." + extension

        # Upload the file to Firebase Storage
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_file(file)

        print("File uploaded to Firebase Storage.")
        return True
    except Exception as e:
        print("An error occurred:", e)
        return False
    
def docuemnt_count(collection_name, query_params=None):
    try:
        print(f"Get document count function called for {collection_name}. Data:\n{query_params}\n")

        collection_ref = db.collection(collection_name)
        
        if query_params:
            for field, value in query_params.items():
                collection_ref = collection_ref.where(field, '==', value)
        
        query_ref = collection_ref.stream()
        
        document_count = sum(1 for _ in query_ref)
        return document_count
    except Exception as e:
        print("An error occurred:", e)
        return -1
    

def get_file_url(file_name, type):
    destination_blob_name = type +  "/" + file_name + ".pdf"
    blob = bucket.blob(destination_blob_name)
    blob.make_public()
    return blob.public_url

def upload_profile_picture(image_content, rollno):
    # Initialize the storage client
    bucket = storage.bucket()

    # Define the name for the image file and specify the folder path
    folder_path = "profile_pictures/"  # Specify the folder path here
    image_name = folder_path + rollno + ".jpg"

    # Create a blob in Firestore storage
    blob = bucket.blob(image_name)

    # Upload the image content to Firestore storage
    blob.upload_from_string(image_content, content_type='image/jpeg')

    # Get the public URL of the uploaded image
    blob.make_public()
    image_url = blob.public_url
    return image_url


def check_profile_picture_exists(roll_no):
    try:
        # Destination path in Firebase Storage
        destination_blob_name = "profile_pictures/" + roll_no + ".jpeg"
        # Check if the file exists in Firebase Storage
        blob = bucket.blob(destination_blob_name)
        return blob.exists()
    except Exception as e:
        print("An error occurred:", e)
        return False