# The player action is processed correctly.
OK = 200

# The player action is rejected for one of following reason:
#   missing argument: something important like token or id is not presented
#   player forbidden: it is not your turn now
#   incorrect interface: you could not perform such an action 
#   wrong argument: something wrong like improper cards or targets is given
# The reason would also be returned.
BAD_REQUEST = 400
BR_MISSING_ARG = 'missing argument: %s'
BR_PLAYER_FORBID = 'player forbidden'
BR_INCORRECT_INTERFACE = 'incorrect interface'
BR_WRONG_ARG = 'wrong argument: %s'
