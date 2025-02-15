#!/usr/bin/env python3
import os, sys, random
from dash import Dash, html, dcc, no_update, callback, Output, Input
from dash_extensions import EventListener  # Import EventListener from dash-extensions
from dash_basecomponent import BaseComponent as bc

class SnakeGameBoard(html.Div, bc):

    # Constants for the board and cells.
    BOARD_WIDTH = 20    # number of cells horizontally
    BOARD_HEIGHT = 20   # number of cells vertically
    CELL_SIZE = 20      # size in pixels for each cell
    INTIIAL_DIRECTION = "RIGHT"

    def __init__(self):
        
        mid_x = self.BOARD_WIDTH // 2
        mid_y = self.BOARD_HEIGHT // 2
        snake = [
            [mid_x, mid_y],
            [mid_x - 1, mid_y],
            [mid_x - 2, mid_y]
        ]
        food = self.generate_food(snake)
        initial_game_state = {"snake": snake, "food": food, "game_over": False}
        super().__init__([
            html.Div(
                id=self.child_id("board"),
                style={
                    'width': f'{self.BOARD_WIDTH * self.CELL_SIZE + 2}px',
                    'border': '2px solid black',
                    'margin': 'auto'
                }
            ),
            # Use EventListener to capture keydown events. Note: autoFocus is removed.
            EventListener(
                id=self.child_id("key-event"),
                events=[{"event": "keydown", "props": ["key"]}],
                logging=True
            ),
            dcc.Interval(id=self.child_id("interval"), interval=150, n_intervals=0),
            dcc.Store(id=self.child_id("game_state"), data=initial_game_state),
            dcc.Store(id=self.child_id("direction_store"), data=self.INTIIAL_DIRECTION)
        ])

    @classmethod
    def generate_food(cls, snake):
        """Return a random cell coordinate [x, y] that is not occupied by the snake."""
        # first check if there are any empty cells
        if all([x, y] in snake for x in range(SnakeGameBoard.BOARD_WIDTH) for y in range(cls.BOARD_HEIGHT)):
            return None
        while True:
            food = [random.randint(0, SnakeGameBoard.BOARD_WIDTH - 1), random.randint(0, cls.BOARD_HEIGHT - 1)]
            if food not in snake:
                return food

    @callback(
        bc.ChildOutput('game_state', 'data'),
        bc.ChildOutput('direction_store', 'data'),
        bc.ChildOutput('key-event', 'event'),
        bc.ChildInput('interval', 'n_intervals'),
        bc.ChildState('key-event', 'event'),
        bc.ChildState('game_state', 'data'),
        bc.ChildState('direction_store', 'data'),
        prevent_initial_call=True
    )
    def update_game(n_intervals, key_event, game_state, direction):            
        if not game_state or game_state.get("game_over"):
            return no_update, no_update, no_update

        # Update direction if a key event is present.
        key = key_event['key'] if key_event and 'key' in key_event else None

        if key == 'ArrowUp' and direction != "DOWN":
            new_direction = "UP"
        elif key == 'ArrowDown' and direction != "UP":
            new_direction = "DOWN"
        elif key == 'ArrowLeft' and direction != "RIGHT":
            new_direction = "LEFT"
        elif key == 'ArrowRight' and direction != "LEFT":
            new_direction = "RIGHT"
        else:
            new_direction = no_update
        
        snake = game_state["snake"]
        head = snake[0].copy()

        if new_direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
            direction = new_direction
        
        if direction == "UP":
            head[1] -= 1
        elif direction == "DOWN":
            head[1] += 1
        elif direction == "LEFT":
            head[0] -= 1
        elif direction == "RIGHT":
            head[0] += 1
        
        # Check for collisions with walls or self.
        if head[0] < 0 or head[0] >= SnakeGameBoard.BOARD_WIDTH or head[1] < 0 or head[1] >= SnakeGameBoard.BOARD_HEIGHT or head in snake:
            game_state["game_over"] = True
            return game_state, new_direction, no_update
        
        snake.insert(0, head)
        if head == game_state["food"]:
            game_state["food"] = SnakeGameBoard.generate_food(snake)
        else:
            snake.pop()
        game_state["snake"] = snake
        return game_state, new_direction, no_update
    
    @callback(
        bc.ChildOutput('board', 'children'),
        bc.ChildInput('game_state', 'data'),
        prevent_initial_call=True
    )
    def update_board(game_state):
        if not game_state:
            return no_update
        snake = game_state["snake"]
        food = game_state["food"]
        game_over = game_state.get("game_over", False)
        cells = []
        for y in range(SnakeGameBoard.BOARD_HEIGHT):
            for x in range(SnakeGameBoard.BOARD_WIDTH):
                cell_color = "white"
                if [x, y] in snake:
                    cell_color = "green"
                if [x, y] == food:
                    cell_color = "red"
                cell_style = {
                    'width': f'{SnakeGameBoard.CELL_SIZE}px',
                    'height': f'{SnakeGameBoard.CELL_SIZE}px',
                    'border': '1px solid #ddd',
                    'backgroundColor': cell_color
                }
                cells.append(html.Div(style=cell_style))
        grid_container = html.Div(
            cells,
            style={'display': 'grid', 'gridTemplateColumns': f'repeat({SnakeGameBoard.BOARD_WIDTH}, {SnakeGameBoard.CELL_SIZE}px)'}
        )
        if game_over:
            overlay = html.Div(
                "Game Over",
                style={
                    'position': 'absolute',
                    'top': '50%',
                    'left': '50%',
                    'transform': 'translate(-50%, -50%)',
                    'fontSize': '40px',
                    'color': 'red'
                }
            )
            return [grid_container, overlay]
        return grid_container

dash_app = Dash(__name__)
dash_app.layout = [
    html.Div([
        html.H1("Snake Game", style={'textAlign': 'center'}),
    ], style={'display': 'flex', 'justifyContent': 'center'}),
    html.Div(
        SnakeGameBoard(),
        id="game"
    ),
    html.Div([
        html.Button("Reset", id="reset-btn", n_clicks=0, style={'margin': '5px'})
    ], style={'textAlign': 'center', 'marginTop': '20px'}),
]

@callback(
    Output("game", "children"),
    Input("reset-btn", "n_clicks"),
    prevent_initial_call=True
)
def reset_game(n_clicks):
    return SnakeGameBoard()

if __name__ == '__main__':
    dash_app.run_server(debug=True)
