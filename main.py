import pygame
import random
import sys
import time
import asyncio
import os
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

# Game Story Data
STORY = {
    "START":{
        "text": "You wake up on a near-empty train compartment.\nThe lights hum softly above you, flickering every few seconds.\nYou don’t remember boarding this late. The city outside is gone — only tunnels flash by.\n",
        "choices":{
            "Explore the compartment": "EXPLORE",
            "Try the doors": "DOORS",
            "Call out for help": "CALL_OUT"
        },
        "bgm": "Sounds/START.wav",
        "bgm_volume": 0.5,
        "sound_effect": None,
        "image": "Images/START.png"
    },
    "EXPLORE":{
        "text": "You wander down the aisle. A forgotten bag sits on a seat.\nInside, you find a cracked phone — the screen glows with a single unread message:\n\n“Don’t stay on after midnight.”\n\nThe train jolts suddenly.\nThe intercom crackles again:\n\n“Still awake, passenger?”\n\n",
        "choices":{
            "Continue": "NEXT_MOVE"
        },
        "bgm": "Sounds/EXPLORE-DOORS-CALL_OUT.flac",
        "bgm_volume": 0.5,
        "sound_effect": None,
        "image": "Images/EXPLORE.png"
    },
    "DOORS":{
        "text": "You pull at the doors, but they won't budge.\nThrough the glass, the tunnel walls rush by in the blur —\nthen you glimpse something impossible:\n\n A figure on the platform as you pass, waving slowly. No stations were supposed to be left late.\n\n The intercom hums:\n\“Please remain seated.”\n\n",
        "choices":{
            "Continue": "NEXT_MOVE"
        },
        "bgm": "Sounds/EXPLORE-DOORS-CALL_OUT.flac",
        "bgm_volume": 0.5,
        "sound_effect": None,
        "image": "Images/DOORS.png"
    },
    "CALL_OUT":{
        "text": "Your voice echoes through the car:\n“Hello? Anyone there?”\n\nA pause. Then, faintly —\n\n“Yes.”\n\nA chill runs down your spine. The voice sounds like… you.\n",
        "choices":{
            "Continue": "NEXT_MOVE"
        },
        "bgm": "Sounds/EXPLORE-DOORS-CALL_OUT.flac",
        "bgm_volume": 0.5,
        "sound_effect": None,
        "image": "Images/CALL_OUT.png"
    },
    "NEXT_MOVE":{
        "text": "You move toward the next compartment.\nThe sliding door hisses open — the same dull seats, the same flickering lights.\nBut this time, one seat is occupied.\n\nA passenger sits perfectly still, head down.\n",
        "choices":{
            "Approach and speak": "APPROACH",
            "Turn back": "TURN_BACK",
            "Check the next compartment quietly": "SNEAK"
        },
        "bgm": "Sounds/NEXT_MOVE.wav",
        "bgm_volume": 0.5,
        "sound_effect": None,
        "image": "Images/NEXT_MOVE.png"
    },
    "APPROACH":{
        "text": "You step closer. The figure raises its head.\nIt’s your face — pale, tired, but unmistakable.\n\nYour reflection smiles faintly.\n\n“We missed our stop.”\n\nThe lights go out for a moment. When they return, the seat is empty.\nA note lies where the figure sat: “You can still get off.”\n\n",
        "choices":{
            "Continue": "VOICE_SCENE"
        },
        "bgm": "Sounds/APPROACH-TURN_BACK-SNEAK.mp3",
        "bgm_volume": 0.5,
        "sound_effect": None,
        "image": "Images/APPROACH.png"
    },
    "TURN_BACK":{
        "text": "You rush back into the previous car, heart pounding.\nBut something’s changed.\nYour seat now has a folded note on it:\n\n“You can’t go back.”\n\nThe train picks up speed.\n",
        "choices":{
            "Continue": "VOICE_SCENE"
        },        
        "bgm": "Sounds/APPROACH-TURN_BACK-SNEAK.mp3",
        "bgm_volume": 0.5,
        "sound_effect": None,
        "image": "Images/TURN_BACK.png"
    },
    "SNEAK":{
        "text": "You quietly slip past the figure and into the next car.\nNo passengers. Just a conductor’s cap resting on a seat.\nThe timetable on the wall reads:\n\nDESTINATION: NOWHERE\nARRIVAL: NEVER\n\nThe intercom flickers to life again.\n\n“Still searching, are you?”\n\n",
        "choices":{
            "Continue": "VOICE_SCENE"
        },
        "bgm": "Sounds/APPROACH-TURN_BACK-SNEAK.mp3",
        "bgm_volume": 0.5,
        "sound_effect": None,
        "image": "Images/SNEAK.png"
    },
    "VOICE_SCENE":{
        "text": "The intercom’s static grows louder.\n\n“You shouldn’t be here. The train runs on time — but not for you.”\n\nThe windows go black.\nThe world outside disappears.\n",
        "choices":{
            "Pull the emergency brake": "ENDING_ESCAPE",
            "Sit back down": "ENDING_WAKE",
            "Head toward the engine": "ENDING_CONDUCTOR"
        },
        "bgm": "Sounds/VOICE_SCENE.mp3",
        "bgm_volume": 0.1,
        "sound_effect": None,
        "image": "Images/VOICE_SCENE.png"
    },
    "ENDING_ESCAPE":{
        "text": "You grab the emergency lever and pull.\n\nWhen the doors finally open, you step out into a dim, empty station.\nA single clock on the wall reads 12:00 — frozen.\n\nYou’re free.\nOr maybe you just stopped time.\n\n\nENDING A — “You Escaped the Loop.”\n\n",
        "choices":{
            "Play again": "RESTART"
        },
        "bgm": "Sounds/ENDING_ESCAPE.wav",
        "bgm_volume": 0.5,
        "sound_effect": None,
        "image": "Images/ENDING_ESCAPE.png"
    },
    "ENDING_WAKE":{
        "text": "You take a slow breath and sit back down.\nThe voice softens.\n\n“You’ve learned, haven’t you? The train keeps going until you’re ready to get off.”\n\nYou close your eyes.\nWhen you open them, sunlight floods in through the window.\nYour stop. Your city.\n\nThe train doors slide open normally.\nYou step out, unsure if you ever left.\n\n\nENDING B — “Woke from the Ride.”\n\n",
        "choices":{
            "Play again": "RESTART"
        },
        "bgm": "Sounds/ENDING_WAKE.mp3",
        "bgm_volume": 0.5,
        "sound_effect": None,
        "image": "Images/ENDING_WAKE.png"
    },
    "ENDING_CONDUCTOR":{
        "text": "You walk toward the front of the train.\nThe doors open one by one until you reach the engine room.\n\nNo driver — only a mirror.\nYour reflection stares back.\n\nWhen you touch the glass, it ripples like water.\nYou step through.\n\n“Next stop… wherever they’re not ready to leave.”\n\nYour voice echoes over the intercom.\n\n\nENDING C — “The New Conductor.”\n\n",
        "choices":{
            "Play again": "RESTART"
        },
        "bgm": "Sounds/ENDING_CONDUCTOR.wav",
        "bgm_volume": 0.5,
        "sound_effect": None,
        "image": "Images/ENDING_CONDUCTOR.png"
    },
    "RESTART":{
        "text": "“Welcome back, passenger. You’ve taken this trip before.”\n\n",
        "choices":{
            "Start over": "START"
        },
        "bgm": "Sounds/RESTART.mp3",
        "bgm_volume": 0.5,
        "sound_effect": None,
        "image": "Images/RESTART.png"
    }
}

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (30, 30, 30)
LIGHT_GRAY = (200, 200, 200)
BUTTON_COLOR = (50, 50, 70)
BUTTON_HOVER = (70, 70, 100)
TEXT_COLOR = (220, 220, 220)
EERIE_GREEN = (50, 255, 100)

def get_asset_path(relative_path):
    """
    Get the absolute path to a resource, whether in development or packaged.
    """
    if hasattr(sys, '_MEIPASS'):
        # Path for a PyInstaller packaged app
        base_path = os.path.join(sys._MEIPASS, '_internal')
    else:
        # Path for development
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

class VisualEffects:
    """Handles all visual effects for the game"""
    
    @staticmethod
    def apply_scanlines(screen):
        width, height = screen.get_size()
        scanline_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        for y in range(0, height, 4):
            pygame.draw.line(scanline_surface, (0, 0, 0, 60), (0, y), (width, y))
        screen.blit(scanline_surface, (0, 0))
    
    @staticmethod
    def apply_pixelation(screen, pixelation="medium"):
        pixelation_val = {"minimum": 2, "medium": 4, "maximum": 6}.get(pixelation, 2)
        width, height = screen.get_size()
        small_surf = pygame.transform.scale(screen, (width // pixelation_val, height // pixelation_val))
        screen.blit(pygame.transform.scale(small_surf, (width, height)), (0, 0))
    
    @staticmethod
    def apply_flicker(screen):
        if random.randint(0, 20) == 0:
            flicker_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            flicker_surface.fill((255, 255, 255, 5))
            screen.blit(flicker_surface, (0, 0))
    
    @staticmethod
    def apply_glow(screen):
        width, height = screen.get_size()
        glow_surf = pygame.transform.smoothscale(screen, (width // 2, height // 2))
        glow_surf = pygame.transform.smoothscale(glow_surf, (width, height))
        glow_surf.set_alpha(100)
        screen.blit(glow_surf, (0, 0))
    
    @staticmethod
    def add_glitch_effect(height, width, glitch_surface, intensity="medium"):
        shift_amount = {"minimum": 10, "medium": 20, "maximum": 40}.get(intensity, 20)
        if random.random() < 0.1:
            y_start = random.randint(0, height - 20)
            slice_height = random.randint(5, 20)
            offset = random.randint(-shift_amount, shift_amount)
            slice_area = pygame.Rect(0, y_start, width, slice_height)
            slice_copy = glitch_surface.subsurface(slice_area).copy()
            glitch_surface.blit(slice_copy, (offset, y_start))
    
    @staticmethod
    def add_color_separation(screen, glitch_surface, intensity="medium"):
        color_shift = {"minimum": 2, "medium": 6, "maximum": 10}.get(intensity, 4)
        if random.random() < 0.05:
            for i in range(3):
                x_offset = random.randint(-color_shift, color_shift)
                y_offset = random.randint(-color_shift, color_shift)
                color_shift_surface = glitch_surface.copy()
                color_shift_surface.fill((0, 0, 0))
                color_shift_surface.blit(glitch_surface, (x_offset, y_offset))
                screen.blit(color_shift_surface, (0, 0), special_flags=pygame.BLEND_ADD)
    
    @staticmethod
    def add_rolling_static(screen, height, width, intensity="medium"):
        static_chance = {"minimum": 0.1, "medium": 0.3, "maximum": 0.8}.get(intensity, 0.2)
        static_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        for y in range(0, height, 8):
            if random.random() < static_chance:
                pygame.draw.line(static_surface, (255, 255, 255, random.randint(30, 80)), (0, y), (width, y))
        screen.blit(static_surface, (0, 0), special_flags=pygame.BLEND_ADD)

class TypewriterText:
    """Handles typewriter effect for text"""
    
    def __init__(self, text, min_delay=0.0, max_delay=0.08):
        self.full_text = text
        self.current_text = ""
        self.current_index = 0
        self.last_update = time.time()
        self.next_delay = random.uniform(min_delay, max_delay)
        self.complete = False
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.scroll_offset = 0  # For scrolling
    
    def update(self):
        """Update the typewriter effect"""
        if self.complete:
            return True
        
        current_time = time.time()
        if current_time - self.last_update >= self.next_delay:
            if self.current_index < len(self.full_text):
                self.current_text += self.full_text[self.current_index]
                self.current_index += 1
                self.last_update = current_time
                self.next_delay = random.uniform(self.min_delay, self.max_delay)
            else:
                self.complete = True
        
        return self.complete
    
    def skip(self):
        """Skip to the end of the text"""
        self.current_text = self.full_text
        self.current_index = len(self.full_text)
        self.complete = True
    
    def get_text(self):
        """Get the current displayed text"""
        return self.current_text
    
    def scroll_up(self, amount=20):
        """Scroll text up"""
        self.scroll_offset = max(0, self.scroll_offset - amount)
    
    def scroll_down(self, amount=20):
        """Scroll text down"""
        self.scroll_offset += amount

class Button:
    """Interactive button for choices"""
    
    def __init__(self, x, y, width, height, text, action, wrapped_lines=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        self.visible = False  # Buttons appear after text finishes
        self.wrapped_lines = wrapped_lines if wrapped_lines else [text]
    
    def draw(self, screen, font):
        if not self.visible:
            return
        
        # Draw text only, with color change on hover
        color = EERIE_GREEN if self.hovered else TEXT_COLOR
        
        # Draw each line of wrapped text
        line_height = font.get_height() + 2
        total_text_height = len(self.wrapped_lines) * line_height
        start_y = self.rect.centery - total_text_height // 2
        
        for i, line in enumerate(self.wrapped_lines):
            text_surf = font.render(line, True, color)
            text_rect = text_surf.get_rect(centerx=self.rect.centerx, y=start_y + i * line_height)
            screen.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        if not self.visible:
            return False
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    
    def check_click(self, pos):
        if not self.visible:
            return False
        return self.rect.collidepoint(pos)

class SoundManager:
    """Manages all game sounds and music"""
    
    def __init__(self):
        self.current_bgm = None
        self.bgm_volume = 0.5
        self.sfx_volume = 0.7
    
    def play_bgm(self, filepath, volume=None):
        """Play background music (loops)"""
        if filepath is None:
            return
        
        try:
            if self.current_bgm != filepath:
                pygame.mixer.music.load(get_asset_path(filepath))
                # Use custom volume or default
                vol = volume if volume is not None else self.bgm_volume
                pygame.mixer.music.set_volume(vol)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.current_bgm = filepath
        except Exception as e:
            print(f"Could not load BGM: {filepath} - {e}")
    
    def stop_bgm(self):
        """Stop background music"""
        pygame.mixer.music.stop()
        self.current_bgm = None
    
    def play_sound_effect(self, filepath, volume=None):
        """Play a sound effect (one-shot)"""
        if filepath is None:
            return
        
        try:
            sound = pygame.mixer.Sound(filepath)
            # Use custom volume or default
            vol = volume if volume is not None else self.sfx_volume
            sound.set_volume(vol)
            sound.play()
        except Exception as e:
            print(f"Could not load sound effect: {filepath} - {e}")
    
    def set_bgm_volume(self, volume):
        """Set background music volume (0.0 to 1.0)"""
        self.bgm_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.bgm_volume)
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))

class Game:
    """Main game class"""
    
    def __init__(self):
        # Set up windowed mode
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Late Night Train")
        icon_image = pygame.image.load(get_asset_path("icon.png"))
        pygame.display.set_icon(icon_image)

        self.width, self.height = self.screen.get_size()
        self.clock = pygame.time.Clock()
        
        # Font setup - smaller fonts for 800x600
        self.title_font = pygame.font.Font(get_asset_path("Fonts/punkbabe/PUNKBABE TRIAL.ttf"), 36)
        self.text_font = pygame.font.Font(get_asset_path("Fonts/1942_report/1942.ttf"), 24)
        self.button_font = pygame.font.Font(get_asset_path("Fonts/1942_report/1942.ttf"), 22)

        # Game state
        self.current_scene = "START"
        self.buttons = []
        self.effects = VisualEffects()
        self.typewriter = None
        self.sound_manager = SoundManager()
        self.current_image = None  # Store loaded scene image
        
        # Initialize first scene
        self.load_scene(self.current_scene)
    
    def load_scene(self, scene_key):
        """Load a new scene with typewriter effect"""
        self.current_scene = scene_key
        scene_data = STORY[scene_key]
        
        # Start typewriter effect
        self.typewriter = TypewriterText(scene_data["text"])
        
        # Create buttons but keep them hidden until text finishes
        self.create_buttons()
        
        # Load scene image
        self.load_scene_image(scene_data.get("image"))
        
        # Play scene sound effects and music with individual volumes
        if scene_data.get("bgm"):
            bgm_vol = scene_data.get("bgm_volume", None)
            self.sound_manager.play_bgm(scene_data["bgm"], bgm_vol)
        
        if scene_data.get("sound_effect"):
            sfx_vol = scene_data.get("sfx_volume", None)
            self.sound_manager.play_sound_effect(scene_data["sound_effect"], sfx_vol)
    
    def load_scene_image(self, image_path):
        """Load and scale image for the scene"""
        if image_path is None:
            self.current_image = None
            return
        
        try:
            # Load image
            image = pygame.image.load(get_asset_path(image_path))
            # Scale to fit the top section (40% of screen)
            top_section_height = int(self.height * 0.4)
            window_margin = 20
            target_width = self.width - 2 * window_margin
            target_height = top_section_height - 2 * window_margin
            
            # Scale image maintaining aspect ratio
            image_rect = image.get_rect()
            scale_x = target_width / image_rect.width
            scale_y = target_height / image_rect.height
            scale = min(scale_x, scale_y)
            
            new_width = int(image_rect.width * scale)
            new_height = int(image_rect.height * scale)
            
            self.current_image = pygame.transform.scale(image, (new_width, new_height))
        except Exception as e:
            print(f"Could not load image: {image_path} - {e}")
            self.current_image = None
    
    def create_buttons(self):
        """Create buttons based on current scene"""
        self.buttons = []
        scene_data = STORY[self.current_scene]
        choices = scene_data["choices"]
        
        # Button layout - positioned at bottom, side by side horizontally
        max_button_width = 200  # Maximum width for each button
        button_height = 30
        button_spacing = 30  # Space between buttons
        bottom_margin = 20
        
        # Calculate button data with text wrapping
        button_data = []
        
        for choice_text, action in choices.items():
            # Word wrap the button text if it's too long
            wrapped_lines = self.wrap_button_text(choice_text, max_button_width)
            
            # Calculate actual button dimensions based on wrapped text
            text_height = len(wrapped_lines) * (self.button_font.get_height() + 2)
            button_width = max_button_width
            actual_height = max(button_height, text_height + 10)
            
            button_data.append((choice_text, action, button_width, actual_height, wrapped_lines))
        
        # Find the tallest button for alignment
        max_height = max(data[3] for data in button_data)
        
        # Calculate total width needed
        total_width = sum(data[2] for data in button_data) + button_spacing * (len(button_data) - 1)
        
        # Calculate starting x position to center all buttons
        start_x = (self.width - total_width) // 2
        y_pos = self.height - bottom_margin - max_height
        current_x = start_x
        
        for choice_text, action, button_width, actual_height, wrapped_lines in button_data:
            # Center vertically with the tallest button
            adjusted_y = y_pos + (max_height - actual_height) // 2
            button = Button(current_x, adjusted_y, button_width, actual_height, choice_text, action, wrapped_lines)
            self.buttons.append(button)
            current_x += button_width + button_spacing
    
    def wrap_button_text(self, text, max_width):
        """Wrap button text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surf = self.button_font.render(test_line, True, TEXT_COLOR)
            
            if test_surf.get_width() <= max_width - 10:  # 10px padding
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Word itself is too long, just add it
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines if lines else [text]
    
    def draw_text_wrapped(self, text, x, y, max_width, max_height, surface):
        """Draw wrapped text with scrolling support"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            if '\n' in word:
                parts = word.split('\n')
                for i, part in enumerate(parts):
                    if i > 0:
                        lines.append(' '.join(current_line))
                        current_line = []
                    if part:
                        current_line.append(part)
            else:
                test_line = ' '.join(current_line + [word])
                test_surf = self.text_font.render(test_line, True, TEXT_COLOR)
                if test_surf.get_width() <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        line_height = self.text_font.get_height() + 5
        
        # Apply scroll offset
        scroll_offset = self.typewriter.scroll_offset if self.typewriter else 0
        
        # Calculate total content height
        total_content_height = len(lines) * line_height
        visible_height = max_height - y
        
        # Limit scroll offset to prevent scrolling past content
        if self.typewriter:
            max_scroll = max(0, total_content_height - visible_height)
            self.typewriter.scroll_offset = min(self.typewriter.scroll_offset, max_scroll)
            scroll_offset = self.typewriter.scroll_offset
        
        # Draw lines with scroll offset
        for i, line in enumerate(lines):
            y_pos = y + i * line_height - scroll_offset
            # Only draw if within visible area
            if y_pos + line_height > y and y_pos < max_height:
                text_surf = self.text_font.render(line, True, TEXT_COLOR)
                surface.blit(text_surf, (x, y_pos))
        
        # Return if scrollbar is needed
        return total_content_height > visible_height, total_content_height, visible_height
    
    def draw(self):
        """Draw the game screen"""
        # Create base surface
        base_surface = pygame.Surface((self.width, self.height))
        base_surface.fill(BLACK)
        
        # Draw top 40% - Image area (simulated train window)
        top_section_height = int(self.height * 0.4)
        pygame.draw.rect(base_surface, DARK_GRAY, (0, 0, self.width, top_section_height))
        
        # Draw "window" effect (scaled for 800x600)
        window_margin = 20
        window_rect = pygame.Rect(window_margin, window_margin, 
                                   self.width - 2 * window_margin, 
                                   top_section_height - 2 * window_margin)
        pygame.draw.rect(base_surface, (10, 10, 20), window_rect)
        
        # Draw scene image if available
        if self.current_image:
            # Center the image in the window
            image_rect = self.current_image.get_rect()
            image_rect.center = window_rect.center
            base_surface.blit(self.current_image, image_rect)
        else:
            # Add "tunnel" effect text (scaled) if no image
            tunnel_font = pygame.font.Font(None, 48)
            tunnel_text = tunnel_font.render("T R A I N", True, (30, 30, 40))
            tunnel_rect = tunnel_text.get_rect(center=(self.width // 2, top_section_height // 2))
            base_surface.blit(tunnel_text, tunnel_rect)
        
        # Draw window border
        pygame.draw.rect(base_surface, (100, 100, 120), window_rect, 3)
        
        # Draw bottom 60% - Story text area
        text_area_y = top_section_height
        text_area_height = self.height - top_section_height
        
        # Draw text background
        pygame.draw.rect(base_surface, (15, 15, 25), 
                        (0, text_area_y, self.width, text_area_height))
        
        # Draw title (scaled)
        title = self.title_font.render("LATE NIGHT TRAIN", True, EERIE_GREEN)
        title_rect = title.get_rect(center=(self.width // 2, text_area_y + 20))
        base_surface.blit(title, title_rect)
        
        # Draw story text with typewriter effect (adjusted margins)
        text_margin = 40
        text_y = text_area_y + 50
        
        # Calculate max height for text (leave space for buttons)
        # Get the highest button position to know where to stop text
        button_top = self.height - 40  # default if no buttons
        if self.buttons:
            button_top = min(btn.rect.y for btn in self.buttons)
        
        max_text_height = button_top - 40  # 40px padding above buttons
        
        scrollbar_needed = False
        total_height = 0
        visible_height = 0
        
        if self.typewriter:
            scrollbar_needed, total_height, visible_height = self.draw_text_wrapped(
                self.typewriter.get_text(), text_margin, text_y, 
                self.width - 2 * text_margin - 20, max_text_height, base_surface)  # Reserve space for scrollbar
        
        # Draw scrollbar if needed
        if scrollbar_needed and total_height > 0:
            scrollbar_x = self.width - text_margin
            scrollbar_y = text_y
            scrollbar_width = 8
            scrollbar_height = visible_height
            
            # Background track
            pygame.draw.rect(base_surface, (40, 40, 50), 
                           (scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height))
            
            # Calculate thumb size and position
            thumb_height = max(20, (visible_height / total_height) * scrollbar_height)
            scroll_percentage = self.typewriter.scroll_offset / max(1, total_height - visible_height)
            thumb_y = scrollbar_y + scroll_percentage * (scrollbar_height - thumb_height)
            
            # Draw thumb
            pygame.draw.rect(base_surface, EERIE_GREEN, 
                           (scrollbar_x, thumb_y, scrollbar_width, thumb_height), 
                           border_radius=4)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(base_surface, self.button_font)
        
        # Apply effects to base surface
        self.screen.blit(base_surface, (0, 0))
        
        # Apply visual effects
        width, height = self.screen.get_size()
        glitch_surface = self.screen.copy()
        
        self.effects.add_glitch_effect(height, width, glitch_surface, "minimum")
        self.effects.add_color_separation(self.screen, glitch_surface, "minimum")
        self.effects.add_rolling_static(self.screen, height, width, "minimum")
        self.effects.apply_scanlines(self.screen)
        self.effects.apply_flicker(self.screen)
        
        pygame.display.flip()
    
    def handle_events(self):
        """Handle user input"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Update button hover states
        for button in self.buttons:
            button.check_hover(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                # Allow skipping typewriter effect with spacebar or enter
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    if self.typewriter and not self.typewriter.complete:
                        self.typewriter.skip()
                # Arrow keys for scrolling
                if event.key == pygame.K_UP:
                    if self.typewriter:
                        self.typewriter.scroll_up(30)
                if event.key == pygame.K_DOWN:
                    if self.typewriter:
                        self.typewriter.scroll_down(30)
            
            # Mouse wheel scrolling
            if event.type == pygame.MOUSEWHEEL:
                if self.typewriter:
                    if event.y > 0:  # Scroll up
                        self.typewriter.scroll_up(30)
                    else:  # Scroll down
                        self.typewriter.scroll_down(30)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Skip typewriter on click if not complete
                if self.typewriter and not self.typewriter.complete:
                    self.typewriter.skip()
                else:
                    # Check button clicks
                    for button in self.buttons:
                        if button.check_click(mouse_pos):
                            self.load_scene(button.action)
        
        return True
    
    async def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            
            # Update typewriter effect
            if self.typewriter:
                text_complete = self.typewriter.update()
                if text_complete:
                    # Show buttons when text is complete
                    for button in self.buttons:
                        button.visible = True
            
            self.draw()
            self.clock.tick(60)
            await asyncio.sleep(0)  # Allow other async tasks to run
        
        pygame.quit()
        sys.exit()

async def main():
    game = Game()
    await game.run()
    
asyncio.run(main())