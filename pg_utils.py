import pygame as pg

class camera:
	# Create a camera at (x, y) in world coords.
	# Camera will blit to surface s whenever camera.render() is called.
	def __init__(self, x, y, s):
		self.x = x
		self.y = y
		self.s = s
	
	# Blit the surface "surf" at global coords "pos" to the surface specified in the constructor.
	def render(self, surf, pos):
		self.s.blit(surf, (pos[0] - (self.x - self.s.get_width()/2), pos[1] - (self.y - self.s.get_height()/2)))
	
	# Modify camera's position
	def move(self, x, y):
		self.x += x
		self.y += y

# Class for collecting sprites together into layers.
class world:
	def __init__(self):
		self.sprites = []
		self.l_dict = {}
		self.s_dict = {}
		self.spr_group = None
	
	# Call update on all sprites.
	# Does nothing on sprites that aren't classes derived from pg.sprite.Sprite
	def update(self):
		for l in self.sprites:
			for s in l:
				s.update()
	
	# Render all groups in order, from the perspective of cam.
	def render(self, cam):
		for l in self.sprites:
			for s in l:
				cam.render(s.image, (s.rect.left, s.rect.top))
	
	# Creates a new group
	def add_layer(self, layer_name):
		self.sprites.append([])
		
		self.l_dict[layer_name] = len(self.sprites) - 1
		self.s_dict[layer_name] = {}
	
	# Removes a layer
	def remove_layer(self, layer_name):
		del self.sprites[self.l_dict[name]]
		del self.l_dict[layer_name]
		del self.s_dict[layer_name]
	
	# Creates a sprite from the passed surface "img" and adds it to the named layer.
	# The surface is copied and can be modified later.
	def add_sprite_from_surface(self, layer_name, sprite_name, img, x=0, y=0):
		s = pg.sprite.Sprite()
		s.image = img.copy()
		s.rect = img.get_rect(topleft=(x, y))
		
		self.sprites[self.l_dict[layer_name]].append(s)
		self.s_dict[layer_name][sprite_name] = len(self.sprites[self.l_dict[layer_name]])-1

	def add_sprite_group(self, group):
		self.spr_group = group
		
	# Adds an existing sprite.
	# This allows the addition of sprites that are actually derived from pg.sprite.Sprite
	# The sprite is NOT copied!
	def add_sprite(self, layer_name, sprite_name, s, x=0, y=0):
		s.rect = s.image.get_rect(center=(x, y))
		self.sprites[self.l_dict[layer_name]].append(s)
		self.s_dict[layer_name][sprite_name] = len(self.sprites[self.l_dict[layer_name]])-1
	
	# Deletes a sprite from a layer
	def remove_sprite(self, layer_name, sprite_name):
		del self.sprites[self.l_dict[layer_name]][self.s_dict[layer_name][sprite_name]]
		del self.s_dict[layer_name][sprite_name]