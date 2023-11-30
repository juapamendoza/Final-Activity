def passenger_schema(passenger) -> dict:
    return {"id":str(passenger["_id"]),
            "identifier":passenger["identifier"],
            "name":passenger["name"],
            "survived":passenger["survived"],
            "sex":passenger["sex"],
            "age":passenger["age"]}