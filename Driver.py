from Screen import Screen
import ctypes
from sdl2 import *
import imgui
import OpenGL.GL as gl
from imgui.integrations.sdl2 import SDL2Renderer
import os
from glob import glob

class Driver:
    def __init__(self):
        self.running = True
        self.screen = Screen("screen.json")
        self.mouse_clicked = False # becomes True for only one frame when clicked

    def Initialize(self):
        # Create ImGUI Context
        imgui.create_context()
        self.io = imgui.get_io()

        if SDL_Init(SDL_INIT_EVERYTHING) < 0:
            print("SDL could not be initialized: " + SDL_GetError())
            return False
        
        # Set OpenGL Attributes
        SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1)
        SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24)
        SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8)
        SDL_GL_SetAttribute(SDL_GL_ACCELERATED_VISUAL, 1)
        SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 1)
        SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 16)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_FLAGS, SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 4)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 1)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
        
        # SDL Hints
        SDL_SetHint(SDL_HINT_VIDEO_HIGHDPI_DISABLED, b"1")
        
        # Create Window
        self.window = SDL_CreateWindow(b"AutoMiner - anthonyafgx studios",
                                        SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                                        512, 256,
                                        SDL_WINDOW_OPENGL)

        if self.window is None:
            print("Window could not be created: " + SDL_GetError())
            return False

        # Create OpenGL Context
        self.glContext = SDL_GL_CreateContext(self.window)
        if self.glContext is None:
            print("GL Context could not be created: " + SDL_GetError())
            return False
        
        SDL_GL_MakeCurrent(self.window, self.glContext)
        if SDL_GL_SetSwapInterval(1) < 0:
            print("Unable to set VSync: " + SDL_GetError())
            return False
        
        # Renderer
        self.renderer = SDL2Renderer(self.window)
        
        # ImGui Font
        self.io.fonts.clear()
        
        # global font scaling
        self.io.font_global_scale = 1. / self._GetFontScalingFactor()
        
        # global font size
        font_size = 16

        # font directory (list of path to each font)
        fonts_dir = glob(os.path.join(
                            os.path.dirname(__file__),
                            'assets', 'fonts', "*.ttf"
            )
        )

        # dictionary of font objects in the fonts directory
        self.fonts = {
            os.path.split(font_path)[-1]: self.io.fonts.add_font_from_file_ttf(
                font_path,
                font_size * self._GetFontScalingFactor(),
                self.io.fonts.get_glyph_ranges_latin()
            )
            for font_path in fonts_dir
        }

        self.renderer.refresh_font_texture()

        return True

    def RunLoop(self):
        while self.running:
            self.ProcessInput()
            self.Update()
            self.GenerateOutput()

    def ProcessInput(self):
        # Handle SDL Events
        self.mouse_clicked = False
        event = SDL_Event()
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                self.running = False
                break
            if event.type == SDL_MOUSEBUTTONDOWN:
                self.mouse_clicked = True
            self.renderer.process_event(event)
        
        # Handle Inputs
        self.renderer.process_inputs()

    def Update(self):
        pass

    def GenerateOutput(self):
        # Draw GUI
        imgui.new_frame()

        with imgui.font(self.fonts['RobotoBold.ttf']):
        # gui function call
            self._imShowFrame()

        # render
        gl.glClearColor(1, 1, 1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        self.renderer.render(imgui.get_draw_data())
        SDL_GL_SwapWindow(self.window)

    def Shutdown(self):
        self.renderer.shutdown()
        SDL_GL_DeleteContext(self.glContext)
        SDL_DestroyWindow(self.window)
        SDL_Quit()

    # Imgui show widgets
    def _imShowFrame(self):
        # Global Styling
        style = imgui.get_style()
        style.colors[imgui.COLOR_BUTTON] = (0.949, 0.584, 0.266, 1)
        style.colors[imgui.COLOR_BUTTON_ACTIVE] = (0.701, 0.431, 0.196, 1)
        style.colors[imgui.COLOR_BUTTON_HOVERED] = (1, 0.682, 0.431, 1)

        # Window Styling
        imgui.set_next_window_size(self.io.display_size.x, self.io.display_size.y)
        imgui.set_next_window_position(0,0)
        flags = imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_TITLE_BAR
        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
        imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, 0.054, 0.450, 0.411)

        # Layout
        imgui.begin("Buttons", True, flags)
        imgui.columns(3)
        imgui.button("START MINING", 120, 40)
        imgui.next_column()
        imgui.button("STOP MINING", 120, 40)
        imgui.end()

        # Window Styling Pop
        imgui.pop_style_var(1) # parameter = number of pops
        imgui.pop_style_color(1)

    def _GetFontScalingFactor(self):
        window_width = self.io.display_size.x
        window_height = self.io.display_size.y
        framebuf_width = c_int()
        framebuf_height = c_int()
        SDL_GL_GetDrawableSize(self.window, ctypes.byref(framebuf_width), ctypes.byref(framebuf_height))

        return max(float(framebuf_width.value) / window_width, float(framebuf_height.value) / window_height)