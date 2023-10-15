![powerline-k8s](https://res.cloudinary.com/j4ckofalltrades/image/upload/v1697278938/foss/gh-social-icons/powerline-k8s_arypmi.png)

[![PyPI](https://img.shields.io/pypi/v/powerline-k8s)](https://pypi.org/project/powerline-k8s/)
![PyPI_Python_Version](https://img.shields.io/pypi/pyversions/powerline-k8s)
[![Docs](https://img.shields.io/badge/docs-green?link=j4ckofalltrades.github.io%2Fpowerline--k8s)](https://j4ckofalltrades.github.io/powerline-k8s)
[![codecov](https://codecov.io/gh/j4ckofalltrades/powerline-k8s/branch/main/graph/badge.svg?token=J5GLE5ZY2V)](https://codecov.io/gh/j4ckofalltrades/powerline-k8s)

A custom [Powerline](https://github.com/powerline/powerline) segment for displaying the current Kubernetes context and namespace.

![](https://res.cloudinary.com/j4ckofalltrades/image/upload/v1623588713/foss/powerline-k8s_uc0cxj.png)

## Installation

### Using pip

`$ pip install powerline-k8s`

## Configuration

### Colorscheme

Add the following config items to your Powerline colorscheme config file (usually located at `~/.config/powerline/colorschemes/`),
see [Powerline Colorschemes](https://powerline.readthedocs.io/en/master/configuration/reference.html#colorschemes) for more info.

```json
{
  "k8s":           { "fg": "solarized:blue", "bg": "solarized:base02", "attrs": [] },
  "k8s_namespace": { "fg": "solarized:red",  "bg": "solarized:base02", "attrs": [] },
  "k8s_context":   { "fg": "solarized:blue", "bg": "solarized:base02", "attrs": [] },
  "k8s:divider":   { "fg": "gray4",          "bg": "solarized:base02", "attrs": [] }
}
```

### Segment

Add the following config item to your Powerline segments config file,
see [Powerline Segment reference](https://powerline.readthedocs.io/en/master/configuration/segments.html#segment-reference) for more info.

```json
{
  "function": "powerline_k8s.k8s",
  "priority": 30
}
```

- If adding the segment to the shell, edit `~/.config/powerline/themes/shell/default.json`.
- If adding the segment to the tmux status line, edit `~/.config/powerline/themes/tmux/default.json`.

### Toggle visibility

Toggle entire segment or specific section's visibility with the following environment variables:

- `POWERLINE_K8S_SHOW`
- `POWERLINE_K8S_SHOW_NS`

Note: Full segment visibility takes precedence over namespace section visibility.

```shell
# toggle segment visibility
$ POWERLINE_K8S_SHOW=0 powerline-daemon --replace # hide powerline-k8s segment
$ POWERLINE_K8S_SHOW=1 powerline-daemon --replace # show powerline-k8s segment (default)

# toggle namespace section visibility
$ POWERLINE_K8S_SHOW_NS=0 powerline-daemon --replace # hide namespace section
$ POWERLINE_K8S_SHOW_NS=1 powerline-daemon --replace # show namespace section (default)
```

Alternatively you can add the following function to your shell for easier toggling:

```shell
toggle_powerline_k8s() {
  case "$1" in
    # pass the '-ns' flag to toggle namespace visibility
    "-ns" | "--namespace")
      if [[ "${POWERLINE_K8S_SHOW_NS:-1}" -eq 1 ]]; then
        export POWERLINE_K8S_SHOW_NS=0
      else
        export POWERLINE_K8S_SHOW_NS=1
      fi
    ;;
    *)
      # toggle segment visibility
      if [[ "${POWERLINE_K8S_SHOW:-1}" -eq 1 ]]; then
        export POWERLINE_K8S_SHOW=0
      else
        export POWERLINE_K8S_SHOW=1
      fi
    ;;
  esac
}
```

## Demo

[![asciicast](https://asciinema.org/a/424536.svg)](https://asciinema.org/a/424536?autoplay=1&speed=2)


## Stats

![Alt](https://repobeats.axiom.co/api/embed/fbba579306e9c836bd6aa443e43637a0131c45f3.svg "Repobeats analytics image")
