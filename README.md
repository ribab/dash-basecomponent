# Dash BaseComponent

A BaseComponent class for building modular Plotly Dash apps.

See [this article](https://www.codingwithricky.com/2025/02/15/dash-basecomponent/) for more info.

## Installation

To install the `dash-basecomponent` package, use the following command:

```bash
pip3 install dash-basecomponent
```

## Usage

To use these components in your own Dash application, simply import the component you want to use and add it to your application's layout.

For example:
```python
from dash import Dash, html, callback
from dash_basecomponent import BaseComponent as bc

class Counter(html.Div, bc):
    def __init__(self, **kwargs):
        super().__init__([
            html.Button("Increment", id=self.child_id("button")),
            html.Span("0", id=self.child_id("count"), style={"marginLeft": "10px"}),
        ], **kwargs)
    
    @callback(
        bc.ChildOutput("count", "children"),
        bc.ChildInput("button", "n_clicks"),
        prevent_initial_call=True
    )
    def increment_count(n_clicks):
        return str(n_clicks)

app = Dash(__name__)
app.layout = Counter()

if __name__ == "__main__":
    app.run_server(debug=True)
```

## Examples

The `examples` directory contains several example applications that demonstrate how to use these components.

* `hello_world.py`: An example application that uses the `InputCombiner` and `ExpandContract` components.
* `tic_tac_toe.py`: An example application that uses the `Game` component.
* `snake.py`: An example application that uses the `SnakeGameBoard` component.
* `example.py`: An example application that uses the `Counter` component.

## Contributing

Contributions to this project are welcome. If you have a new component you'd like to add, or if you've found a bug in one of the existing components, please submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
