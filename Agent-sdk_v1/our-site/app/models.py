from datetime import datetime

def build_log(doc, meta):
    return {
        "project": meta["project"],
        "environment": meta["environment"],
        "type": doc.get("type"),
        "message": doc.get("message"),
        "data": doc,
        "created_at": datetime.utcnow()
    }