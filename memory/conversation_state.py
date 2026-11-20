class ConversationState:

    def __init__(self):

        self.current_game = None

    def set_game(
        self,
        game_id: str,
    ):
        self.current_game = game_id

    def get_game(self):

        return self.current_game


conversation_state = ConversationState()