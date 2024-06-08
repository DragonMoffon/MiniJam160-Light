from arcade import get_window, TextureAtlas
import arcade.gl as gl


class Particles:
    """
    Batched Gpu particles
    """

    def __init__(self):
        self._atlas: TextureAtlas = None
        self._max_particles: int = 0
        
        self._position_source: gl.Buffer = None
        self._position_target: gl.Buffer = None

        self._texture_source: gl.Buffer = None
        self._texture_target: gl.Buffer = None

        self._size_source: gl.Buffer = None
        self._size_target: gl.Buffer = None

        self._transform_shader: gl.Program = None
        self._render_shader: gl.Program = None

        self._vao_source: gl.Geometry = None
        self._vao_target: gl.Geometry = None
