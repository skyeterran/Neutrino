import json

def uncache_scene(in_data):
    pure_data = {
        "meta": in_data["meta"],
        "graph": in_data["graph"]
    }
    raw_json = json.dumps(pure_data)

    # cache objects
    raw_cache = json.dumps(in_data["cache"])
    for key, value in in_data["cache"]["objects"].items():
        pointer = "#" + key
        raw_cache = raw_cache.replace(f'"{pointer}"', json.dumps(value))
    unpacked_object_cache = json.loads(raw_cache)

    # objects
    for key, value in unpacked_object_cache.items():
        print(json.dumps(value))
        pointer = "#" + key
        raw_json = raw_json.replace(f'"{pointer}"', json.dumps(value))

    # names
    for key, value in in_data["cache"]["names"].items():
        raw_json = raw_json.replace("@" + key, value)


    out_data = json.loads(raw_json)

    return out_data