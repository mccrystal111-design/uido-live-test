# UiDo — Google Earth Studio Hole 2 capture

Target: Overstone Park Hole 2. Controlled imagery-acquisition test for the UiDo pixel tagger.

Known green coordinates:
- Front: 52.2762446, -0.8166103
- Middle: 52.2761187565, -0.8166885565
- Back: 52.2759866, -0.8167443

Do not add the field-test tee GPS to the Earth Studio project. It is validation data only.

## Earth Studio setup
1. Open https://earth.google.com/studio/
2. Create a new project.
3. Set project dimensions to 4096 x 2304.
4. Navigate to the Hole 2 green using the middle coordinate above.
5. Use a top-down / overhead camera with 0 degree tilt and north-up.
6. Frame enough ground to include the green and the complete likely tee/fairway corridor. Start generous rather than tightly cropping the green.
7. Import hole2-kml.kml as an overlay. It shows the supplied green reference only; it is not part of image classification.
8. Set render texture quality to High.
9. Hide the KML overlay before the final capture if a clean imagery input is wanted.
10. Use Snapshot to save the still JPG. Earth Studio saves snapshots at project resolution.
11. Keep the original JPG unchanged. Do not crop, resize, sharpen, recolour, or remove attribution.

## Why 4096 x 2304?
Earth Studio documents a maximum project resolution of 4096 x 2304 and says High texture quality loads the highest possible texture quality available at the location.

## Next step
Upload the resulting JPG into the UiDo conversation. The pixel-tagger test will use that exact image as its fixed source.

## Licensing / attribution
Earth Studio automatically places Google Earth / imagery-provider attribution on rendered imagery. Google states that attribution must remain visible when Earth Studio content is shown. Treat this render as a development/test input until commercial imagery licensing is resolved.
