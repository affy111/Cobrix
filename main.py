from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window

import random
import os

Window.fullscreen = True
Window.clearcolor = (0, 0, 0, 1)

BLOCK = 20


class GameArea(Widget):

    def __init__(
        self,
        score_label,
        best_label,
        play_again_btn,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.score_label = score_label
        self.best_label = best_label
        self.play_again_btn = play_again_btn

        self.load_highscore()

        self.restart()

        Clock.schedule_interval(
            self.update,
            0.12
        )

    def load_highscore(self):

        self.highscore = 0

        if os.path.exists(
            "highscore.txt"
        ):

            try:

                with open(
                    "highscore.txt",
                    "r"
                ) as f:

                    self.highscore = int(
                        f.read()
                    )

            except:

                self.highscore = 0

    def save_highscore(self):

        with open(
            "highscore.txt",
            "w"
        ) as f:

            f.write(
                str(self.highscore)
            )

    def restart(self):

        self.snake = [
            [
                5 * BLOCK,
                5 * BLOCK
            ]
        ]

        self.dx = 0
        self.dy = 0

        self.score = 0

        self.paused = False
        self.game_over = False

        self.food = [
            10 * BLOCK,
            10 * BLOCK
        ]

        self.score_label.text = (
            "Score : 0"
        )

        self.best_label.text = (
            f"Best : {self.highscore}"
        )

        self.play_again_btn.opacity = 0
        self.play_again_btn.disabled = True

    def spawn_food(self):

        cols = max(
            5,
            int(self.width // BLOCK)
        )

        rows = max(
            5,
            int(self.height // BLOCK)
        )

        while True:

            food = [

                random.randint(
                    0,
                    cols - 1
                ) * BLOCK,

                random.randint(
                    0,
                    rows - 1
                ) * BLOCK
            ]

            if food not in self.snake:

                self.food = food
                return

    def move(self):

        if self.paused:
            return

        if self.game_over:
            return

        if (
            self.dx == 0
            and
            self.dy == 0
        ):
            return

        x, y = self.snake[0]

        new_head = [

            x + self.dx,

            y + self.dy
        ]

        # WRAP

        if new_head[0] < 0:

            new_head[0] = (
                int(
                    self.width
                    - BLOCK
                )
            )

        elif (
            new_head[0]
            >=
            self.width
        ):

            new_head[0] = 0

        if new_head[1] < 0:

            new_head[1] = (
                int(
                    self.height
                    - BLOCK
                )
            )

        elif (
            new_head[1]
            >=
            self.height
        ):

            new_head[1] = 0

        # BODY HIT

        if new_head in self.snake:

            self.game_over = True

            if (
                self.score
                >
                self.highscore
            ):

                self.highscore = (
                    self.score
                )

                self.save_highscore()

            self.best_label.text = (
                f"Best : {self.highscore}"
            )

            self.play_again_btn.opacity = 1
            self.play_again_btn.disabled = False

            self.score_label.text = (
                f"GAME OVER | Score : {self.score}"
            )

            return

        self.snake.insert(
            0,
            new_head
        )

        # FOOD

        if (

            abs(
                new_head[0]
                -
                self.food[0]
            ) < BLOCK

            and

            abs(
                new_head[1]
                -
                self.food[1]
            ) < BLOCK

        ):

            self.score += 1

            self.score_label.text = (
                f"Score : {self.score}"
            )

            self.spawn_food()

        else:

            self.snake.pop()
            
            
    def update(self, dt):

        self.move()

        self.canvas.clear()

        with self.canvas:

            # Background

            Color(0, 0, 0)

            Rectangle(
                pos=self.pos,
                size=self.size
            )

            # Food

            Color(0, 1, 0)

            Rectangle(
                pos=(
                    self.x + self.food[0],
                    self.y + self.food[1]
                ),
                size=(BLOCK, BLOCK)
            )

            # Snake

            for i, part in enumerate(self.snake):

                # =====================
                # HEAD
                # =====================

                if i == 0:

                    Color(1, 1, 0)

                    Rectangle(
                        pos=(
                            self.x + part[0],
                            self.y + part[1]
                        ),
                        size=(BLOCK, BLOCK)
                    )

                    # Eyes

                    Color(0, 0, 0)

                    if self.dx > 0:

                        Rectangle(
                            pos=(
                                self.x + part[0] + 13,
                                self.y + part[1] + 13
                            ),
                            size=(3, 3)
                        )

                        Rectangle(
                            pos=(
                                self.x + part[0] + 13,
                                self.y + part[1] + 4
                            ),
                            size=(3, 3)
                        )

                    elif self.dx < 0:

                        Rectangle(
                            pos=(
                                self.x + part[0] + 4,
                                self.y + part[1] + 13
                            ),
                            size=(3, 3)
                        )

                        Rectangle(
                            pos=(
                                self.x + part[0] + 4,
                                self.y + part[1] + 4
                            ),
                            size=(3, 3)
                        )

                    elif self.dy > 0:

                        Rectangle(
                            pos=(
                                self.x + part[0] + 4,
                                self.y + part[1] + 13
                            ),
                            size=(3, 3)
                        )

                        Rectangle(
                            pos=(
                                self.x + part[0] + 13,
                                self.y + part[1] + 13
                            ),
                            size=(3, 3)
                        )

                    else:

                        Rectangle(
                            pos=(
                                self.x + part[0] + 4,
                                self.y + part[1] + 4
                            ),
                            size=(3, 3)
                        )

                        Rectangle(
                            pos=(
                                self.x + part[0] + 13,
                                self.y + part[1] + 4
                            ),
                            size=(3, 3)
                        )

                    # Red Fangs

                    Color(1, 0, 0)

                    if self.dx > 0:

                        Rectangle(
                            pos=(
                                self.x + part[0] + 18,
                                self.y + part[1] + 12
                            ),
                            size=(2, 4)
                        )

                        Rectangle(
                            pos=(
                                self.x + part[0] + 18,
                                self.y + part[1] + 4
                            ),
                            size=(2, 4)
                        )

                    elif self.dx < 0:

                        Rectangle(
                            pos=(
                                self.x + part[0],
                                self.y + part[1] + 12
                            ),
                            size=(2, 4)
                        )

                        Rectangle(
                            pos=(
                                self.x + part[0],
                                self.y + part[1] + 4
                            ),
                            size=(2, 4)
                        )

                    elif self.dy > 0:

                        Rectangle(
                            pos=(
                                self.x + part[0] + 4,
                                self.y + part[1] + 18
                            ),
                            size=(4, 2)
                        )

                        Rectangle(
                            pos=(
                                self.x + part[0] + 12,
                                self.y + part[1] + 18
                            ),
                            size=(4, 2)
                        )

                    else:

                        Rectangle(
                            pos=(
                                self.x + part[0] + 4,
                                self.y + part[1]
                            ),
                            size=(4, 2)
                        )

                        Rectangle(
                            pos=(
                                self.x + part[0] + 12,
                                self.y + part[1]
                            ),
                            size=(4, 2)
                        )

                # =====================
                # BODY
                # =====================

                else:

                    Color(1, 0.2, 0.2)

                    Rectangle(
                        pos=(
                            self.x + part[0],
                            self.y + part[1]
                        ),
                        size=(BLOCK, BLOCK)
                    )
                    
                    
class SnakeUI(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(
            orientation="vertical",
            **kwargs
        )

        # =====================
        # TOP BAR
        # =====================

        top_bar = BoxLayout(
            size_hint_y=0.08
        )

        self.score_label = Label(
            text="Score : 0",
            font_size=24
        )

        self.best_label = Label(
            text="Best : 0",
            font_size=24
        )

        top_bar.add_widget(
            self.score_label
        )

        top_bar.add_widget(
            self.best_label
        )

        self.add_widget(
            top_bar
        )

        # =====================
        # PLAY AGAIN
        # =====================

        self.play_again_btn = Button(
            text="PLAY AGAIN",
            size_hint_y=0.08,
            font_size=28,
            opacity=0,
            disabled=True,
            background_normal=""
        )

        self.play_again_btn.bind(
            on_press=self.restart_game
        )

        self.add_widget(
            self.play_again_btn
        )

        # =====================
        # GAME AREA
        # =====================

        self.game = GameArea(
            self.score_label,
            self.best_label,
            self.play_again_btn
        )

        self.game.size_hint_y = 0.66

        self.add_widget(
            self.game
        )

        # =====================
        # CONTROL PANEL
        # =====================

        control_panel = BoxLayout(
            size_hint_y=0.18
        )

        control_panel.add_widget(
            Widget()
        )

        grid = GridLayout(
            cols=3,
            rows=3,
            spacing=8,
            size_hint=(None, None),
            size=(250, 250)
        )

        # Row 1

        grid.add_widget(
            Widget()
        )

        up = self.make_btn("▲")

        up.bind(
            on_press=self.up_move
        )

        grid.add_widget(
            up
        )

        grid.add_widget(
            Widget()
        )

        # Row 2

        left = self.make_btn("◀")

        left.bind(
            on_press=self.left_move
        )

        grid.add_widget(
            left
        )

        self.pause_btn = self.make_btn(
            "II"
        )

        self.pause_btn.bind(
            on_press=self.pause_game
        )

        grid.add_widget(
            self.pause_btn
        )

        right = self.make_btn("▶")

        right.bind(
            on_press=self.right_move
        )

        grid.add_widget(
            right
        )

        # Row 3

        grid.add_widget(
            Widget()
        )

        down = self.make_btn("▼")

        down.bind(
            on_press=self.down_move
        )

        grid.add_widget(
            down
        )

        grid.add_widget(
            Widget()
        )

        control_panel.add_widget(
            grid
        )

        control_panel.add_widget(
            Widget()
        )

        self.add_widget(
            control_panel
        )

    # =====================
    # BUTTON STYLE
    # =====================

    def make_btn(self, text):

        return Button(
            text=text,
            font_size=28,
            background_normal="",
            background_color=(
                0,
                0,
                0,
                1
            ),
            color=(
                1,
                0.2,
                0.2,
                1
            )
        )

    # =====================
    # MOVEMENT
    # =====================

    def left_move(self, instance):

        if self.game.dx != BLOCK:

            self.game.dx = -BLOCK
            self.game.dy = 0

    def right_move(self, instance):

        if self.game.dx != -BLOCK:

            self.game.dx = BLOCK
            self.game.dy = 0

    def up_move(self, instance):

        if self.game.dy != -BLOCK:

            self.game.dx = 0
            self.game.dy = BLOCK

    def down_move(self, instance):

        if self.game.dy != BLOCK:

            self.game.dx = 0
            self.game.dy = -BLOCK

    # =====================
    # PAUSE
    # =====================

    def pause_game(self, instance):

        self.game.paused = (
            not self.game.paused
        )

        if self.game.paused:

            self.pause_btn.text = "▶"

        else:

            self.pause_btn.text = "II"

    # =====================
    # RESTART
    # =====================

    def restart_game(self, instance):

        self.game.restart()

        self.pause_btn.text = "II"

    # =====================
    # SWIPE CONTROL
    # =====================

    def on_touch_down(self, touch):

        self.start_x = touch.x
        self.start_y = touch.y

        return super().on_touch_down(
            touch
        )

    def on_touch_up(self, touch):

        dx = touch.x - self.start_x
        dy = touch.y - self.start_y

        if abs(dx) > abs(dy):

            if dx > 50:

                self.right_move(
                    None
                )

            elif dx < -50:

                self.left_move(
                    None
                )

        else:

            if dy > 50:

                self.up_move(
                    None
                )

            elif dy < -50:

                self.down_move(
                    None
                )

        return super().on_touch_up(
            touch
        )


# =====================
# APP
# =====================

class SnakeApp(App):

    def build(self):

        return SnakeUI()


SnakeApp().run()
