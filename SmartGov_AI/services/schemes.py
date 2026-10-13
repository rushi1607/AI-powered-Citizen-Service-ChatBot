from services.storage import get_db

def search_schemes(query="", audience="citizen"):
    q = query.lower().strip()
    with get_db() as db:
        rows = db.execute("SELECT * FROM schemes ORDER BY name").fetchall()
    results = []
    for row in rows:
        item = dict(row)
        searchable = " ".join([
            item["name"], item["description"], item["audience"], item["keywords"]
        ]).lower()
        audience_match = audience in ("all", "any", "") or item["audience"] == audience or item["audience"] == "citizen"
        query_match = not q or q in searchable or any(word in searchable for word in q.split())
        if audience_match and query_match:
            results.append({
                "name": item["name"],
                "description": item["description"],
                "audience": item["audience"],
                "official_url": item["official_url"],
                "eligibility_note": item["eligibility_note"]
            })
    return results
