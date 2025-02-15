#!/usr/bin/env python3
from dash import Dash, html, dcc, callback, MATCH, Output, Input, State, no_update
import os, sys
from dash_basecomponent import BaseComponent as bc

class InputCombiner(html.Div, bc):

    def __init__(self, **kwargs):
        super().__init__(children=[
            dcc.Input(id=self.child_id('input_1'), type='text', placeholder='Input 1', value='Hello'),
            dcc.Input(id=self.child_id('input_2'), type='text', placeholder='Input 2', value='World'),
        ], **kwargs, **{"data-value": ""})

        @callback(
            Output(self.id, 'data-value'),
            Input(self.child_id('input_1'), 'value'),
            Input(self.child_id('input_2'), 'value'),
        )
        def combine_inputs(input_1, input_2):
            return str(input_1) + ' ' + str(input_2)

class InfiniteHelloWorld(html.Div, bc):

    def __init__(self, initial_text='Hello World', **kwargs):
        super().__init__([
            html.Div(initial_text, id=self.child_id('text')),
            html.Div(
                html.Button('MORE', id=self.child_id('more_button')),
                id=self.child_id('more_content')
            ),
            # interval of every 5 seconds
            dcc.Interval(id=self.child_id('interval'), interval=1000, n_intervals=0)
        ], **kwargs)
    
    @callback(
        bc.ChildOutput('more_content', 'children'),
        bc.ChildInput('more_button', 'n_clicks'),
        State('input_combiner', 'data-value'),
        prevent_initial_call=True
    )
    def infinite_hello_world(n_clicks, value):
        return html.Div(InfiniteHelloWorld(initial_text=value), style={'borderLeft': '1px solid black', 'paddingLeft': '10px'})
    
    @callback(
        bc.ChildOutput('text', 'children'),
        bc.ChildInput('interval', 'n_intervals'),
        State('input_combiner', 'data-value'),
        bc.ChildState('text', 'value'),
        prevent_initial_call=True
    )
    def update_text(n_intervals, new_value, current_value):
        if new_value != current_value:
            return new_value
        return no_update

class ExpandContract(html.Div, bc):

    def __init__(self):
        button_child_id = self.child_id('button')
        content_child_id = self.child_id('content')
        super().__init__([
            html.Button('Expand', id=self.child_id('button'), style={'cursor': 'pointer'}),
            InfiniteHelloWorld(id=self.child_id('content'), style={'display': 'none'}),
        ])

    @callback(
        bc.ChildOutput('content', 'style'),
        bc.ChildOutput('button', 'children'),
        bc.ChildInput('button', 'n_clicks'),
        prevent_initial_call=True
    )
    def toggle_content(n_clicks):
        if n_clicks % 2 == 0:
            return ({'display': 'none'}, 'Expand')
        else:
            return ({'borderLeft': '1px solid black', 'paddingLeft': '10px'}, 'Contract')

if __name__ == '__main__':
    dash_app = Dash(__name__)
    dash_app.layout = [
        # html.Button('Hello World', value='hellovalue'),
        InputCombiner(id='input_combiner'),
        ExpandContract()
    ]
    dash_app.run_server(debug=True)
