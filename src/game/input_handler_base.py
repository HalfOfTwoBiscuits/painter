from abc import ABC

class InputHandler(ABC):
    '''A base class for input handlers that specifies the
    process_input() method to respond to key presses.'''

    # Constant response to keys being pressed
    _ACTIONS = {}
    # If not None, this variable value will be used instead
    _variable_actions = None

    @staticmethod
    def process_input(self, key):
        '''Use the actions dictionary to determine
        what to do in response to a key being pressed.
        
        If the key code is a key in the dictionary,
        the first element of the corresponding tuple is the
        string name of a method to call.
        All other elements in that tuple will be passed as arguments.
        
        The return value of that method, if any, is a string
        identifier for a new state. Return it to the main loop.
        
        For some children an instance is created and for others the class is used,
        so this is a staticmethod and self is passed in manually in the main loop.'''

        actions = self._variable_actions or self._ACTIONS
        a = actions.get(key)
        if a is not None:
            method_name = a[0]
            method_to_call = getattr(self, method_name)
            arguments = a[1:]
            state_change = method_to_call(*arguments)
            return state_change