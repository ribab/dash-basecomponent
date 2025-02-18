

# Motivation here is to use https://dash.plotly.com/all-in-one-components

import uuid, inspect, os
from dash import Output, Input, State, MATCH, ALL, ALLSMALLER


class BaseComponent:

    __id_counter = 0

    def child_id(self, child_name):
        return BaseComponent.__child_id(child_name, parent=self)

    @staticmethod
    def ChildOutput(child_name, attribute, **kwargs):
        child_output = Output(BaseComponent.__child_id(child_name), attribute, **kwargs)
        return child_output

    @staticmethod
    def ChildInput(child_name, attribute, all=False, match=False, allsmaller=False, **kwargs):
        assert sum([all, match, allsmaller]) <= 1, "Only one of all, match, or allsmaller can be True"
        parent = None
        if all:
            parent = ALL
        elif match:
            parent = MATCH
        elif allsmaller:
            parent = ALLSMALLER
        child_input = Input(BaseComponent.__child_id(child_name, parent=parent), attribute, **kwargs)
        return child_input

    @staticmethod
    def ChildState(child_name, attribute, all=False, match=False, allsmaller=False, **kwargs):
        assert sum([all, match, allsmaller]) <= 1, "Only one of all, match, or allsmaller can be True"
        parent = None
        if all:
            parent = ALL
        elif match:
            parent = MATCH
        elif allsmaller:
            parent = ALLSMALLER
        return State(BaseComponent.__child_id(child_name, parent=parent), attribute, **kwargs)
    
    def Output(self, attribute, **kwargs):
        return Output(self.id, attribute, **kwargs)

    def Input(self, attribute, **kwargs):
        return Input(self.id, attribute, **kwargs)
    
    def State(self, attribute, **kwargs):
        return State(self.id, attribute, **kwargs)


    # ===============
    # Private Methods
    # ===============

    @classmethod
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__called_from = BaseComponent.__called_from()
        if 'id' in kwargs:
            instance.id = kwargs['id']
        else:
            instance.id = str(BaseComponent.__id_counter)
            BaseComponent.__id_counter += 1
        return instance
    
    @staticmethod
    def __called_from():
        stack = inspect.stack()
        this_file = stack[0].filename
        i = 1
        while i < len(stack) - 1 and stack[i].filename == this_file:
            i += 1
        called_from = os.path.abspath(stack[i].filename).replace('.', '_')
        return called_from
    
    @staticmethod
    def __child_id(child_name, parent=None):
        called_from = BaseComponent.__called_from()
        if parent == MATCH or parent == ALL or parent == ALLSMALLER:
            parent_id = parent
        elif parent is None:
            parent_id = MATCH
        else:
            parent_id = str(parent.id)
        return {
            'path': str(called_from),
            'child': str(child_name),
            'id': parent_id,
        }
