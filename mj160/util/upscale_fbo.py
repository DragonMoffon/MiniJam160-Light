from arcade import get_window, ArcadeContext, camera, LBWH
import arcade.gl as gl

from mj160.util import CONFIG
from mj160.light_state import LightState


class UpscaleFBO:

    def __init__(self):
        win = get_window()
        ctx = win.ctx
        self._ctx: ArcadeContext = ctx

        wr, hr = CONFIG['win_resolution']
        ws, hs = win.size

        ratio = min(int(ws / wr), int(hs / hr))

        wa, ha = wr * ratio, hr * ratio

        wp, hp = (ws - wa) / 2, (hs - ha) / 2

        self._fbo: gl.Framebuffer = ctx.framebuffer(
            color_attachments=[
                ctx.texture(
                    size=(wr, hr),
                    filter=(gl.NEAREST, gl.NEAREST),
                    wrap_x=gl.CLAMP_TO_BORDER,
                    wrap_y=gl.CLAMP_TO_BORDER
                )
            ],
            depth_attachment=ctx.depth_texture(
                size=(wr, hr)
            )
        )
        self._screen: gl.Framebuffer = ctx.screen

        self._geo = gl.geometry.quad_2d_fs()
        self._prog = ctx.utility_textured_quad_program

        self.display_camera: camera.Camera2D = camera.Camera2D(viewport=LBWH(wp, hp, wa, ha), position=(0.0, 0.0))
        self.into_camera: camera.Camera2D = camera.Camera2D(viewport=LBWH(0, 0, wr, hr), position=(0.0, 0.0))

    def use(self):
        self._fbo.use()
        self.into_camera.use()

    def clear(self):
        self._fbo.clear(color=(0, 0, 0, 255))

    def display(self):
        self._screen.use()
        self._screen.clear()

        self.display_camera.use()

        LightState.render(self._fbo.color_attachments[0], self.into_camera)
        LightState.display()

        self._fbo.color_attachments[0].use()
        self._geo.render(self._prog)

        self._fbo.use()
        self._fbo.clear()

        self.into_camera.use()
