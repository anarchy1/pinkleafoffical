# Photo shot list

Seven store items have no photo file, so they fall back to the
`assets/photo-coming.svg` placeholder. They are all recent arrivals, and
they are the only products on the site without a picture.

Save each as `plants/<id>.jpg`. The build script picks the image up on the
next run and adds it to that product's structured data, which it cannot do
while the file is missing.

| Save as | Plant | Status | Price |
|---|---|---|---|
| `plants/X_venom_aurea.jpg` | Alocasia Venom Aurea | coming | 1800 ILS |
| `plants/X_angela_aurea.jpg` | Philodendron Angela Aurea Var | coming | 450 ILS |
| `plants/X_black_cardinal.jpg` | Philodendron Black Cardinal Var | coming | 1000 ILS / 250 ILS |
| `plants/X_radiatum.jpg` | Philodendron Radiatum Var | coming | 350 ILS |
| `plants/X_monstera_jungle_mint.jpg` | Monstera Jungle Mint | coming | 700 ILS |
| `plants/X_brown_beauty.jpg` | Philodendron Brown Beauty Var | coming | 500 ILS |
| `plants/X_atabapoense_pink.jpg` | Philodendron Atabapoense Pink Var | coming | 800 ILS |

Shooting notes, to match the rest of the catalogue:

- Square crop. The store renders every photo in a circle, so anything
  near the edges gets cut.
- Plain, light background. Cream or white wall works; the existing
  catalogue is shot that way.
- Fill the frame with one plant, shot straight on, not from above.
- Daylight, indirect. Flash flattens variegation, which is the thing
  people are paying for.
- 1400px on the long edge is plenty. `tools/optimize_images.py` will cap
  anything larger anyway.

After adding the files, run:

```
python3 tools/optimize_images.py
python3 tools/build_product_schema.py
```
