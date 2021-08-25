import json

# create a new scene graph
def new_scene(name, cache = True):
    # create empty neutrino data
    data = {
        "meta": {
            "name": ("name", name),
            "scale": ("float", 1.0),
            "asset_path": ("path", "./")
        },
        "graph": {
            "scene": {},
            "assets": {}
        },
        "cache": {
            "names": {},
            "objects": {}
        },
        "internal": {
            "cache": cache,
            "max_object_key": {"index": 0},
            "max_name_key": {"index": 0}
        }
    }

    # return that empty data
    return data

# write the data to a JSON file
def save_scene(data, readable = False):
    # cache the scene
    if data["internal"]["cache"]:
        cache_scene(data)

    # create working copy of the scene data
    clean_data = data.copy()

    # get rid of internal data (not to be exported)
    del clean_data["internal"]
    
    filename = data["meta"]["name"][1].replace(" ", "") + ".json"
    with open(filename, "w") as outfile:
        if readable:
            json.dump(clean_data, outfile, indent = 4)
        else:
            json.dump(clean_data, outfile)

# get a new indexed object key and track it
def new_key(index):
    # get the indexed key
    key = hex(index["index"] + 1)

    # index the max key
    index["index"] += 1

    return key

# returns a cached name key from a string
def name_key(data, name):
    if data["internal"]["cache"]:
        name_pointer = ""

        # retrieve the proper key if it exists
        for key, value in data["cache"]["names"].items():
            if value == name:
                name_pointer = key
        
        # if the name pointer is still empty, make a new key and add it to the cache
        if name_pointer == "":
            name_pointer = new_key(data["internal"]["max_name_key"])
            data["cache"]["names"][name_pointer] = name

        return "@" + name_pointer
    else:
        return name

# add an asset to the graph
def add_asset(data, name, path):
    asset_data = {
        name_key(data, "name"): (name_key(data, "name"), name),
        name_key(data, "file"): (name_key(data, "path"), path)
    }
    
    # add the asset to the graph
    data["graph"]["assets"][new_key(data["internal"]["max_object_key"])] = (name_key(data, "asset"), asset_data)

# add an object to the scene
def spawn_object(data, name, asset):
    object_data = {
        name_key(data, "name"): (name_key(data, "name"), name),
        name_key(data, "asset"): "",
        name_key(data, "transform"): (name_key(data, "transform"), {
            name_key(data, "position"): (name_key(data, "vec3"), [0.0, 0.0, 0.0]),
            name_key(data, "rotation"): (name_key(data, "vec3"), [0.0, 0.0, 0.0]),
            name_key(data, "scale"): (name_key(data, "vec3"), [1.0, 1.0, 1.0])
        })
    }

    # get an asset key by the provided name
    for key, value in data["graph"]["assets"].items():
        if value[1][name_key(data, "name")][1] == asset:
            object_data[name_key(data, "asset")] = f"*{key}"

    # add the object to the scene
    data["graph"]["scene"][new_key(data["internal"]["max_object_key"])] = (name_key(data, "object"), object_data)

# recursively cache a single typeval tuple object
def cache_typeval(cache, typeval):
    # ignore if not typeval
    if type(typeval) == tuple:
        for key, value in typeval[1].items():
            # refuse to cache pointers (that's just... that would just be a nightmare)
            if type(value) == str:
                is_pointer = ("*" in value)
            else:
                is_pointer = False
            if not is_pointer:
                # cache member objects if it's a dictionary object
                if type(value[1]) == dict:
                    cache_typeval(cache, value)

                value_hash = hash(str(value))

                # track in cache
                if value_hash not in cache["objects"]:
                    cache_pointer = new_key(cache["key_index"])
                    cache["objects"][value_hash] = {"key": cache_pointer, "value": value, "count": 1}
                else:
                    cache_pointer = cache["objects"][value_hash]["key"]
                    cache["objects"][value_hash]["count"] += 1

                # replace real value with hash
                typeval[1][key] = "#" + cache_pointer

# if there's only one instance of a certain value, convert it back to the original value and destroy the cached version
def uncache_typeval(cache, typeval):
    for key, value in typeval[1].items():
        # refuse to cache pointers (that's just... that would just be a nightmare)
        if type(value) == str:
            is_pointer = ("*" in value)
        else:
            is_pointer = False
        if not is_pointer:
            # cache member objects if it's a dictionary object
            if type(value[1]) == dict:
                uncache_typeval(cache, value)

            value_hash = hash(str(value))

            # check if it occurs only once
            cache_key = value.replace("#", "")
            if cache[cache_key]["count"] <= 1:
                # replace the cache pointer in the scene data with its original value
                typeval[1][key] = cache[cache_key]["value"]

                # delete this object from the cache
                del cache[cache_key]

# cache the scene
def cache_scene(data):
    containers = [
        data["graph"]["scene"],
        data["graph"]["assets"]
    ]

    # build a cache of value hashes and pointers
    hash_cache = {"key_index": {"index": 0}, "objects": {}}
    for objects in containers:
        for key, value in objects.items():
            cache_typeval(hash_cache, value)

    # create a cache hashed with pointer keys instead of value hashes
    key_cache = {}
    for key, value in hash_cache["objects"].items():
        key_cache[value["key"]] = {"value": value["value"], "count": value["count"]}

    # prune the cache to only redirect repeat values
    for objects in containers:
        for key, value in objects.items():
            uncache_typeval(key_cache, value)

    # create a serialized cache usable by neutrino
    serial_cache = {}
    for key, value in key_cache.items():
        serial_cache[key] = value["value"]

    # add that cache to the neutrino scene data
    data["cache"]["objects"] = serial_cache