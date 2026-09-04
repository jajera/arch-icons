# Arch Icons

[![GitHub Pages](https://github.com/jajera/arch-icons/actions/workflows/deploy.yml/badge.svg)](https://jajera.github.io/arch-icons/)

Browse and copy common architecture icons.

Companion libraries:
[AWS Icons](https://jajera.github.io/aws-icons/),
[GCP Icons](https://jajera.github.io/gcp-icons/),
[Azure Icons](https://jajera.github.io/azure-icons/),
[CNCF Icons](https://jajera.github.io/cncf-icons/).

## Features

- Search by product name, family, or tags
- Filter by product / family tags
- Copy SVG or PNG to the clipboard
- Download icons as SVG or PNG
- Light and dark themes
- White icon variants shown on a dark tile

## Statistics

- **86** SVG icon marks across HashiCorp, containers, VCS/CI, data, OS, and more
- Organized by product under `icons/<product>/`

## Usage

```shell
python3 -m http.server 8000
```

Open <http://localhost:8000>.

## Repository structure

```text
icons/
  <product>/     Official / brand-kit SVG marks
icons.json       Searchable metadata for the web app
scripts/         Metadata generation tooling
```

Regenerate metadata after adding icons:

```shell
python3 scripts/generate_icons_json.py
```

## Attribution

Icons come from official brand kits and project artwork. See `icons/SOURCE.txt`
and per-product `SOURCE.txt` files where present. Marks are trademarks of their
respective owners and are not relicensed under MIT.

## License

Website code is under the [MIT License](LICENSE). Icon assets remain under their
upstream brand terms.
