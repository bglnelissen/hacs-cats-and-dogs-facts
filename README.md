# Cats and Dogs Facts: Home Assistant HACS Integration

A Home Assistant integration that shows a new cat or dog fact on a configurable schedule.

This integration used to be called Cat Facts (`cat_facts`). Version 2.0.0 renamed the domain to `cats_and_dogs_facts`, so after upgrading you add the integration again and update any dashboards that used `sensor.cat_facts_fact`.

## Installation via HACS

1. Open HACS in Home Assistant
2. Go to Integrations
3. Click the three dots in the top right and choose "Custom repositories"
4. Add `https://github.com/bglnelissen/hacs-cats-and-dogs-facts` with category "Integration"
5. Search for "Cats and Dogs Facts" and install
6. Restart Home Assistant
7. Go to Settings > Devices & Services > Add Integration > Cats and Dogs Facts

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| JSON URL | [cats_and_dogs_facts.json](https://raw.githubusercontent.com/bglnelissen/cats-and-dogs-facts-dataset/main/cats_and_dogs_facts.json) | URL to a JSON file with facts |
| Random order | Yes | Pick a random fact on each update |
| Update interval | 6h | Time between each new fact, for example 30m, 6h, 1d or 1d12h (max 7d) |

The JSON file must be either a plain array of strings, or an object with a `facts` key containing an array of strings.

For Dutch facts, use `https://raw.githubusercontent.com/bglnelissen/cats-and-dogs-facts-dataset/main/cats_and_dogs_facts.nl.json`. Every Dutch fact is at most 160 characters, so it fits on a small e-ink display.

## Entities

The integration creates one device per entry with two entities:

- **Sensor** `sensor.cats_and_dogs_facts_fact`: the current fact, also available as the attribute `fact`
- **Button** `button.cats_and_dogs_facts_next_fact`: show a new fact right away

## Data source

The default dataset contains 716 facts: 509 cat facts and 207 dog facts, mixed in one list.

| Source | License |
|--------|---------|
| [alexwohlbruck/cat-facts](https://github.com/alexwohlbruck/cat-facts) | Apache-2.0 |
| [vadimdemedes/cat-facts](https://github.com/vadimdemedes/cat-facts) | MIT |
| [wh-iterabb-it/meowfacts](https://github.com/wh-iterabb-it/meowfacts) | MIT |
| [DucNgn/Dog-Facts-API-v2](https://github.com/DucNgn/Dog-Facts-API-v2) | MIT |
| [kinduff/dog-api](https://github.com/kinduff/dog-api) (original collection of the dog facts) | none stated |

Dataset repository: [bglnelissen/cats-and-dogs-facts-dataset](https://github.com/bglnelissen/cats-and-dogs-facts-dataset)

The icon is the `paw` icon from [Material Design Icons](https://pictogrammers.com/library/mdi/) (Apache-2.0).

## License

MIT
