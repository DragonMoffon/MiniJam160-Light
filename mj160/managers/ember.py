from mj160.states import EmberState


class EmberManager:

    def update(self):
        for brazier in EmberState.braziers:
            brazier.update()