#!/usr/bin/env python3
import os, sys
from dash import Dash, html, dcc, Input, Output, State, no_update, callback, ctx
from dash_basecomponent import BaseComponent as bc

class Square(html.Div, bc):
    def __init__(self, x, y):
        super().__init__(
            [
                html.Div(
                    id=self.child_id('square'),
                    style={
                        'width': '100%', 'height': '100%', 'display': 'flex',
                        'justify-content': 'center', 'align-items': 'center',
                        'font-size': '100px', 'cursor': 'pointer', 'text-align': 'center'
                    }
                ),
                dcc.Store(id=self.child_id('x_position'), data=x),
                dcc.Store(id=self.child_id('y_position'), data=y),
            ],
            style={
                'width': '200px', 'height': '200px',
                'border-right': '1px solid black' if x != 2 else 'none',
                'border-bottom': '1px solid black' if y != 2 else 'none'
            },
        )
    
        @callback(
            Output('game_state', 'data', allow_duplicate=True),
            Input(self.child_id('square'), 'n_clicks'),
            [
                State('game_state', 'data'),
                State(self.child_id('x_position'), 'data'),
                State(self.child_id('y_position'), 'data'),
            ],
            prevent_initial_call=True
        )
        def push_button(n_clicks, game_state, x, y):
            if not game_state or not n_clicks or game_state[x][y]:
                return no_update
            num_x = sum(row.count('X') for row in game_state)
            num_o = sum(row.count('O') for row in game_state)
            if num_x - num_o == 1:
                game_state[x][y] = 'O'
            else:
                game_state[x][y] = 'X'
            return game_state

        @callback(
            Output(self.child_id('square'), 'children', allow_duplicate=True),
            Input('game_state', 'data'),
            State(self.child_id('x_position'), 'data'),
            State(self.child_id('y_position'), 'data'),
            prevent_initial_call=True
        )
        def update_mark(game_state, x, y):
            if not game_state:
                return no_update
            print('update_mark')
            if game_state[x][y] == 'X':
                return 'X'
            if game_state[x][y] == 'O':
                return 'O'
            return ' '
            

class Game(html.Div, bc):
    def __init__(self):
        # create tic tac toe game board layout in children of this component __init__, with all styles to make it look like a game board for tic tac toe
        super().__init__([
            html.Div(
                [
                    html.Div(
                        [
                            Square(x, y)
                            for y in range(3)
                        ],
                        style={'width': '200px', 'height': '600px', 'display': 'flex', 'flex-direction': 'column'}
                    )
                    for x in range(3)
                ],
                style={'width': '600px', 'height': '600px', 'display': 'flex', 'flex-direction': 'row'},
                id=self.child_id('board')
            ),
            dcc.Store(id='game_state', data=[['' for _ in range(3)] for _ in range(3)])
        ])
    
    @callback(
        bc.ChildOutput('board', 'children'),
        Input('game_state', 'data'),
    )
    def check_if_win(game_state):
        if not game_state:
            return no_update
        print('check if win')
        for row in game_state:
            if row.count('X') == 3:
                return 'X wins'
            if row.count('O') == 3:
                return 'O wins'
        for col in zip(*game_state):
            if col.count('X') == 3:
                return 'X wins'
            if col.count('O') == 3:
                return 'O wins'
        # also check diagonals
        if game_state[0][0] == 'X' and game_state[1][1] == 'X' and game_state[2][2] == 'X':
            return 'X wins'
        if game_state[0][0] == 'O' and game_state[1][1] == 'O' and game_state[2][2] == 'O':
            return 'O wins'
        if game_state[0][2] == 'X' and game_state[1][1] == 'X' and game_state[2][0] == 'X':
            return 'X wins'
        if game_state[0][2] == 'O' and game_state[1][1] == 'O' and game_state[2][0] == 'O':
            return 'O wins'
        return no_update

dash = Dash(__name__)
dash.layout = Game()

# start dash app
dash.run_server(debug=True)