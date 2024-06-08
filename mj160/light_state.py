from typing import NamedTuple
from struct import pack

from arcade import get_window, ArcadeContext, Camera2D
import arcade.gl as gl

from mj160.data import load_shader
from mj160.util import CONFIG


class Light(NamedTuple):
    r: float
    g: float
    b: float
    x: float
    y: float
    s: float


class _LightState:
    MAX_LIGHTS: int = 32

    def __init__(self):
        self._is_enabled: bool = False

        self.ctx: ArcadeContext = None

        self._lights: list[Light] = None

        self._light_buffer: gl.Buffer = None

        self.program: gl.Program = None
        self.display_program: gl.Program = None
        self.geo: gl.Geometry = None

        self.render_target: gl.Framebuffer = None

    def enable(self):
        self._is_enabled = True

    def disable(self):
        self._is_enabled = False

    def add_light(self, light: Light):
        if not self.program:
            raise ValueError("adding light before Lights have been initialised")

        if len(self._lights) >= _LightState.MAX_LIGHTS:
            raise ValueError("Tried adding one too many lights")

        self._lights.append(light)
        self.bufferise()
        return len(self._lights) - 1

    def get_light_idx(self, light: Light):
        if not self.program:
            raise ValueError("Tried to get light before before lights have been initialised")

        return self._lights.index(light)

    def get_light(self, idx: int):
        if not self.program:
            raise ValueError("Tried to get light before before lights have been initialised")

        return self._lights[idx]

    def clear_lights(self):
        self._lights = []
        self.bufferise()

    def modify_light(self, old_light: Light, new_light: Light):
        if not self.program:
            raise ValueError("modifying light before Lights have been initialised")

        idx = self._lights.index(old_light)
        self._lights[idx] = new_light
        self._light_buffer = None
        self.bufferise()

    def modify_directly(self, idx: int, new_light: Light):
        if not self.program:
            raise ValueError("modifying light before Lights have been initialised")

        self._lights[idx] = new_light

        self.bufferise()

    def initialise(self):
        self.ctx = get_window().ctx

        self._lights = []  # Just start with the player's light active

        self.program = self.ctx.program(
            vertex_shader=load_shader("lighting_vs"),
            fragment_shader=load_shader("lighting_fs")
        )
        self.display_program = self.ctx.utility_textured_quad_program

        self.geo = gl.geometry.quad_2d_fs()

        self.render_target = self.ctx.framebuffer(
            color_attachments=[
                self.ctx.texture(size=CONFIG['win_resolution'], filter=(gl.NEAREST, gl.NEAREST))
            ]
        )

    def bufferise(self):
        if not self._lights or not self.program:
            return

        def _linearise():
            for light in self._lights:
                yield light.r
                yield light.g
                yield light.b
                yield 1.0  ## Padding
                yield light.x
                yield light.y
                yield light.s
                yield 0.0  ## Padding

        _buffer_size = 4 * (4 + 8 * len(self._lights))
        if self._light_buffer is None:
            self._light_buffer = self.ctx.buffer(reserve=_buffer_size)
        elif self._light_buffer.size != _buffer_size:
            self._light_buffer.orphan(size=_buffer_size)

        byte_data = pack(f'i i i i {len(self._lights) * 8}f', len(self._lights), 0, 0, 0, *_linearise())
        self._light_buffer.write(byte_data)

    def render(self, source: gl.Texture2D, camera: Camera2D):
        if self.program is None or not self._is_enabled:
            return

        with self.render_target.activate():
            bl = camera.bottom_left

            self.program['view_area'] = bl.x, bl.y, camera.width, camera.height

            source.use()
            self._light_buffer.bind_to_storage_buffer()
            self.geo.render(self.program)


LightState = _LightState()
