import os
from supabase import create_client, Client
from django.conf import settings

def get_supabase_client() -> Client:
    """Initialize and return a Supabase client."""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL and Key must be set in environment variables")
    
    return create_client(supabase_url, supabase_key)

def upload_profile_picture(file, user_id: str) -> str:
    """
    Upload a profile picture to Supabase Storage and return the public URL.
    
    Args:
        file: The file object to upload
        user_id: The ID of the user
        
    Returns:
        str: Public URL of the uploaded file
    """
    try:
        supabase = get_supabase_client()
        
        # Generate a unique filename
        file_extension = os.path.splitext(file.name)[1].lower()
        if file_extension not in ['.jpg', '.jpeg', '.png']:
            raise ValueError("Only JPG and PNG files are allowed")
            
        filename = f"profile_{user_id}_{os.urandom(8).hex()}{file_extension}"
        file_path = f"profile_pictures/{filename}"
        
        # Read the file content
        file_content = file.read()
        
        # Upload to Supabase Storage
        supabase.storage.from_('profile-pictures').upload(
            file_path,
            file_content,
            {"content-type": file.content_type}
        )
        
        # Get the public URL
        url = supabase.storage.from_('profile-pictures').get_public_url(file_path)
        
        return url
        
    except Exception as e:
        # Log the error and re-raise
        print(f"Error uploading profile picture: {str(e)}")
        raise

def delete_profile_picture(url: str) -> bool:
    """
    Delete a profile picture from Supabase Storage.
    
    Args:
        url: The URL of the file to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        if not url:
            return False
            
        # Extract the file path from the URL
        file_path = url.split('/')[-1]
        if not file_path:
            return False
            
        # Add the folder prefix if needed
        if not file_path.startswith('profile_pictures/'):
            file_path = f"profile_pictures/{file_path}"
        
        # Delete the file
        supabase = get_supabase_client()
        result = supabase.storage.from_('profile-pictures').remove([file_path])
        
        return True
        
    except Exception as e:
        print(f"Error deleting profile picture: {str(e)}")
        return False
