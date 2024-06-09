from arcade import get_window, ArcadeContext
import arcade.gl as gl

from mj160.data import load_shader
from mj160.util import CONFIG
from mj160.util.upscale_fbo import UpscaleFBO
from mj160.states import LightState


class LightManager:
    """
    Uses the LightState object to run a post-processing layer
    """

    def __init__(self):
        self.ctx: ArcadeContext = get_window().ctx
        self.upscale: UpscaleFBO = get_window().upscale_renderer

        self.post_process_prog: gl.Program = self.ctx.program(
            vertex_shader=load_shader("lighting_vs"),
            fragment_shader=load_shader("lighting_fs")
        )
        self.display_prog: gl.Program = self.ctx.utility_textured_quad_program

        self.render_target: gl.framebuffer = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture(size=CONFIG['win_resolution'], filter=(gl.NEAREST, gl.NEAREST), wrap_x=gl.CLAMP_TO_BORDER, wrap_y=gl.CLAMP_TO_BORDER)]
        )

        self.render_geo: gl.Geometry = gl.geometry.quad_2d_fs()
        self.display_geo: gl.Geometry = gl.geometry.quad_2d_fs()

    def draw(self):
        LightState.bufferise()

        prev_fbo = self.ctx.active_framebuffer

        self.render_target.use()
        self.render_target.clear()
        prev_fbo.color_attachments[0].use()

        b_l = self.upscale.into_camera.bottom_left
        w, h = self.upscale.into_camera.width, self.upscale.into_camera.height
        self.post_process_prog['view_area'] = b_l.x, b_l.y, w, h
        LightState.light_buffer.bind_to_storage_buffer()
        self.render_geo.render(self.post_process_prog)

        prev_fbo.use()
        self.render_target.color_attachments[0].use()
        self.display_geo.render(self.display_prog)

