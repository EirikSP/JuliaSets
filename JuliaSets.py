import moderngl_window as mglw
from moderngl_window import geometry
from numpy import pi
import imgui
import moderngl_window.integrations.imgui as img


class App(mglw.WindowConfig):
    window_size = 1600, 900
    resource_dir = "JuliaSets"
    vsync = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quad = geometry.quad_fs()

        self.cR = 0.0
        self.cI = 0.0
        self.zoom = 5.0
        self.offsetX = 0.0
        self.offsetY = 0.0

        imgui.create_context()
        self.imgui = img.ModernglWindowRenderer(self.wnd)

        self.prog = self.load_program(vertex_shader='vertex_shader.glsl', fragment_shader='fragment_shader.glsl')

        #self.frame = self.load_program(vertex_shader='diffusion.glsl', varyings=[])

        self.set_uniform('resolution', self.window_size)
        self.set_uniform('pi', pi)
        self.update_uniforms()

    def set_uniform(self, u_name, u_value):
        try:
            self.prog[u_name] = u_value
        except:
            print(f'uniform: {u_name} - not used in shader')

    def update_uniforms(self):
        self.prog['cR'] = self.cR
        self.prog['cI'] = self.cI
        self.prog['zoom'] = self.zoom
        self.prog['offsetX'] = self.offsetX
        self.prog['offsetY'] = self.offsetY


    def render(self, time: float, frame_time: float):
        self.ctx.clear()
        self.set_uniform('time', time)
        self.quad.render(self.prog)
        self.render_ui()

    def render_ui(self):
        imgui.new_frame()

        if imgui.begin("Settings"):
            imgui.push_item_width(imgui.get_window_width()*0.5)

            changed = False
            c, self.cR = imgui.slider_float(
                "Real", self.cR, -2.0, 2.0
            )
            changed = changed or c
            c, self.cI = imgui.slider_float(
                "Imaginary", self.cI, -2.0, 2.0
            )
            changed = changed or c
            c, self.zoom = imgui.slider_float(
                "Zoom", self.zoom, 0.0, 12.0
            )
            changed = changed or c
            c, self.offsetX = imgui.slider_float(
                "Offset X", self.offsetX, -1.5, 1.5
            )
            changed = changed or c
            c, self.offsetY = imgui.slider_float(
                "Offset Y", self.offsetY, -1.5, 1.5
            )
            changed = changed or c
            if changed:
                self.update_uniforms()
            
            
            imgui.pop_item_width()



        imgui.end()

        imgui.render()
        self.imgui.render(imgui.get_draw_data())

    def mouse_position_event(self, x, y, dx, dy):
        self.imgui.mouse_position_event(x, y, dx, dy)

    def mouse_drag_event(self, x, y, dx, dy):
        self.imgui.mouse_drag_event(x, y, dx, dy)

    def mouse_scroll_event(self, x_offset, y_offset):
        self.imgui.mouse_scroll_event(x_offset, y_offset)

    def mouse_press_event(self, x, y, button):
        self.imgui.mouse_press_event(x, y, button)

    def mouse_release_event(self, x: int, y: int, button: int):
        self.imgui.mouse_release_event(x, y, button)


if __name__=='__main__':
    mglw.run_window_config(App)