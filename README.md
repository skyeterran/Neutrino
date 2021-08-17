# Neutrino

> A neutrino is a fermion (an elementary particle) that interacts only via the weak interaction and gravity. The neutrino is so named because it is electrically neutral and because its rest mass is so small that it was long thought to be zero. The rest mass of the neutrino is much smaller than that of the other known elementary particles excluding massless particles. Neutrinos typically pass through normal matter unimpeded and undetected.
- [Neutrino on Wikipedia](https://en.wikipedia.org/wiki/Neutrino)

# A minimal, human-readable exchange format for 3D scene data

## Goals/properties of the format

Neutrino should have:

1. Minimal core data structure
2. Human-readable syntax
3. Simple cross-platform integration
4. Safely extendable data structure

### Minimal core data structure

- No redundancy
- No junk data (anything that isn't universally relevant to the vast majority of 3D software)

### Human-readable syntax

- Clear, categorical data hierarchy (meshes → transforms, materials → texture maps, etc.)
- Stored via an ASCII format which can be directly opened and read by users (for instance, indented JSON files)
- Verbose data structures with simple English names (for example, named location/rotation/scale arrays in a transform dictionary rather than a nameless array of arrays which looks like Matrix code) (similar philosophy to Python and Ruby syntax)

### Simple cross-platform integration

- No hard requirements for storage format (although I am using and recommend JSON since it's human-readable, widely-supported, and directly converts to generic Python dictionaries)
- No application-specific data structures

### Safely extendable data structure

- Should be able to support arbitrary, additional data for specific pipeline needs
- Additional data will be discarded by the Neutrino preprocessor if it's not recognized by the target application. The core data structure can never be modified since it's the fallback.

# Format specification
*Note: This is very much a work-in-progress.*

## Neutrino Alpha

- settings [dict]
    - assets [dict]
    *Defines properties relating to the on-disk assets referenced.*
        - root_directory [string]
        *The root directory/path which will be prepended to each of the file paths referenced. Setting this to "" will allow file paths to be absolute, but that's a terrible idea. Please don't do that.*
    - units [dict]
    *The unit systems used by this scene. Currently only length is relevant, but it's safer to keep this as a dictionary for future extensibility for other types of measurement.*
        - length [string]
        *The unit of measurement used by the scene ("centimeters", "meters", "feet", etc.)*
    - axes [dict]
    *Describes the handedness of the axes used in the scene (what the up/right/forward axes are)*
        - up [string]
        *Describes the up axis of the scene ("x", "-x", "y", "-y", "z", or "-z")*
        - forward [string]
        *Describes the right axis of the scene ("x", "-x", "y", "-y", "z", or "-z")*
- scene [dict]
*The hierarchy of objects in the scene, stored as a recursive tree of objects and their children.*
    - {object name} [dict]
    *The name of the object in the scene hierarchy is the same as its name in the objects dictionary which details its properties below.*
        - transform [dict]
        *The object's transform in the scene.*
            - location [array]
            *List declaring X, Y, Z location values.*
            - rotation [array]
            *List declaring X, Y, Z rotation values.*
            - scale [array]
            *List declaring X, Y, Z scale values.*
        - children [dict]
        *A named dictionary of the object's children.*
            - {object name} [dict]
            *A child object, following the same dictionary format as its parent (including its own children)*
- objects [dict]
*A dictionary of named objects in the scene, each containing their properties.*
    - {object name} [dict]
    *The name of the object in the scene.*
        - type [string]
        *The type of object ("null", "mesh", "spotlight", etc.)*
        - properties [dict] [optional]
        *Data specific to the object's type.*
            - source_file [string] [optional] [used by: mesh]
            *The relative file path of the source file for this object, for example: an FBX file for a mesh.*
            - materials [array] [optional] [used by: mesh]
            *List of the names of the materials applied to the mesh, in order of material assignment.*
- materials [dict]
*A list of named materials in the scene.*
    - {material name} [dict]
        - parameters [dict]
        *A list of the material's parameters.*
            - {parameter name} [string]
            *The name of the material parameter.*
                - type [string]
                *The datatype of the parameter ("scalar", "vector", or "texture")*
                - value [array or string]
                *The value of the parameter, which depends on the parameter type:*
                - *If it's a scalar: a float declaring the value.*
                - *If it's a vector: an array of length 4 declaring RGBA values.*
                - *If it's a texture: the relative file path of the texture map.*

### Example

```json
{
	"settings": {
		"assets": {
			"root_directory": "/"
		},
		"units": {
			"length": "centimeters"
		},
		"axes": {
			"up": "z",
			"forward": "x"
		},
	},
	"scene": {
		"Light_Group": {
			"transform": {...},
			"children": {
				"KeyLight": {...},
				"FillLight": {...}
			}
		},
		"LargeWindow": {
			"transform": {
				"location": [
					88.61341857910156,
					-0.7978610992431641,
					4.113158702850342
				],
				"rotation": [
					-45.0,
					0.0,
					89.9997
				],
				"scale": [
					1.0,
					1.0,
					1.0
				]
			},
			"children": {
				"WindowHandle": {
					"transform": {...},
					"children": {...}
				}
			}
		},
		"MetalDoorframe": {
			"transform": {...},
			"children": {
				"WoodDoor_Damaged": {...}
			}
		}
	},
	"objects": {
		"Light_Group": {
			"type": "null"
		},
		"KeyLight": {
			"type": "spotlight",
			"properties": {...}
		},
		"FillLight": {...},
		"LargeWindow": {
			"type": "mesh",
			"properties": {
				"source_file": "Meshes/SM_LargeWindow_A.obj",
				"materials": [
					"M_Windows"
				]
			}
		},
		"WindowHandle": {...},
		"MetalDoorFrame": {...},
		"WoodDoor_Damaged": {...}
	},
	"materials": {
		"M_Windows": {
			"parameters": {
				"base_color": {
					"type": "texture",
					"value": "Textures/T_Windows_DiffColor.png"
				},
				"roughness": {
					"type": "scalar",
					"value": 0.23
				},
				"normal": {
					"type": "vector",
					"value": [
						0.5,
						0.5,
						1.0,
						1.0
					]
				}
			}
		}
	}
}
```
