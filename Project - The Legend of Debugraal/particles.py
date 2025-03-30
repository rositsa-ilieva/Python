import pygame
from support import import_folder
from random import choice

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            'flame': import_folder('images/particles/flame/frames'),
			'aura': import_folder('images/particles/aura'),
			'heal': import_folder('images/particles/heal/frames'),
            'slash': import_folder('images/particles/slash/')
        }
    
    def reflect_images(self, frames):
        new_frames = []
        for frame in frames:
            flipped_fr = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_fr)
        return new_frames

    def create_particles(self, animation_type, pos, groups):
        if animation_type not in self.frames:
            return
    
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.frame_ind = 0
        self.animation_speed = 0.5
        self.frames = animation_frames
        self.image = self.frames[self.frame_ind]
        self.rect = self.image.get_rect(center = pos)
        self.sprite_type = 'magic'

    def animate(self):
        self.frame_ind += self.animation_speed
        if self.frame_ind >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_ind)]

    def update(self):
        self.animate()