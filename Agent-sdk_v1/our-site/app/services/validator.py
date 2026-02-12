from database import projects_collection

def validate_api_key(api_key: str):
    project = projects_collection.find_one({"api_key": api_key})
    if not project:
        return None
    return project
