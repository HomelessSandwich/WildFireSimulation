import pyglet as glet

class Window(pyglet.window.Window):
	
	def __init__(self):
		super(Window, self)._init_()


if __name__ == '__main__':
	window = Window()
	glet.app.run()