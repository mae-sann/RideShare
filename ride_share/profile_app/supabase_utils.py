import os
from supabase import create_client, Client
from django.conf import settings

def get_supabase_client() -> Client:
    """Initialize and return a Supabase client."""
    supabase_url = os.getenv('SUPABASE_URL')
    
    # Try service role key first (bypasses RLS), fallback to anon key
    supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY') or os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL and Key must be set in environment variables")
    
    print(f"DEBUG: Connecting to Supabase with URL: {supabase_url}")
    return create_client(supabase_url, supabase_key)

def upload_profile_picture_to_supabase(file, user_id: str) -> str:
    """
    Upload a profile picture to Supabase Storage and return the public URL.
    """
    try:
        supabase = get_supabase_client()
        
        # Generate a unique filename
        file_extension = os.path.splitext(file.name)[1].lower()
        if file_extension not in ['.jpg', '.jpeg', '.png']:
            raise ValueError("Only JPG and PNG files are allowed")
            
        # Simple filename without folder structure
        filename = f"profile_{user_id}{file_extension}"
        
        # Read the file content
        file_content = file.read()
        
        print(f"DEBUG: Uploading file {filename} to Supabase storage")
        print(f"DEBUG: File size: {len(file_content)} bytes")
        
        # Upload to Supabase Storage
        print(f"DEBUG: Starting upload to profile-pictures bucket...")
        result = supabase.storage.from_('profile-pictures').upload(
            path=filename,
            file=file_content,
            file_options={"content-type": file.content_type}
        )
        
        print(f"DEBUG: Upload result: {result}")
        
        if hasattr(result, 'error') and result.error:
            print(f"DEBUG: Upload error details: {result.error}")
            raise Exception(f"Upload failed: {result.error}")
        
        # Get the public URL
        print(f"DEBUG: Getting public URL for {filename}")
        public_url = supabase.storage.from_('profile-pictures').get_public_url(filename)
        print(f"DEBUG: Public URL: {public_url}")
        
        return str(public_url)
        
    except Exception as e:
        print(f"Error uploading profile picture: {str(e)}")
        import traceback
        print(f"DEBUG: Full upload error traceback: {traceback.format_exc()}")
        raise

def delete_profile_picture(url: str) -> bool:
    """
    Delete a profile picture from Supabase Storage.
    """
    try:
        if not url:
            return False
            
        # Extract the file path from the URL
        file_path = url.split('/')[-1]
        if not file_path:
            return False
        
        # Delete the file
        supabase = get_supabase_client()
        result = supabase.storage.from_('profile-pictures').remove([file_path])
        
        return True
        
    except Exception as e:
        print(f"Error deleting profile picture: {str(e)}")
        return False

def update_or_create_profile(user_id: str, profile_data: dict) -> bool:
    """
    Update or create profile data in Supabase table.
    """
    try:
        supabase = get_supabase_client()
        
        # Check if profile exists
        print(f"DEBUG: Checking if profile exists for user_id: {user_id}")
        response = supabase.table('profiles').select('*').eq('user_id', user_id).execute()
        print(f"DEBUG: Profile check response: {response}")
        
        if response.data:
            print(f"DEBUG: Updating existing profile with data: {profile_data}")
            update_response = supabase.table('profiles').update(profile_data).eq('user_id', user_id).execute()
            print(f"DEBUG: Update response: {update_response}")
            
            # Check if update was successful
            if hasattr(update_response, 'data') and update_response.data:
                print("DEBUG: Update successful")
                return True
            else:
                print("DEBUG: Update failed - no data returned")
                return False
        else:
            print(f"DEBUG: Creating new profile with data: {profile_data}")
            profile_data['user_id'] = user_id
            insert_response = supabase.table('profiles').insert(profile_data).execute()
            print(f"DEBUG: Insert response: {insert_response}")
            
            # Check if insert was successful
            if hasattr(insert_response, 'data') and insert_response.data:
                print("DEBUG: Insert successful")
                return True
            else:
                print("DEBUG: Insert failed - no data returned")
                return False
        
    except Exception as e:
        print(f"Error updating profile data: {str(e)}")
        import traceback
        print(f"DEBUG: Full database error traceback: {traceback.format_exc()}")
        return False