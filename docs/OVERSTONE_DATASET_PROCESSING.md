# Overstone dataset processing

The Overstone build is split into source acquisition and processing.

## Input
- Authoritative OSM capture: persisted in UiDo Library.
- AOI: overstone-aoi-shapefile.zip, EPSG:27700.
- EA VAP coverage: SP8064, SP8065, SP8164, SP8165.
- EA National LiDAR coverage: SP8060, SP8065.

## Processing order
1. Acquire original source tiles without modification.
2. Verify checksums and source metadata.
3. Clip working copies to AOI plus a safety buffer.
4. Build raster-aligned source layers.
5. Register/validate OSM against imagery only from measured control points.
6. Derive feature candidates; preserve source geometry and provenance.
7. Derive LiDAR terrain/canopy layers.
8. Fuse into the provider-neutral course model.
9. Export a compact player course package.

## Production acquisition rule
The EA survey portal is a development fallback, not production-ready until retrieval is demonstrated programmatically without human intervention.
