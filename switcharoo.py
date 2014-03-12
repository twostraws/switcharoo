# Switcharoo
# Copyright (C) 2010 Paul Hudson (http://www.hudzillagames.com)

# Switcharoo is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


from __future__ import division

from gloss import *
import time
import datetime
from random import choice
import pickle

class Switcharoo(GlossGame):
	def preload_content(self):
		self.splash_screen = Texture("content/splash.png")
		
	def draw_loading_screen(self):
		self.splash_screen.draw()
	
	def load_content(self):
		self.splash_screen = None
		
		game.on_mouse_down = self.handle_mouse_down
		game.on_mouse_up = self.handle_mouse_up
		game.on_mouse_motion = self.handle_mouse_motion
		
		self.refresh_selected = False
		
		Color.DARK_BLUE = Color(0, 0.1, 0.6, 1)


		# load the primary word list
		f = open("content/words")
		raw_word_list = f.readlines()
		
		word_list = []

		for line in raw_word_list:
			line = line.strip("\n")
			word_list.append(line)
		
		self.word_list = set(word_list)
		
		
		# load the list of colours
		f = open("content/colours")
		raw_word_list = f.readlines()
		
		self.colour_list = []
		
		for line in raw_word_list:
			line = line.strip("\n")
			self.colour_list.append(line)
		
		
		# finally, load our list of starting and bonus words
		self.starting_words = "late", "time", "line", "dare", "bite", "lace", "sire", "lone", "note", "pure", "hats", "read", "sand", "safe", "sing", "need", "core", "cane", "rags", "near", "will", "bows", "dent", "lots", "sail", "pale", "mock", "mule" 
		self.current_bonus_word = ""
		
		# load high scores, if anything
		self.high_scores = []
		
		if not os.path.exists(".switcharoo_scores"):
			for i in reversed(range(10)):
				score = SwitcharooScore("Hudzilla", 200 + (i * 200))
				self.high_scores.append(score)
				
			with open(".switcharoo_scores", "wb") as scores: 
				 pickle.dump(self.high_scores, scores)
			
		with open(".switcharoo_scores", "rb") as scores: 
			self.high_scores = pickle.load(scores)
		
		# now load all graphics
		self.letter_list = dict([(chr(i), Texture("content/" + chr(i) + ".png")) for i in range(ord('a'), ord('z') + 1)])
		
		self.logo = Texture("content/logo.png")
		self.logo_small = Texture("content/logo_small.png")
		
		self.curtain_left = Texture("content/curtain_left.png")
		self.curtain_right = Texture("content/curtain_right.png")
		self.spotlight = Texture("content/spotlight.png")
		
		self.background = Texture("content/background.jpg")
		self.rings = Texture("content/rings.png")
		self.lensflare = Texture("content/lensflare.png")
		self.timer_bg = Texture("content/timer_bg.png")
		self.score_bg = Texture("content/score_bg.png")
		self.colours_bg = Texture("content/colours_bg.png")
		self.drop_unknown = Texture("content/drop_unknown.png")
		self.drop_good = Texture("content/drop_good.png")
		self.drop_bad = Texture("content/drop_bad.png")
		self.game_over = Texture("content/game_over.png")
		
		self.menu_button = Texture("content/menu.png")
		self.menu_button_down = Texture("content/menu_down.png")
		self.menu_button_position = (747, 695)
		
		self.refresh_letters = Texture("content/refresh_letters.png")
		self.refresh_letters_down = Texture("content/refresh_letters_down.png")
		self.refresh_letters_position = (512 - self.refresh_letters.half_width, 400)
		
		self.down_over_refresh_letters = False
		self.down_over_menu_button = False

		self.sans_font = SpriteFont("content/freesans.ttf", 76)
		self.serif_font = SpriteFont("content/freeserif.ttf", 50)
		self.mono_font = SpriteFont("content/freemonobold.ttf", 36)
		self.high_scores_font = SpriteFont("content/freeserif.ttf", 36)
		
		self.smoke = Texture("content/particle_smoke.png")
		self.particles = []
		
		self.melody_welcome = Texture("content/melody_welcome.png")
		self.melody_important = Texture("content/melody_important.png")
		self.melody_happy = Texture("content/melody_happy.png")
		self.melody_sad = Texture("content/melody_sad.png")
		
		self.bonus_word_box = Texture("content/bonus_word_box.png")
		self.melody_important_small = Texture("content/melody_important_small.png")
		self.melody_happy_small = Texture("content/melody_happy_small.png")
		
		self.menu_main = Texture("content/menu_main.png")
		self.how_to_play = [Texture("content/how_to_play1.png"), Texture("content/how_to_play2.png"), Texture("content/how_to_play3.png"), Texture("content/how_to_play4.png"), Texture("content/how_to_play5.png"), Texture("content/how_to_play6.png"), Texture("content/how_to_play7.png")]
		self.menu_options_anim = 0
		
		self.letter_width = 90
		self.letter_height = 128

		self.bonus_chain = Texture("content/chain.png")
		self.bonus_colour = Texture("content/colour.png")
		self.bonus_word = Texture("content/bonus_word.png")
		self.bonus_q = Texture("content/q_bonus.png")
		self.bonus_text_life = 1500 # make bonus text like "Chain!" appear for this time
		
		self.menu_logo_position = (512, 184)
		self.playing_logo_position = (512, 92)
		
		pygame.mixer.music.load("content/RadioMartini.ogg")
		pygame.mixer.music.play()
		
		self.card_flip_sound = pygame.mixer.Sound("content/card_flip.wav")
		self.card_flip2_sound = pygame.mixer.Sound("content/card_flip2.wav")
		self.wrong_sound = pygame.mixer.Sound("content/wrong.wav")
		self.click_sound = pygame.mixer.Sound("content/mouse_click.wav")
		self.bonus_sound = pygame.mixer.Sound("content/bonus.wav")

		
		self.set_menu_state(MS_MENU)
		self.menu_light_pos = 0
				
	def set_menu_state(self, state):
		self.menu_state = state
		self.menu_anim_pos = 0
		self.menu_options_anim = 0

	def draw(self):
		if self.menu_state is MS_MENU or self.menu_state is MS_HOW_TO_PLAY:
			self.draw_menu()
		if self.menu_state is MS_HIGH_SCORES:
			self.draw_high_scores()
		elif self.menu_state is MS_LOADING_GAME:
			self.draw_loading_game()
		elif self.menu_state is MS_PLAYING:
			self.draw_playing(True)
		elif self.menu_state is MS_UNLOADING_GAME:
			self.draw_unloading_game()
		elif self.menu_state is MS_GAME_OVER_IN:
			self.draw_playing(True)
			glBlendFunc(GL_SRC_ALPHA, GL_ONE)
			self.lensflare.draw((512, 384), origin = None, color = Color(1, 1, 1, 1), scale = self.menu_anim_pos * 3)
			glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		elif self.menu_state is MS_GAME_OVER_SHOWING:
			Gloss.fill(top = Color(1, 1, 1, 1), bottom = Color(1, 1, 1, 1))
			self.game_over.draw((512, 384), origin = None)
		elif self.menu_state is MS_GAME_OVER_OUT:
			self.draw_menu()
			Gloss.fill(top = Color(1, 1, 1, 1 - self.menu_anim_pos), bottom = Color(1, 1, 1, 1 - self.menu_anim_pos))

	def update(self):
		if self.menu_anim_pos < 1:
			self.menu_anim_pos += Gloss.elapsed_seconds
			
			if self.menu_anim_pos >= 1:
				self.menu_anim_pos = 1.0
				
				if self.menu_state is MS_LOADING_GAME:
					self.set_menu_state(MS_PLAYING)
					pygame.mixer.music.load("content/SchemingWeasel.ogg")
					pygame.mixer.music.play()					
				elif self.menu_state is MS_UNLOADING_GAME:
					self.set_menu_state(MS_MENU)
					pygame.mixer.music.load("content/RadioMartini.ogg")
					pygame.mixer.music.play()	
				elif self.menu_state is MS_GAME_OVER_IN:
					self.set_menu_state(MS_GAME_OVER_SHOWING)	
				elif self.menu_state is MS_GAME_OVER_SHOWING:
					self.set_menu_state(MS_GAME_OVER_OUT)
				elif self.menu_state is MS_GAME_OVER_OUT:
					self.set_menu_state(MS_MENU)
		
		if self.menu_state is MS_MENU or self.menu_state is MS_HOW_TO_PLAY:
			self.update_menu()
		elif self.menu_state is MS_PLAYING:
			self.update_playing()		
		
	def handle_mouse_down(self, event):
		if self.menu_state is MS_MENU or self.menu_state is MS_HOW_TO_PLAY:
			self.handle_mouse_down_menu(event)
		elif self.menu_state is MS_HIGH_SCORES:
			self.set_menu_state(MS_MENU)
			self.click_sound.play()
		elif self.menu_state is MS_PLAYING:
			self.handle_mouse_down_playing(event)

	def handle_mouse_down_menu(self, event):
		if self.menu_state is MS_MENU:
			if point_over_rect(event.pos[0], event.pos[1], 263, 408, 267, 50):
				# start a new game
				self.new_game()
				self.set_menu_state(MS_LOADING_GAME)
				pygame.mixer.music.fadeout(750)
				self.click_sound.play()
			elif point_over_rect(event.pos[0], event.pos[1], 263, 472, 267, 50):
				# show high scores
				self.set_menu_state(MS_HIGH_SCORES)
			elif point_over_rect(event.pos[0], event.pos[1], 263, 535, 267, 50):
				# show the instructions
				self.set_menu_state(MS_HOW_TO_PLAY)
				self.click_sound.play()
				self.how_to_play_counter = 0
			elif point_over_rect(event.pos[0], event.pos[1], 263, 612, 267, 50):
				# quit the game
				self.quit()
		else:
			self.menu_options_anim = 0
			self.how_to_play_counter += 1
			self.click_sound.play()
				
			if self.how_to_play_counter is len(self.how_to_play):
				self.set_menu_state(MS_MENU)

	def handle_mouse_down_playing(self, event):
		if self.timer is 0: return
		
		self.selected_letter = None
		self.drop_status = DROP_UNKNOWN
		
		if point_over_rect(event.pos[0], event.pos[1], self.refresh_letters_position[0], self.refresh_letters_position[1], self.refresh_letters.width, self.refresh_letters.height):
			self.down_over_refresh_letters = True
			return
			
		if point_over_rect(event.pos[0], event.pos[1], self.menu_button_position[0], self.menu_button_position[1], self.menu_button.width, self.menu_button.height):
			self.down_over_menu_button = True
			return
		
		for letter in self.letters:
			if point_over_rect(event.pos[0], event.pos[1], letter.position[0], letter.position[1], self.letter_width, self.letter_height):
				self.selected_letter = letter
				self.selected_letter_offset = (event.pos[0] - letter.position[0], event.pos[1] - letter.position[1])
				self.card_flip_sound.play()
				return
		
	def handle_mouse_up(self, event):
		if self.menu_state is MS_MENU:
			self.handle_mouse_up_menu(event)
		elif self.menu_state is MS_PLAYING:
			self.handle_mouse_up_playing(event)
			
	def handle_mouse_up_menu(self, event):
		pass
			
	def handle_mouse_up_playing(self, event):
		if self.timer is 0:
			return
		
		if self.down_over_refresh_letters is True:
			if point_over_rect(event.pos[0], event.pos[1], self.refresh_letters_position[0], self.refresh_letters_position[1], self.refresh_letters.width, self.refresh_letters.height):
				self.generate_starting_word(True)
				self.click_sound.play()

		if self.down_over_menu_button is True:
			if point_over_rect(event.pos[0], event.pos[1], self.menu_button_position[0], self.menu_button_position[1], self.menu_button.width, self.menu_button.height):
				self.set_menu_state(MS_UNLOADING_GAME)
				pygame.mixer.music.fadeout(750)
				self.click_sound.play()
				return
				
		self.down_over_refresh_letters = False
		self.down_over_menu = False
		
		if self.selected_letter is None:
			return
				
		if self.drop_status is DROP_GOOD:
			self.card_flip2_sound.play()
	
			if self.last_drop_slot is self.hover_letter:
				self.drop_count += 1
			else:
				self.drop_count = 0
			
			self.last_drop_slot = self.hover_letter
			
			self.hover_letter.char = self.selected_letter.char

			self.particles.append(self.create_particles(self.hover_letter.position))
			
			self.letters.remove(self.selected_letter)
			self.matched_letter = self.selected_letter
			
			# we draw every tile from the top-left, except when it's just been matched - that draws from the centre for scaling reasons
			# so we need to offset it here!
			self.matched_letter.draw_position = Point.add(self.hover_letter.draw_position, (self.letter_width / 2.0, self.letter_height / 2.0))
			self.last_match_time = Gloss.tick_count
			self.selected_letter = None

			bonus_list = []

			current_word = self.get_current_word()
			
			if current_word in self.used_words:
				self.score += 1
			else:
				# this is the first time we've matched this word - do we need to award a bonus for it?				
				if "q" in current_word:
					# q bonus!
					self.score += 100
					bonus_list.append(self.bonus_q)
					
				if current_word in self.colour_list:
					# colour bonus!
					self.score += 20
					bonus_list.append(self.bonus_colour)
					self.last_colour_match_time = Gloss.tick_count
				
				if current_word.upper() == self.current_bonus_word:
					self.score += 50
					self.timer += 60
					self.last_bonus_word_time = Gloss.tick_count
					bonus_list.append(self.bonus_word)
					self.bonus_sound.play()
			
				if self.drop_count > 2:
					self.score += 10 * (self.drop_count - 3)
					bonus_list.append(self.bonus_chain)
				
				self.used_words.append(current_word)
				
				for letter in current_word:
					self.score += self.get_letter_score(letter)
					
			for i in range(0, len(bonus_list)):					
				bonus = SwitcharooBonus(bonus_list[i], (512, 240 - (i * 50)))
				self.bonus_text.append(bonus)
			
			self.add_letter()
			self.reposition_letters()
		else:
			self.wrong_sound.play()
			self.selected_letter.draw_position = self.selected_letter.position
			self.selected_letter = None
		
	def handle_mouse_motion(self, event):
		if self.menu_state is MS_PLAYING:
			if self.down_over_refresh_letters is True:
				if not point_over_rect(event.pos[0], event.pos[1], self.refresh_letters_position[0], self.refresh_letters_position[1], self.refresh_letters.width, self.refresh_letters.height):
					self.down_over_refresh_letters = False
		
			if self.selected_letter is None:
				return
		
			hover_letter = None
		
			self.selected_letter.draw_position = Point.subtract(event.pos, self.selected_letter_offset)
		
			for i in range(0, len(self.current_word)):
				# are we over any of the current word letters?
				letter = self.current_word[i]
			
				if point_over_rect(event.pos[0], event.pos[1], letter.position[0], letter.position[1], self.letter_width, self.letter_height):
					# yes; store away which letter we're over in case we release the mouse button
					hover_letter = letter
				
					# only check the dictionary if we've changed the letter we're hovering over
					if hover_letter is not self.hover_letter:
						# is this a real word or not?
					
						test_word = self.get_current_letters()
					
						test_word[i] = self.selected_letter.char
						search_word = "".join(test_word)
					
						if search_word == self.get_current_word():
							self.drop_status = DROP_BAD
						else:
							if search_word in self.word_list:
								self.drop_status = DROP_GOOD
							else:
								self.drop_status = DROP_BAD
	
			# cache it for later
			self.hover_letter = hover_letter
		
			if hover_letter is None:
				self.drop_status = DROP_UNKNOWN
			
	def update_menu(self):
		self.menu_options_anim += Gloss.elapsed_seconds * 2
		if self.menu_options_anim > 1.0: self.menu_options_anim = 1.0
		
		self.menu_light_pos += 1.0 * Gloss.elapsed_seconds
		pass
		
	def update_playing(self):
		if self.timer > 0:
			self.timer -= Gloss.elapsed_seconds
			
		if self.timer <= 0:
			self.timer = 0
			
			if self.selected_letter is not None:
				self.selected_letter.draw_position = self.selected_letter.position
				self.selected_letter = None
				
			self.set_menu_state(MS_GAME_OVER_IN)
		
		for bonus in reversed(self.bonus_text):
			bonus.position = (bonus.position[0], bonus.position[1] - 30 * Gloss.elapsed_seconds)
			
			if bonus.created_time + self.bonus_text_life < Gloss.tick_count:
				self.bonus_text.remove(bonus)
				
		if self.last_bonus_word_time != -1:
			# we've matched the bonus word!
			if self.last_bonus_word_time + 2000 < Gloss.tick_count:
				# reset the clock and choose a new word!
				self.current_bonus_word = self.active_word.upper()
		
				while self.current_bonus_word == self.active_word.upper():
					self.current_bonus_word = choice(self.starting_words).upper()
					
				self.last_bonus_word_time = -1


			
	def draw_menu(self):
		self.curtain_left.draw((0, 0))
		self.curtain_right.draw((474, 0))
		self.logo.draw(self.menu_logo_position, origin = None)
		
		# give the spotlights smooth movement
		xdiff = math.sin(self.menu_light_pos + 1) * 350
		ydiff = math.cos(self.menu_light_pos) * 150
		
		glBlendFunc(GL_DST_COLOR, GL_ONE_MINUS_SRC_ALPHA)
		self.spotlight.draw((512 + xdiff, 384 + ydiff), origin = None)
		self.spotlight.draw((512 - xdiff, 384 + ydiff), origin = None)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		if self.menu_state is MS_MENU or self.menu_state is MS_GAME_OVER_OUT:
			self.draw_menu_options(self.menu_main)
			self.draw_melody(self.melody_welcome, (600, 300))
		else:
			self.draw_menu_options(self.how_to_play[self.how_to_play_counter])
			
			if self.how_to_play_counter is 0:
				self.draw_melody(self.melody_happy, (600, 300))
			elif self.how_to_play_counter is 1:
				self.draw_melody(self.melody_welcome, (600, 300))
			elif self.how_to_play_counter is 2:
				self.draw_melody(self.melody_important, (600, 300))
			elif self.how_to_play_counter is 3:
				self.draw_melody(self.melody_welcome, (600, 300))
			elif self.how_to_play_counter is 4:
				self.draw_melody(self.melody_important, (600, 300))
			elif self.how_to_play_counter is 5:
				self.draw_melody(self.melody_sad, (600, 300))
			elif self.how_to_play_counter is 6:
				self.draw_melody(self.melody_happy, (600, 300))
								

	def draw_menu_options(self, menu, color = Color.WHITE):
		scale = Gloss.bounce_out(0, 1, self.menu_options_anim, 10)
		menu.draw((400, 500), color = color, origin = None, scale = scale)
		
	def draw_melody(self, texture, position, color = Color.WHITE):
		texture.draw((position[0] + 5, position[1] + 5), color = Color(0, 0, 0, color.a / 2))
		texture.draw(position, color = color)
	
	def draw_high_scores(self):
		self.curtain_left.draw((0, 0))
		self.curtain_right.draw((474, 0))
		self.logo_small.draw(self.playing_logo_position, origin = None)
		
		for i in range(len(self.high_scores)):
			score = self.high_scores[i]
			self.high_scores_font.draw(score.name, (300, 200 + (i * 50)))
			self.high_scores_font.draw(str(score.score), (700, 200 + (i * 50)))
	
	def draw_loading_game(self):
		self.draw_playing(False)
		
		Gloss.fill(top = Color(0, 0, 0, 1 - self.menu_anim_pos), bottom = Color(0, 0, 0, 1 - self.menu_anim_pos))
		
		left_x = Gloss.smooth_step(0, -self.curtain_left.width, self.menu_anim_pos)
		right_x = Gloss.smooth_step(474, 1024, self.menu_anim_pos)
				
		self.curtain_left.draw((left_x, 0))
		self.curtain_right.draw((right_x, 0))
		
		menu_pos = Point.smooth_step(self.menu_logo_position, self.playing_logo_position, self.menu_anim_pos)
		menu_scale = Gloss.smooth_step(self.logo.width, self.logo_small.width, self.menu_anim_pos)
		menu_scale = (menu_scale / self.logo.width)		
		self.logo.draw(menu_pos, scale = menu_scale, origin = None)
		
		# give the spotlights smooth movement
		xdiff = math.sin(self.menu_light_pos + 1) * 350
		ydiff = math.cos(self.menu_light_pos) * 150
		
		# but we're fading them away, so push them off
		actual_x = Gloss.smooth_step(xdiff, 768, self.menu_anim_pos)
		
		glBlendFunc(GL_DST_COLOR, GL_ONE_MINUS_SRC_ALPHA)
		self.spotlight.draw((512 + actual_x, 384 + ydiff), origin = None)
		self.spotlight.draw((512 - actual_x, 384 + ydiff), origin = None)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		self.menu_options_anim = 1.0 # don't reset the menu position when we're loading the game
		self.draw_menu_options(self.menu_main, color = Color(1, 1, 1, 1 - self.menu_anim_pos * 4))
		self.draw_melody(self.melody_welcome, (600, 300), color = Color(1, 1, 1, 1 - self.menu_anim_pos * 4))
		
	def draw_unloading_game(self):
		self.draw_playing(False)
		
		Gloss.fill(top = Color(0, 0, 0, self.menu_anim_pos), bottom = Color(0, 0, 0, self.menu_anim_pos))
		
		left_x = Gloss.smooth_step(-self.curtain_left.width, 0, self.menu_anim_pos)
		right_x = Gloss.smooth_step(1024, 474, self.menu_anim_pos)
				
		self.curtain_left.draw((left_x, 0))
		self.curtain_right.draw((right_x, 0))
		
		menu_pos = Point.smooth_step(self.playing_logo_position, self.menu_logo_position, self.menu_anim_pos)
		menu_scale = Gloss.smooth_step(self.logo_small.width, self.logo.width, self.menu_anim_pos)
		menu_scale = (menu_scale / self.logo.width)		
		self.logo.draw(menu_pos, scale = menu_scale, origin = None)
		
		# give the spotlights smooth movement
		xdiff = math.sin(self.menu_light_pos + 1) * 350
		ydiff = math.cos(self.menu_light_pos) * 150
		
		# but we're fading them away, so push them off
		actual_x = Gloss.smooth_step(768, xdiff, self.menu_anim_pos)
		
		glBlendFunc(GL_DST_COLOR, GL_ONE_MINUS_SRC_ALPHA)
		self.spotlight.draw((512 + actual_x, 384 + ydiff), origin = None)
		self.spotlight.draw((512 - actual_x, 384 + ydiff), origin = None)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
			
	def draw_playing(self, include_logo):
		self.background.draw((512, 384), origin = None, color = Color(0.8, 0.8, 0.8, 1.0))
		
		if self.last_match_time + 1000 > Gloss.tick_count:
			glBlendFunc(GL_SRC_ALPHA, GL_ONE)
			
			# we need our flash to fade up quickly, then fade out slowly			
			background_colour_anim = (Gloss.tick_count - self.last_match_time) / 1000
			if background_colour_anim < 0.1:
				fade_in_anim = Gloss.lerp(0, 0.3, background_colour_anim * 10)
				self.lensflare.draw((512, 384), origin = None, color = Color(1, 1, 1, fade_in_anim))
			else:
				self.lensflare.draw((512, 384), origin = None, color = Color(1, 1, 1, (1 - background_colour_anim) / 3))
			
			rings_alpha = Gloss.lerp(0.05, 0, background_colour_anim)
			self.rings.draw((512, 384), origin = None, color = Color(1, 1, 1, rings_alpha), scale = background_colour_anim * 4)
			glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		if include_logo:
			self.logo_small.draw(self.playing_logo_position, scale = 1.0, origin = None)
		
		if self.down_over_menu_button:
			self.menu_button_down.draw(self.menu_button_position)
		else:
			self.menu_button.draw(self.menu_button_position)

		self.score_bg.draw((35, 20))	
		self.sans_font.draw(str(self.score), (59, 60))
		
		self.timer_bg.draw(position = (790, 45), color = Color(0, 0, 0, 0.5))
				
		if self.timer < 10 and self.timer > 0:
			if datetime.datetime.now().microsecond < 500000:
				self.draw_timer()
		else:
			self.draw_timer()
		
		if self.last_colour_match_time + 4000 > Gloss.tick_count:
			anim_pos = (self.last_colour_match_time + 4000) - Gloss.tick_count
			
			if anim_pos > 3500:
				# anim is just starting - move it in!
				colours_bg_anim = (Gloss.tick_count - self.last_colour_match_time) / 500.0
				if colours_bg_anim > 1: colours_bg_anim = 1
				colours_bg_x = Gloss.smooth_step(-300, 0, colours_bg_anim)

				pass
				
			elif anim_pos < 500:
				# anim is ending - move it out!
				colours_bg_anim = anim_pos / 500.0
				if colours_bg_anim > 1: colours_bg_anim = 1
				colours_bg_x = Gloss.smooth_step(0, -300, 1 - colours_bg_anim)
				pass
				
			else:
				# anim is doing nothing - don't move it!
				colours_bg_x = 0
			
			self.colours_bg.draw((colours_bg_x, 185))

		
			for i in range(0, len(self.colour_list)):
				colour = self.colour_list[i]
				draw_colour = Color(1, 1, 1, 0.3)
				
				if colour in self.used_words:
					draw_colour = Color.WHITE
			
				if i % 2 is 0:
					self.mono_font.draw(colour, position = (colours_bg_x + 33, 245 + 36 * (i / 2)), color = draw_colour)
				else:
					self.mono_font.draw(colour, position = (colours_bg_x + 133, 245 + 36 * ((i - 1) / 2)), color = draw_colour)

		self.letter_list[self.current_word[0].char].draw(self.current_word[0].draw_position)
		self.letter_list[self.current_word[1].char].draw(self.current_word[1].draw_position)
		self.letter_list[self.current_word[2].char].draw(self.current_word[2].draw_position)
		self.letter_list[self.current_word[3].char].draw(self.current_word[3].draw_position)
		
		if self.down_over_refresh_letters:
			self.refresh_letters_down.draw(self.refresh_letters_position)
		else:
			self.refresh_letters.draw(self.refresh_letters_position)


		# draw the bonus word box
			
		if self.last_bonus_word_time != -1:
			self.melody_happy_small.draw((796, 136))
		else:
			self.melody_important_small.draw((796, 136))
			
		self.bonus_word_box.draw((764, 370))
		
		bonus_word_size = self.serif_font.measure_string(self.current_bonus_word)
		
		self.serif_font.draw(self.current_bonus_word, (879 - bonus_word_size[0] / 2, 420), color = Color.BLACK)
					
		# we draw all our letters except the selected one
		for i in range(0, len(self.letters)):
			letter = self.letters[i]
			if letter is not self.selected_letter:
				self.letter_list[letter.char].draw(letter.draw_position)
			
		# draw the selected one last so that it always appears on top
		if self.selected_letter is not None:
			glow_pos = (self.selected_letter.draw_position[0] - 18, self.selected_letter.draw_position[1] - 18)
			
			if self.drop_status is DROP_GOOD:
				self.drop_good.draw(glow_pos)
			elif self.drop_status is DROP_BAD:
				self.drop_bad.draw(glow_pos)
			else:
				self.drop_unknown.draw(glow_pos)

			self.letter_list[self.selected_letter.char].draw(self.selected_letter.draw_position)
			
		if self.matched_letter is not None:
			anim_pos = (Gloss.tick_count - self.last_match_time) / 500.0
			
			if anim_pos > 1:
				self.matched_letter = None
			else:
				self.letter_list[self.matched_letter.char].draw(self.matched_letter.draw_position, scale = 1.0 - anim_pos, rotation = anim_pos * 360, origin = None, color = Color(1.0, 1.0, 1.0, 1 - anim_pos))
		
		for particles in reversed(self.particles):
			if not particles.alive:
				self.particles.remove(particles)
			else:
				particles.draw()
			
		for bonus in self.bonus_text:
			bonus.draw()
			
	def draw_timer(self):
		timer_x = 821
		timer_y = 45
		
		minutes = time.strftime("%M", time.gmtime(self.timer))
		seconds = time.strftime("%S", time.gmtime(self.timer))

		if minutes[0] == "0":
			minutes = minutes[1:]
		
		self.sans_font.draw(minutes + ":" + seconds, (timer_x + 4, timer_y + 4), color = Color(0.0, 0.0, 0.0, 0.4))
		self.sans_font.draw(minutes + ":" + seconds, (timer_x + 2, timer_y + 2), color = Color(0.0, 0.0, 0.0, 0.7))
		self.sans_font.draw(minutes + ":" + seconds, (timer_x, timer_y), color = Color.YELLOW, second_color = Color(0.8, 0.1, 0.0, 1.0), )		
			
	def get_current_letters(self):
		test_word = []
	
		for current_letter in self.current_word:
			test_word += current_letter.char
			
		return test_word
		
	def get_current_word(self):
		return ''.join(self.get_current_letters())
		
	def new_game(self):
		# reset key variables
		self.selected_letter = None
		self.matched_letter = None
		self.last_match_time = -1000
		self.last_colour_match_time = -10000
		self.last_bonus_word_time = -1
		self.timer = 180
		self.score = 0
		self.last_drop_slot = None
		self.down_over_refresh_letters = False
		self.down_over_menu_button = False

		
		self.used_words = []
		self.bonus_text = []
		self.generate_starting_word(False)
		
		self.current_bonus_word = self.active_word.upper()
		
		while self.current_bonus_word == self.active_word.upper():
			self.current_bonus_word = choice(self.starting_words).upper()
		
		# create an empty list for our starting letters
		self.letters = []
		
		# now add some random letters to get us started!
		for i in range(0, 10):
			self.add_letter()
						
		self.reposition_letters()
		
	def generate_starting_word(self, player_requested):
		self.active_word = choice(self.starting_words)
				
		while self.active_word.upper() == self.current_bonus_word:
			self.active_word = choice(self.starting_words)
		
		self.current_word = []
		self.current_word.append(SwitcharooLetter((321, 240), self.active_word[0]))
		self.current_word.append(SwitcharooLetter((421, 240), self.active_word[1]))
		self.current_word.append(SwitcharooLetter((521, 240), self.active_word[2]))
		self.current_word.append(SwitcharooLetter((621, 240), self.active_word[3]))
		
		if player_requested:
			# subtract 10-point penalty
			self.score -= 10
			if self.score < 0: self.score = 0
			
			# kill all existing particle systems
			self.particles = []
			
			for letter in self.current_word:
				self.particles.append(self.create_particles(letter.position))

	def add_letter(self):
		self.letters.append(SwitcharooLetter(char = self.get_letter()))

	def reposition_letters(self):
		for i in range(0, len(self.letters)):
			letter = self.letters[i]
			letter.position = (15 + (i * 100), 540)
			letter.draw_position = letter.position
			
	def create_particles(self, position):
		particles = ParticleSystem(texture = self.smoke, position = Point.add(position, (self.letter_width / 2, self.letter_height / 2)), initialparticles = 100, minspeed = 200, maxspeed = 300, growth = -1, drag = 5)
		particles.additive = True
		return particles
			
	def get_letter(self):
		freq_a = 8167
		freq_b = freq_a + 1492
		freq_c = freq_b + 2782
		freq_d = freq_c + 4253
		freq_e = freq_d + 12702
		freq_f = freq_e + 2228
		freq_g = freq_f + 2015
		freq_h = freq_g + 6094
		freq_i = freq_h + 6966
		freq_j = freq_i + 153
		freq_k = freq_j + 772
		freq_l = freq_k + 4025
		freq_m = freq_l + 2406
		freq_n = freq_m + 6749
		freq_o = freq_n + 7507
		freq_p = freq_o + 1929
		freq_q = freq_p + 95
		freq_r = freq_q + 5987
		freq_s = freq_r + 6327
		freq_t = freq_s + 9056
		freq_u = freq_t + 2758
		freq_v = freq_u + 978
		freq_w = freq_v + 2360
		freq_x = freq_w + 150
		freq_y = freq_x + 1974
		freq_z = freq_y + 74
	
		random = Gloss.rand_float(0, 100000)
	
		chosen = ""
	
		if random < freq_a:
			chosen = "a"
		elif random < freq_b:
			chosen = "b"
		elif random < freq_c:
			chosen = "c"
		elif random < freq_d:
			chosen = "d"
		elif random < freq_e:
			chosen = "e"
		elif random < freq_f:
			chosen = "f"
		elif random < freq_g:
			chosen = "g"
		elif random < freq_h:
			chosen = "h"
		elif random < freq_i:
			chosen = "i"
		elif random < freq_j:
			chosen = "j"
		elif random < freq_k:
			chosen = "k"
		elif random < freq_l:
			chosen = "l"
		elif random < freq_m:
			chosen = "m"
		elif random < freq_n:
			chosen = "n"
		elif random < freq_o:
			chosen = "o"
		elif random < freq_p:
			chosen = "p"
		elif random < freq_q:
			chosen = "q"
		elif random < freq_r:
			chosen = "r"
		elif random < freq_s:
			chosen = "s"
		elif random < freq_t:
			chosen = "t"
		elif random < freq_u:
			chosen = "u"
		elif random < freq_v:
			chosen = "v"
		elif random < freq_w:
			chosen = "w"
		elif random < freq_x:
			chosen = "x"
		elif random < freq_y:
			chosen = "y"
		else:
			chosen = "z"
	
		got_this_letter_already = False
		
		for letter in self.letters:
			if letter.char is chosen:
				got_this_letter_already = True
				break
				
		if got_this_letter_already:
			return self.get_letter()
		else:
			return chosen
			
	def get_letter_score(self, letter):
		if letter is "a":
			return 1
		elif letter is "b":
			return 3
		elif letter is "c":
			return 3
		elif letter is "d":
			return 2
		elif letter is "e":
			return 1
		elif letter is "f":
			return 4
		elif letter is "g":
			return 2
		elif letter is "h":
			return 4
		elif letter is "i":
			return 1
		elif letter is "j":
			return 8
		elif letter is "k":
			return 5
		elif letter is "l":
			return 1
		elif letter is "m":
			return 3
		elif letter is "n":
			return 1
		elif letter is "o":
			return 1
		elif letter is "p":
			return 3
		elif letter is "q":
			return 10
		elif letter is "r":
			return 1
		elif letter is "s":
			return 1
		elif letter is "t":
			return 1
		elif letter is "u":
			return 1
		elif letter is "v":
			return 4
		elif letter is "w":
			return 4
		elif letter is "x":
			return 8
		elif letter is "y":
			return 4
		else:
			return 10
		

class SwitcharooLetter(object):
	char = ""
	position = (0, 0)
	draw_position = (0, 0)
	
	def __init__(self, position = None, char = ""):
		self.position = position
		self.draw_position = position
		self.char = char
		
class SwitcharooBonus(object):
	def __init__(self, type, position):
		self.type = type
		self.position = position
		self.created_time = Gloss.tick_count

	def draw(self):
		anim_pos = (Gloss.tick_count - self.created_time) / game.bonus_text_life		
		self.type.draw(self.position, color = Color(1, 1, 1, Gloss.smooth_step(1, 0, anim_pos)), origin = None, scale = 1.0 + anim_pos / 3)
		
class SwitcharooScore(object):
	name = ""
	score = 0
	
	def __init__(self, name, score):
		self.name = name
		self.score = score
		
def point_over_rect(x1, y1, x2, y2, width, height):
	if x1 >= x2 and x1 <= x2 + width:
		if y1 >= y2 and y1 <= y2 + height:
			return True
		
	return False

MS_MENU, MS_HOW_TO_PLAY, MS_LOADING_GAME, MS_PLAYING, MS_UNLOADING_GAME, MS_HIGH_SCORES, MS_GAME_OVER_IN, MS_GAME_OVER_SHOWING, MS_GAME_OVER_OUT = range(9)
DROP_GOOD, DROP_BAD, DROP_UNKNOWN = range(3)

#os.environ['SDL_AUDIODRIVER'] = 'pulseaudio' # silly Ubuntu workaround - hangs without this line!
game = Switcharoo("Switcharoo")
Gloss.screen_resolution = (1024,768)
game.run()
