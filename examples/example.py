#!/usr/bin/env python3
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
