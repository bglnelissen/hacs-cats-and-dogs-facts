# Cat Facts — Home Assistant HACS Integration

A Home Assistant integration that shows a new cat fact on a configurable schedule.

## Installation via HACS

1. Open HACS in Home Assistant
2. Go to Integrations
3. Click the three dots in the top right and choose "Custom repositories"
4. Add `https://github.com/bglnelissen/hacs-cat-facts` with category "Integration"
5. Search for "Cat Facts" and install
6. Restart Home Assistant
7. Go to Settings > Devices & Services > Add Integration > Cat Facts

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| JSON URL | [cat-facts-dataset](https://raw.githubusercontent.com/bglnelissen/cat-facts-dataset/main/cat_facts.json) | URL to a JSON file with facts |
| Random order | Yes | Pick a random fact on each update |
| Update interval | 6 hours | Hours between each new fact (1–168) |

The JSON file must be either a plain array of strings, or an object with a `facts` key containing an array of strings.

## Sensor

The integration creates one sensor per entry:

- **Entity**: `sensor.cat_facts_fact`
- **State**: The current cat fact (truncated to 255 characters if longer)
- **Attribute** `full_fact`: The full untruncated fact text

## Data source

The default dataset contains 509 unique cat facts merged from three open source datasets:

| Source | License |
|--------|---------|
| [alexwohlbruck/cat-facts](https://github.com/alexwohlbruck/cat-facts) | Apache-2.0 |
| [vadimdemedes/cat-facts](https://github.com/vadimdemedes/cat-facts) | MIT |
| [wh-iterabb-it/meowfacts](https://github.com/wh-iterabb-it/meowfacts) | MIT |

Dataset repository: [bglnelissen/cat-facts-dataset](https://github.com/bglnelissen/cat-facts-dataset)

## License

MIT
