def disc_schema(disc) -> dict:
    return {"id":str(disc["_id"]),
            "title":disc["title"],
            "artist":disc["artist"],
            "genre":disc["genre"],
            "year":disc["year"],
            "label":disc["label"]}