import json
import pygame
import random
from pathlib import Path
from game.player import Player,LANE_W
from game.traffic import Car,make_car

LANES=8
WIDTH=LANES*LANE_W
HEIGHT=600
FPS=60
BG=(60,60,60)
WATER_Y=HEIGHT//2-35
WATER_H=70
RAFT_W=180
RAFT_SPEED=2
HIGH_SCORE_PATH=Path(__file__).resolve().parent.parent/"high_scores.json"
DAY_NIGHT_INTERVAL=30000

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Traffic Escape")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",24,bold=True)
        self.big_font=pygame.font.SysFont("monospace",44,bold=True)
        self.high_score_path=HIGH_SCORE_PATH
        self.high_scores=self._load_high_scores()
        self.is_night=False
        self.last_day_night_switch=pygame.time.get_ticks()
        self.headlight_surface=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        self.reset()

    def reset(self):
        self.player=Player(WIDTH//2,HEIGHT-80)
        self.cars=[]
        self.timer=0
        self.spawn_interval=50
        self.speed=3
        self.score=0
        self.lives=3
        self.raft=pygame.Rect(WIDTH//2-RAFT_W//2,WATER_Y,RAFT_W,WATER_H)
        self.raft_speed=RAFT_SPEED
        self.riding_raft=False
        self.score_saved=False
        self.game_over=False
        self.won=False

    def _load_high_scores(self):
        try:
            with self.high_score_path.open(encoding="utf-8") as scores_file:
                scores=json.load(scores_file)
        except (OSError,UnicodeDecodeError,json.JSONDecodeError):
            return []
        if not isinstance(scores,list):
            return []
        valid_scores=[score for score in scores if isinstance(score,int) and not isinstance(score,bool) and score>=0]
        return sorted(valid_scores,reverse=True)[:5]

    def _record_score(self):
        if self.score_saved:
            return
        self.score_saved=True
        self.high_scores=sorted([*self.high_scores,self.score//10],reverse=True)[:5]
        try:
            with self.high_score_path.open("w",encoding="utf-8") as scores_file:
                json.dump(self.high_scores,scores_file)
        except OSError:
            pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r: self.reset()
        return True

    def update(self):
        now=pygame.time.get_ticks()
        while now-self.last_day_night_switch>=DAY_NIGHT_INTERVAL:
            self.is_night=not self.is_night
            self.last_day_night_switch+=DAY_NIGHT_INTERVAL
        if self.game_over or self.won: return
        previous_raft_x=self.raft.x
        self.raft.x+=self.raft_speed
        if self.raft.left<0:
            self.raft.left=0
            self.raft_speed=abs(self.raft_speed)
        elif self.raft.right>WIDTH:
            self.raft.right=WIDTH
            self.raft_speed=-abs(self.raft_speed)
        raft_dx=self.raft.x-previous_raft_x
        if self.riding_raft:
            self.player.rect.x=max(0,min(WIDTH-self.player.rect.width,self.player.rect.x+raft_dx))
        keys=pygame.key.get_pressed()
        self.player.move(keys,0,WIDTH)
        self.timer+=1
        if self.timer>=self.spawn_interval:
            lane=random.randint(0,LANES-1)
            self.cars.append(make_car(lane,HEIGHT,self.speed))
            self.timer=0
            self.spawn_interval=max(22,self.spawn_interval-0.2)
        for c in self.cars:
            c.update()
        in_water=self.player.rect.colliderect(pygame.Rect(0,WATER_Y,WIDTH,WATER_H))
        on_raft=in_water and self.player.rect.colliderect(self.raft)
        hit_by_car=not on_raft and any(c.rect.colliderect(self.player.rect) for c in self.cars)
        if hit_by_car or (in_water and not on_raft):
            self.lives-=1
            self.riding_raft=False
            if self.lives==0:
                self.game_over=True
            else:
                self.player=Player(WIDTH//2,HEIGHT-80)
                self.cars=[]
        else:
            self.riding_raft=on_raft
        self.cars=[c for c in self.cars if not c.off_screen(HEIGHT)]
        self.score+=1
        if self.score%300==0: self.speed=min(10,self.speed+0.5)
        if self.player.rect.top<=10:
            self.won=True
        if self.game_over or self.won:
            self._record_score()

    def draw(self):
        background=(14,22,34) if self.is_night else BG
        lane_color=(55,69,82) if self.is_night else (100,100,100)
        marking_color=(105,104,76) if self.is_night else (200,200,100)
        sidewalk_color=(62,66,69) if self.is_night else (150,130,110)
        water_color=(15,54,78) if self.is_night else (28,115,150)
        water_edge=(55,105,122) if self.is_night else (90,185,195)
        raft_color=(94,67,46) if self.is_night else (135,86,44)
        log_color=(68,51,37) if self.is_night else (92,55,28)
        hud_color=(7,12,21) if self.is_night else (20,20,20)
        self.screen.fill(background)
        # road markings
        for i in range(LANES+1):
            pygame.draw.line(self.screen,lane_color,(i*LANE_W,0),(i*LANE_W,HEIGHT),2)
        for y in range(0,HEIGHT,60):
            for i in range(LANES):
                pygame.draw.rect(self.screen,marking_color,pygame.Rect(i*LANE_W+LANE_W//2-3,y,6,30))
        # sidewalks
        pygame.draw.rect(self.screen,sidewalk_color,pygame.Rect(0,HEIGHT-50,WIDTH,50))
        pygame.draw.rect(self.screen,sidewalk_color,pygame.Rect(0,0,WIDTH,30))
        if self.is_night:
            self.headlight_surface.fill((0,0,0,0))
            for c in self.cars: self._draw_headlight_beams(c)
            self.screen.blit(self.headlight_surface,(0,0))
        for c in self.cars:
            c.draw(self.screen)
            if self.is_night: self._draw_headlight_lamps(c)
        pygame.draw.rect(self.screen,water_color,pygame.Rect(0,WATER_Y,WIDTH,WATER_H))
        pygame.draw.line(self.screen,water_edge,(0,WATER_Y),(WIDTH,WATER_Y),2)
        pygame.draw.line(self.screen,water_edge,(0,WATER_Y+WATER_H),(WIDTH,WATER_Y+WATER_H),2)
        raft_visual=pygame.Rect(self.raft.x,WATER_Y+7,RAFT_W,WATER_H-14)
        pygame.draw.rect(self.screen,raft_color,raft_visual,border_radius=8)
        for x in range(self.raft.x+24,self.raft.right,28):
            pygame.draw.line(self.screen,log_color,(x,raft_visual.top+3),(x,raft_visual.bottom-3),3)
        self.player.draw(self.screen)
        hud=pygame.Rect(0,0,WIDTH,30)
        pygame.draw.rect(self.screen,(20,20,20),hud)
        s=self.font.render(f"Score: {self.score//10}  Lives: {self.lives}  Reach top  R=Restart",True,(220,220,220))
        self.screen.blit(s,(6,4))
        if self.game_over:
            self._msg("CRASHED!",(220,60,60))
        if self.won:
            self._msg("YOU MADE IT!",(80,220,80))
        pygame.display.flip()

    def _draw_headlight_beams(self,car):
        if car.direction==1:
            near_y=car.rect.bottom
            far_y=min(HEIGHT,near_y+180)
        else:
            near_y=car.rect.top
            far_y=max(0,near_y-180)
        for center_x in (car.rect.x+18,car.rect.x+42):
            pygame.draw.polygon(self.headlight_surface,(255,226,145,38),[
                (center_x-4,near_y),(center_x+4,near_y),
                (center_x+38,far_y),(center_x-38,far_y),
            ])

    def _draw_headlight_lamps(self,car):
        lamp_y=car.rect.bottom-8 if car.direction==1 else car.rect.top+3
        for lamp_x in (car.rect.x+9,car.rect.x+45):
            pygame.draw.ellipse(self.screen,(255,242,180),pygame.Rect(lamp_x,lamp_y,7,5))

    def _msg(self,text,color):
        ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,150))
        self.screen.blit(ov,(0,0))
        m=self.big_font.render(text,True,color)
        sub=self.font.render("Press R to Restart",True,(200,200,200))
        title=self.font.render("TOP 5 SCORES",True,(220,220,220))
        self.screen.blit(m,(WIDTH//2-m.get_width()//2,HEIGHT//2-170))
        self.screen.blit(sub,(WIDTH//2-sub.get_width()//2,HEIGHT//2-115))
        self.screen.blit(title,(WIDTH//2-title.get_width()//2,HEIGHT//2-65))
        for index in range(5):
            score=self.high_scores[index] if index<len(self.high_scores) else "--"
            row=self.font.render(f"{index+1}. {score}",True,(200,200,200))
            self.screen.blit(row,(WIDTH//2-row.get_width()//2,HEIGHT//2-30+index*26))

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
