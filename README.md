# Neutrino
## A flexible exchange format for 3D scene data

> A neutrino is a fermion (an elementary particle) that interacts only via the weak interaction and gravity. The neutrino is so named because it is electrically neutral and because its rest mass is so small that it was long thought to be zero. The rest mass of the neutrino is much smaller than that of the other known elementary particles excluding massless particles. Neutrinos typically pass through normal matter unimpeded and undetected.
- [Neutrino on Wikipedia](https://en.wikipedia.org/wiki/Neutrino)

## Goals/properties of the format

Neutrino should have:

1. Reliable core data structure
3. Simple cross-platform integration
4. Safe extensibility

### Reliable core data structure

- No redundancy
- Explicit data types
- No junk data (anything that isn't universally relevant to the vast majority of 3D software)
- Non-hierarchical structure which can facilitate conversion between different softwares' conventions
    - *For example: Many softwares use DAGs (Directed Acyclic Graphs) to structure their scenes, but not all of them. Neutrino should not be limited to any specific software's convention.*

### Human-readable syntax

- Clear, categorical data hierarchy (meshes → transforms, materials → texture maps, etc.)
- Stored via an ASCII format which can be directly opened and read by users
- Verbose data structures with simple English names (for example, named location/rotation/scale arrays in a transform dictionary rather than a nameless array of arrays which looks like Matrix code) (similar philosophy to Python and Ruby syntax)

### Simple cross-platform integration

- No application-specific data structures

### Safe extensibility

- Should be able to support arbitrary, additional data for specific pipeline needs
- Additional data will be discarded by the Neutrino preprocessor if it's not recognized by the target application. The core data structure can never be modified since it's the fallback.

# Format specification
*Note: This is very much a work-in-progress.*

## Neutrino Alpha

### Example

```
@{
    string,
    float,
    int
}
#{
    2:"100"
}
*{
    &0,
    0:"Hello, world! Here's a bunch of special characters: @#*{},,/|,{{}#@*",
    1:"512.0",
    &0
}
```
