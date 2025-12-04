import time
import pgzero.music as music

WIDTH = 1000
HEIGHT = 600

game_state = "menu"

def load_frames(prefix, count):
    return [f"{prefix}-{i:02}" for i in range(count)]

def load_frames_flip(prefix, count):
    return [f"{prefix}-{i:02}_flip" for i in range(count)]

class Player:
    def __init__(self, x, y):
        self.idle = load_frames("adventurer-idle", 4)
        self.idle_flip = load_frames_flip("adventurer-idle", 4)
        self.run = load_frames("adventurer-run", 6)
        self.run_flip = load_frames_flip("adventurer-run", 6)
        self.jump = load_frames("adventurer-jump", 4)
        self.jump_flip = load_frames_flip("adventurer-jump", 4)
        self.state = "idle"
        self.facing = "right"
        self.frame_index = 0
        self.anim_speed = 0.20
        self.actor = Actor(self.idle[0])
        self.actor.pos = (x, y)
        self.vx = 0
        self.vy = 0
        self.speed = 4
        self.jump_force = -12
        self.gravity = 0.5
        self.on_ground = False
        self.hp = 100
        self.score = 0
        self.last_damage_time = 0 

    @property
    def hitbox(self):
        return Rect((self.actor.x - 20, self.actor.y - 45), (40, 50))

    def animate(self):
        if self.state == "idle":
            frames = self.idle if self.facing == "right" else self.idle_flip
        elif self.state == "run":
            frames = self.run if self.facing == "right" else self.run_flip
        else:
            frames = self.jump if self.facing == "right" else self.jump_flip

        self.frame_index += self.anim_speed
        if self.frame_index >= len(frames):
            self.frame_index = 0
        self.actor.image = frames[int(self.frame_index)]

    def update(self):
        self.vx = 0

        if keyboard.left:
            self.vx = -self.speed
            self.facing = "left"
            if self.on_ground:
                self.state = "run"

        elif keyboard.right:
            self.vx = self.speed
            self.facing = "right"
            if self.on_ground:
                self.state = "run"

        else:
            if self.on_ground:
                self.state = "idle"

        if keyboard.up and self.on_ground:
            self.vy = self.jump_force
            self.state = "jump"

        self.vy += self.gravity

        self.actor.x += self.vx
        self.handle_horizontal()

        self.actor.y += self.vy
        self.handle_vertical()
        self.animate()

        if time.time() - self.last_damage_time > 1:
            self.hp = min(100, self.hp + 0.05)

    def handle_horizontal(self):
        for p in platforms:
            if self.hitbox.colliderect(p.rect):
                if self.vx > 0:
                    self.actor.x = p.rect.left - 25
                elif self.vx < 0:
                    self.actor.x = p.rect.right + 25

    def handle_vertical(self):
        self.on_ground = False

        for p in platforms:
            if self.hitbox.colliderect(p.rect):
                if self.vy > 0:
                    self.actor.y = p.rect.top - 5
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.actor.y = p.rect.bottom + 50
                    self.vy = 0

        ground_y = HEIGHT - 20
        if self.hitbox.bottom >= ground_y:
            self.actor.y = ground_y - 5
            self.vy = 0
            self.on_ground = True

    def draw(self):
        self.actor.draw()

class Platform:
    def __init__(self, x, y, w, h):
        self.rect = Rect((x, y), (w, h))

    def draw(self):
        screen.draw.filled_rect(self.rect, (120, 70, 30))

class Enemy:
    def __init__(self, x, y, left_limit, right_limit):
        self.frames = load_frames("adventurer-run", 6)
        self.frames_flip = load_frames_flip("adventurer-run", 6)

        self.facing = "right"
        self.frame_index = 0
        self.anim_speed = 0.18

        self.actor = Actor(self.frames[0])
        self.actor.pos = (x, y)

        self.left_limit = left_limit
        self.right_limit = right_limit
        self.speed = 2

    @property
    def hitbox(self):
        return Rect((self.actor.x - 20, self.actor.y - 45), (40, 50))

    def animate(self):
        frames = self.frames if self.facing == "right" else self.frames_flip
        self.frame_index += self.anim_speed
        if self.frame_index >= len(frames):
            self.frame_index = 0
        self.actor.image = frames[int(self.frame_index)]

    def update(self):
        self.actor.x += self.speed

        if self.actor.x < self.left_limit:
            self.facing = "right"
            self.speed *= -1
        if self.actor.x > self.right_limit:
            self.facing = "left"
            self.speed *= -1

        if self.hitbox.colliderect(player.hitbox):
            if time.time() - player.last_damage_time > 0.8:
                player.hp -= 30
                player.last_damage_time = time.time()

                if player.hp <= 0:
                    global game_state
                    game_state = "lose"
        self.animate()
    def draw(self):
        self.actor.draw()

class Coin:
    def __init__(self, x, y):
        self.actor = Actor("coin")
        self.actor.pos = (x, y)
        self.collected = False

    @property
    def hitbox(self):
        return Rect((self.actor.x - 15, self.actor.y - 15), (30, 30))

    def update(self):
        if not self.collected and player.hitbox.colliderect(self.hitbox):
            self.collected = True
            player.score += 1

    def draw(self):
        if not self.collected:
            self.actor.draw()

class Finish:
    def __init__(self, x, y):
        self.actor = Actor("flag")
        self.actor.pos = (x, y)

    @property
    def hitbox(self):
        return Rect((self.actor.x - 20, self.actor.y - 40), (40, 50))

    def update(self):
        if player.hitbox.colliderect(self.hitbox):
            global game_state
            game_state = "win"

    def draw(self):
        self.actor.draw()

player = Player(100, 480)

platforms = [
    Platform(0, HEIGHT - 20, WIDTH, 20),
    Platform(200, 480, 200, 20),
    Platform(450, 380, 180, 20),
    Platform(300, 290, 200, 20),
    Platform(550, 210, 180, 20),
]

enemies = [
    Enemy(400, 520, 350, 650),
    Enemy(250, 430, 200, 380)
]

coins = [
    Coin(220, 450),
    Coin(520, 350),
    Coin(330, 260),
    Coin(750, 180)
]

finish = Finish(900, 160)

def draw():
    screen.clear()

    if game_state == "menu":
        screen.draw.text("PLATFORMER GAME", center=(WIDTH//2, 100), fontsize=48, color="white")
        screen.draw.text("Click to Start", center=(WIDTH//2, 200), fontsize=36)

    elif game_state == "playing":
        screen.blit("forest_bg", (0, 0))

        for p in platforms: p.draw()
        for c in coins: c.draw()
        for e in enemies: e.draw()
        finish.draw()
        player.draw()

        hp_width = 200
        hp_height = 20
        hp_x = 20
        hp_y = 20

        screen.draw.filled_rect(Rect((hp_x-2, hp_y-2), (hp_width+4, hp_height+4)), (0, 0, 0))
        screen.draw.filled_rect(Rect((hp_x, hp_y), (hp_width, hp_height)), (120, 0, 0))

        green_width = int((player.hp / 100) * hp_width)
        screen.draw.filled_rect(Rect((hp_x, hp_y), (green_width, hp_height)), (0, 200, 0))

        screen.draw.text(f"{int(player.hp)} HP",
                         center=(hp_x + hp_width/2, hp_y + hp_height/2),
                         fontsize=24, color="white")

        score_x = 20
        score_y = 60
        screen.draw.text(f"Score: {player.score}", (score_x+2, score_y+2),
                         fontsize=40, color="black")
        screen.draw.text(f"Score: {player.score}", (score_x, score_y),
                         fontsize=40, color=(230, 200, 50))

    elif game_state == "lose":
        screen.draw.text("YOU LOSE", center=(WIDTH//2, HEIGHT//2), fontsize=64, color="red")
        screen.draw.text(f"Final Score: {player.score}", center=(WIDTH//2, HEIGHT//2+80), fontsize=40)

    elif game_state == "win":
        screen.draw.text("YOU WIN!", center=(WIDTH//2, HEIGHT//2), fontsize=64, color="green")
        screen.draw.text(f"Final Score: {player.score}", center=(WIDTH//2, HEIGHT//2+80), fontsize=40)

def update(dt):
    if game_state == "playing":
        player.update()
        for e in enemies: e.update()
        for c in coins: c.update()
        finish.update()

def on_mouse_down(pos):
    global game_state
    if game_state == "menu":
        game_state = "playing"
        music.play("adventure")
        music.set_volume(0.6)
