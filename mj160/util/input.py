from arcade.experimental.input import InputManager, Keys, ControllerAxes, ControllerButtons, MouseAxes, MouseButtons


def setup_input(manager: InputManager):
    manager.new_action("gui-back")
    manager.add_action_input("gui-back", Keys.ESCAPE)
    manager.add_action_input("gui-back", Keys.BACKSPACE)
    manager.add_action_input("gui-back", ControllerButtons.RIGHT_FACE)

    manager.new_action("gui-select")
    manager.add_action_input("gui-select", Keys.ENTER)
    manager.add_action_input("gui-select", ControllerButtons.BOTTOM_FACE)

    manager.new_action("gui-left_click")
    manager.add_action_input("gui-left_click", MouseButtons.LEFT)
    manager.add_action_input("gui-left_click", ControllerButtons.LEFT_STICK)

    manager.new_action("gui-right_click")
    manager.add_action_input("gui-right_click", MouseButtons.RIGHT)
    manager.add_action_input("gui-right_click", ControllerButtons.RIGHT_STICK)

    manager.new_action("gui-down")
    manager.add_action_input("gui-down", Keys.DOWN)
    manager.add_action_input("gui-down", Keys.S)
    manager.add_action_input("gui-down", ControllerButtons.DPAD_DOWN)

    manager.new_action("gui-up")
    manager.add_action_input("gui-up", Keys.UP)
    manager.add_action_input("gui-up", Keys.W)
    manager.add_action_input("gui-up", ControllerButtons.DPAD_UP)

    manager.new_action("gui-left")
    manager.add_action_input("gui-left", Keys.LEFT)
    manager.add_action_input("gui-left", Keys.A)
    manager.add_action_input("gui-left", ControllerButtons.DPAD_LEFT)

    manager.new_action("gui-right")
    manager.add_action_input("gui-right", Keys.RIGHT)
    manager.add_action_input("gui-right", Keys.D)
    manager.add_action_input("gui-right", ControllerButtons.DPAD_RIGHT)

    manager.new_axis("player-move_horizontal")
    manager.add_axis_input("player-move_horizontal", Keys.A, -1.0)
    manager.add_axis_input("player-move_horizontal", Keys.D, 1.0)
    manager.add_axis_input("player-move_horizontal", ControllerAxes.LEFT_STICK_X)
    manager.new_axis("player-move_vertical")
    manager.add_axis_input("player-move_vertical", Keys.W, 1.0)
    manager.add_axis_input("player-move_vertical", Keys.S, -1.0)
    manager.add_axis_input("player-move_vertical", ControllerAxes.LEFT_STICK_Y)
    manager.new_action("player-primary")
    manager.add_action_input("player-primary", MouseButtons.LEFT)
    manager.add_action_input("player-primary", ControllerButtons.LEFT_SHOULDER)
    manager.new_action("player-secondary")
    manager.add_action_input("player-secondary", MouseButtons.RIGHT)
    manager.add_action_input("player-secondary", ControllerButtons.RIGHT_SHOULDER)

    manager.new_axis("player-look_horizontal")
    manager.add_axis_input("player-look_horizontal", MouseAxes.X)
    manager.add_axis_input("player-look_horizontal", ControllerAxes.RIGHT_STICK_X)

    manager.new_axis("player-look_vertical")
    manager.add_axis_input("player-look_vertical", MouseAxes.Y)
    manager.add_axis_input("player-look_vertical", ControllerAxes.RIGHT_STICK_Y)
