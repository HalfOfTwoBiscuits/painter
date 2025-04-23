from abc import ABC

class InputHandler(ABC):
    '''A base class for input handlers that specifies the
    process_input() method to respond to key presses.'''
    _ACTIONS = {}

    @classmethod
    def process_input(cls, key):
        '''Use the _ACTIONS attribute to determine what to
        do in response to a key being pressed.
        
        If the key code is a key in the _ACTIONS dictionary,
        the first element of the corresponding tuple is the
        string name of a method to call.
        All other elements in that tuple will be passed as arguments.
        
        The return value of that method will be returned.'''
        action = cls._ACTIONS.get(key)
        if action is not None:
            method_to_call = getattr(cls,action[0])
            arguments = action[1:]
            state_change = method_to_call(*arguments)
            return state_change