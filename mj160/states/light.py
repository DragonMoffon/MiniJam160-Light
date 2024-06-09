from arcade import get_window, ArcadeContext
import arcade.gl as gl
from struct import pack

class Light:

    def __init__(self, r, g, b, x, y, s):
        self.r: float = r
        self.g: float = g
        self.b: float = b
        self.x: float = x
        self.y: float = y
        self.s: float = s


class _LightState:
    MAX_LIGHTS: int = 32

    def __init__(self):
        self.lights: list[Light] = []
        self.light_buffer: gl.Buffer = None

    def reset(self):
        self.lights: list[Light] = []
        self.light_buffer: gl.Buffer = None

    def add_light(self, light: Light):
        if len(self.lights) >= _LightState.MAX_LIGHTS:
            raise ValueError("trying to add too many lights")

        self.lights.append(light)

    def remove_lights(self, light: Light):
        self.lights.remove(light)

    def bufferise(self):
        def _linearise():
            for light in self.lights:
                yield light.r
                yield light.g
                yield light.b
                yield 1.0  # Padding
                yield light.x
                yield light.y
                yield light.s
                yield 0.0  # Padding

        _buffer_size = 4 * (4 + 8 * len(self.lights))
        if self.light_buffer is None:
            self.light_buffer = get_window().ctx.buffer(reserve=_buffer_size)
        elif self.light_buffer.size != _buffer_size:
            self.light_buffer.orphan(_buffer_size)

        byte_data = pack(f'i i i i {len(self.lights) * 8}f', len(self.lights), 0, 0, 0, *_linearise())
        self.light_buffer.write(byte_data)


LightState = _LightState()