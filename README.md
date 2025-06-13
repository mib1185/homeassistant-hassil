# HassIL

The Home Assistant Intent Language (HassIL) parser for [intents](https://github.com/home-assistant/intents).


## Dependencies

* PyYAML


## Installation

Run the `script/setup` script to automatically create a virtual environment and install the requirements.


# Running

``` sh
python3 -m hassil <yaml_file_or_directory> [<yaml_file_or_directory> ...]
```

Once loaded, you may type in a sentence and see what intent it matches.
For example:

``` sh
python3 -m hassil examples/en.yaml --areas 'living room'
what is the temperature in the living room
{'intent': 'HassClimateGetTemperature', 'area': 'living room', 'domain': 'climate'}
```

Make sure to provide area names with `--areas`. Device or entity names can be provided with `--names`.

``` sh
python3 -m hassil examples/en.yaml --areas office --names trapdoor
open the trapdoor in the office
{'intent': 'HassOpenCover', 'name': 'trapdoor', 'area': 'office'}
```


### Sampling Sentences

Sentences for each intent can be sampled from the intent YAML files:

``` sh
python3 -m hassil.sample examples/en.yaml -n 1
{"intent": "HassTurnOn", "text": "turn on the entity"}
{"intent": "HassTurnOff", "text": "turn off the entity"}
{"intent": "HassOpenCover", "text": "open the entity in the area"}
{"intent": "HassCloseCover", "text": "close the entity in the area"}
{"intent": "HassLightsSet", "text": "set the entity color to red"}
{"intent": "HassClimateSetTemperature", "text": "set temperature to 0 degrees in the area"}
{"intent": "HassClimateGetTemperature", "text": "what is the temperature in the area"}
```

The `--areas` and `--names` arguments are the same from `python3 -m hassil`, but default to generic "area" and "entity" terms.

Exclude the `-n` argument to sample all possible sentences.


## Sentence Templates

Uses a custom parser written in Python.

* Alternative words or phrases
  * `(red|green|blue)`
  * `turn(s|ed|ing)`
* Optional words or phrases
  * `[the]`
  * `[this|that]`
  * `light[s]`
* Permutations of words or phrases
  * `(patience; you must have) my young Padawan`
  * `is [the] light (on; in <area>)`
* Slot Lists
  * `{list_name}`
  * `{list_name:slot_name}`
  * Refers to a pre-defined list of values in YAML (`lists`), either global or local (particular to the intent to which the sentence refers)
* Expansion Rules
  * `<rule_name>`
  * Refers to a pre-defined expansion rule in YAML (`expansion_rules`), either global or local (particular to the intent to which the sentence refers)


## YAML Format

``` yaml
language: "<language code>"
intents:
  <intent name>:
    data:
      # List of sentences/slots/etc.
      - sentences:
          - "<sentence template>"
          - "<sentence template>"
        # Optional
        slots:
          # Fixed slots for the recognized intent
          <name>: <value>
        requires_context:
          # Must be present in match context
          <name>: # Any provided value is good
        excludes_context:
          # Must NOT be present in match context
          <name>: <value or list>
        expansion_rules:
          # Expansion rules which only apply to the intent, referenced as <rule_name>
          <rule_name>: <sentence template>
        lists:
          # Lists which apply only to the current set of sentences, referenced as {list_name} or {list_name:slot_name}
          <list name>:
            values:
              # See below for other possible types
              - "items"
              - "in list"
        metadata:
          # Arbitrary key/value pairs that will be available in the result
          <key>: <value>

# Optional lists of items that become alternatives in sentence templates
lists:
  # Referenced as {list_name} or {list_name:slot_name}
  <list name>:
    values:
      - "items"
      - "in list"
      - in: "text in"
        out: <value for slot>
        # Optional
        context:
          <name>: <value>
        metadata:
          # Arbitrary key/value pairs that will be available in the result
          <key>: <value>
  <range_name>
    range:
      type: "number"
      from: 0
      to: 100  # inclusive
      multiplier: 1.0  # multiply to get final value
  <wildcard_name>
    wildcard: true

# Optional rules that are expanded in sentence templates
expansion_rules:
  # Referenced as <rule_name>
  <rule_name>: "<sentence template>"

# Optional words that the intent recognizer can skip during recognition
skip_words:
  - "<word>"
```
