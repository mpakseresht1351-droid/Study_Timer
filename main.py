"""
Study Timer with Minutes and Full History
For Pydroid 3
Developed by Argash
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from datetime import datetime
import json
import os

# Full screen
Window.fullscreen = True

class TimerApp(App):
    def build(self):
        # Main layout with purple background
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Set purple background
        with main_layout.canvas.before:
            Color(0.15, 0.02, 0.3, 1)
            self.bg_rect = Rectangle(pos=main_layout.pos, size=main_layout.size)
        
        main_layout.bind(pos=self.update_bg, size=self.update_bg)
        
        # Title
        title = Label(
            text='STUDY TIMER',
            font_size=38,
            size_hint=(1, 0.08),
            color=(1, 1, 1, 1),
            bold=True
        )
        main_layout.add_widget(title)
        
        # Subtitle
        subtitle = Label(
            text='by Argash',
            font_size=14,
            size_hint=(1, 0.04),
            color=(0.7, 0.5, 1, 0.8)
        )
        main_layout.add_widget(subtitle)
        
        # Time selection
        time_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        time_layout.add_widget(Label(
            text='Hours:',
            font_size=22,
            color=(1, 1, 1, 0.9),
            size_hint=(0.2, 1)
        ))
        self.hour_spinner = Spinner(
            text='1',
            values=[str(i) for i in range(0, 5)],
            font_size=22,
            size_hint=(0.25, 1),
            background_color=(0.3, 0.1, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        time_layout.add_widget(self.hour_spinner)
        
        time_layout.add_widget(Label(
            text='Min:',
            font_size=22,
            color=(1, 1, 1, 0.9),
            size_hint=(0.15, 1)
        ))
        self.min_spinner = Spinner(
            text='0',
            values=[str(i) for i in range(0, 60, 5)],
            font_size=22,
            size_hint=(0.25, 1),
            background_color=(0.3, 0.1, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        time_layout.add_widget(self.min_spinner)
        main_layout.add_widget(time_layout)
        
        # Timer display
        self.timer_display = Label(
            text='01:00:00',
            font_size=120,
            size_hint=(1, 0.35),
            color=(0.3, 1, 0.9, 1),
            bold=True
        )
        main_layout.add_widget(self.timer_display)
        
        # Buttons
        btn_layout = BoxLayout(size_hint=(1, 0.09), spacing=10)
        
        self.start_btn = Button(
            text='START',
            font_size=18,
            background_color=(0, 0.6, 0, 1),
            color=(1, 1, 1, 1)
        )
        self.start_btn.bind(on_press=self.start_timer)
        btn_layout.add_widget(self.start_btn)
        
        self.stop_btn = Button(
            text='STOP',
            font_size=18,
            background_color=(0.6, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        self.stop_btn.bind(on_press=self.stop_timer)
        btn_layout.add_widget(self.stop_btn)
        
        self.reset_btn = Button(
            text='RESET',
            font_size=18,
            background_color=(0, 0, 0.6, 1),
            color=(1, 1, 1, 1)
        )
        self.reset_btn.bind(on_press=self.reset_timer)
        btn_layout.add_widget(self.reset_btn)
        main_layout.add_widget(btn_layout)
        
        # Save button
        self.save_btn = Button(
            text='SAVE SESSION',
            font_size=18,
            size_hint=(1, 0.07),
            background_color=(0.5, 0.1, 0.7, 1),
            color=(1, 1, 1, 1)
        )
        self.save_btn.bind(on_press=self.save_session)
        main_layout.add_widget(self.save_btn)
        
        # Statistics - Current
        main_layout.add_widget(Label(
            text='CURRENT STATISTICS',
            font_size=18,
            size_hint=(1, 0.04),
            color=(0.7, 0.5, 1, 1)
        ))
        
        # Stats grid
        stats_grid = BoxLayout(size_hint=(1, 0.12), spacing=5)
        
        self.stats_labels = {}
        stats_names = ['Day', 'Week', 'Month', 'Year']
        
        for name in stats_names:
            stat_box = BoxLayout(orientation='vertical', spacing=2)
            stat_box.add_widget(Label(
                text=name,
                font_size=14,
                color=(0.8, 0.8, 1, 0.8),
                halign='center'
            ))
            self.stats_labels[name] = Label(
                text='0.0h',
                font_size=22,
                bold=True,
                color=(0.3, 1, 0.8, 1),
                halign='center'
            )
            stat_box.add_widget(self.stats_labels[name])
            stats_grid.add_widget(stat_box)
        
        main_layout.add_widget(stats_grid)
        
        # History button
        history_btn = Button(
            text='📊 VIEW FULL HISTORY',
            font_size=16,
            size_hint=(1, 0.06),
            background_color=(0.3, 0.1, 0.6, 1),
            color=(1, 1, 1, 1)
        )
        history_btn.bind(on_press=self.show_history)
        main_layout.add_widget(history_btn)
        
        # Delete stats button
        delete_btn = Button(
            text='DELETE ALL STATS',
            font_size=14,
            size_hint=(1, 0.05),
            background_color=(0.5, 0, 0, 0.8),
            color=(1, 1, 1, 1)
        )
        delete_btn.bind(on_press=self.reset_stats)
        main_layout.add_widget(delete_btn)
        
        # Footer
        footer = Label(
            text='Developed by Argash © 2026',
            font_size=11,
            size_hint=(1, 0.03),
            color=(0.5, 0.3, 0.7, 0.6)
        )
        main_layout.add_widget(footer)
        
        # Load data
        self.load_data()
        self.update_stats()
        
        # Timer variables
        self.total_seconds = 3600
        self.time_left = 3600
        self.running = False
        self.timer_event = None
        
        self.update_display()
        
        return main_layout
    
    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def start_timer(self, instance):
        if self.running:
            return
        
        hours = int(self.hour_spinner.text)
        minutes = int(self.min_spinner.text)
        self.total_seconds = hours * 3600 + minutes * 60
        self.time_left = self.total_seconds
        self.update_display()
        self.running = True
        self.start_btn.text = 'RUNNING'
        self.start_btn.background_color = (0.6, 0.6, 0, 1)
        self.timer_event = Clock.schedule_interval(self.tick, 1)
    
    def tick(self, dt):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_display()
        else:
            self.stop_timer(None)
            self.timer_display.color = (1, 0.3, 0.3, 1)
            Clock.schedule_once(lambda dt: setattr(self.timer_display, 'color', (0.3, 1, 0.9, 1)), 2)
    
    def update_display(self):
        hours = self.time_left // 3600
        minutes = (self.time_left % 3600) // 60
        seconds = self.time_left % 60
        self.timer_display.text = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    
    def stop_timer(self, instance):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        self.running = False
        self.start_btn.text = 'START'
        self.start_btn.background_color = (0, 0.6, 0, 1)
    
    def reset_timer(self, instance):
        self.stop_timer(None)
        hours = int(self.hour_spinner.text)
        minutes = int(self.min_spinner.text)
        self.total_seconds = hours * 3600 + minutes * 60
        self.time_left = self.total_seconds
        self.update_display()
    
    def save_session(self, instance):
        if self.time_left <= 0:
            return
        
        elapsed = self.total_seconds - self.time_left
        if elapsed < 60:
            return
        
        today = datetime.now().strftime('%Y-%m-%d')
        elapsed_hours = elapsed / 3600
        
        if today not in self.data['daily']:
            self.data['daily'][today] = 0
        self.data['daily'][today] += elapsed_hours
        
        week = datetime.now().strftime('%Y-W%W')
        if week not in self.data['weekly']:
            self.data['weekly'][week] = 0
        self.data['weekly'][week] += elapsed_hours
        
        month = datetime.now().strftime('%Y-%m')
        if month not in self.data['monthly']:
            self.data['monthly'][month] = 0
        self.data['monthly'][month] += elapsed_hours
        
        year = datetime.now().strftime('%Y')
        if year not in self.data['yearly']:
            self.data['yearly'][year] = 0
        self.data['yearly'][year] += elapsed_hours
        
        self.save_data()
        self.update_stats()
        self.reset_timer(None)
    
    def update_stats(self):
        today = datetime.now().strftime('%Y-%m-%d')
        week = datetime.now().strftime('%Y-W%W')
        month = datetime.now().strftime('%Y-%m')
        year = datetime.now().strftime('%Y')
        
        self.stats_labels['Day'].text = f'{self.data["daily"].get(today, 0):.1f}h'
        self.stats_labels['Week'].text = f'{self.data["weekly"].get(week, 0):.1f}h'
        self.stats_labels['Month'].text = f'{self.data["monthly"].get(month, 0):.1f}h'
        self.stats_labels['Year'].text = f'{self.data["yearly"].get(year, 0):.1f}h'
    
    def show_history(self, instance):
        # Create popup content
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        popup_layout.add_widget(Label(
            text='📊 STUDY HISTORY',
            font_size=24,
            color=(0.8, 0.5, 1, 1),
            size_hint=(1, 0.06),
            bold=True
        ))
        
        # Scrollable content
        scroll = ScrollView(size_hint=(1, 0.88))
        history_content = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        history_content.bind(minimum_height=history_content.setter('height'))
        
        # Add daily history
        history_content.add_widget(Label(
            text='━━━ DAILY ━━━',
            font_size=18,
            color=(0.5, 0.8, 1, 1),
            size_hint_y=None,
            height=30
        ))
        
        if self.data['daily']:
            for date, hours in sorted(self.data['daily'].items(), reverse=True):
                history_content.add_widget(Label(
                    text=f'{date}:  {hours:.1f} hours',
                    font_size=16,
                    color=(1, 1, 1, 0.9),
                    size_hint_y=None,
                    height=25
                ))
        else:
            history_content.add_widget(Label(
                text='No daily data yet',
                font_size=16,
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=25
            ))
        
        # Add weekly history
        history_content.add_widget(Label(
            text='\n━━━ WEEKLY ━━━',
            font_size=18,
            color=(0.5, 0.8, 1, 1),
            size_hint_y=None,
            height=30
        ))
        
        if self.data['weekly']:
            for week, hours in sorted(self.data['weekly'].items(), reverse=True):
                history_content.add_widget(Label(
                    text=f'{week}:  {hours:.1f} hours',
                    font_size=16,
                    color=(1, 1, 1, 0.9),
                    size_hint_y=None,
                    height=25
                ))
        else:
            history_content.add_widget(Label(
                text='No weekly data yet',
                font_size=16,
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=25
            ))
        
        # Add monthly history
        history_content.add_widget(Label(
            text='\n━━━ MONTHLY ━━━',
            font_size=18,
            color=(0.5, 0.8, 1, 1),
            size_hint_y=None,
            height=30
        ))
        
        if self.data['monthly']:
            for month, hours in sorted(self.data['monthly'].items(), reverse=True):
                history_content.add_widget(Label(
                    text=f'{month}:  {hours:.1f} hours',
                    font_size=16,
                    color=(1, 1, 1, 0.9),
                    size_hint_y=None,
                    height=25
                ))
        else:
            history_content.add_widget(Label(
                text='No monthly data yet',
                font_size=16,
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=25
            ))
        
        # Add yearly history
        history_content.add_widget(Label(
            text='\n━━━ YEARLY ━━━',
            font_size=18,
            color=(0.5, 0.8, 1, 1),
            size_hint_y=None,
            height=30
        ))
        
        if self.data['yearly']:
            for year, hours in sorted(self.data['yearly'].items(), reverse=True):
                history_content.add_widget(Label(
                    text=f'{year}:  {hours:.1f} hours',
                    font_size=16,
                    color=(1, 1, 1, 0.9),
                    size_hint_y=None,
                    height=25
                ))
        else:
            history_content.add_widget(Label(
                text='No yearly data yet',
                font_size=16,
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=25
            ))
        
        scroll.add_widget(history_content)
        popup_layout.add_widget(scroll)
        
        # Close button
        close_btn = Button(
            text='CLOSE',
            font_size=18,
            size_hint=(1, 0.06),
            background_color=(0.4, 0.1, 0.6, 1),
            color=(1, 1, 1, 1)
        )
        popup_layout.add_widget(close_btn)
        
        # Create and open popup
        popup = Popup(
            title='',
            content=popup_layout,
            size_hint=(0.9, 0.85),
            auto_dismiss=False,
            background_color=(0.1, 0.02, 0.2, 0.95)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def reset_stats(self, instance):
        self.data = {'daily': {}, 'weekly': {}, 'monthly': {}, 'yearly': {}}
        self.save_data()
        self.update_stats()
    
    def load_data(self):
        filename = 'study_data.json'
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    self.data = json.load(f)
                return
            except:
                pass
        self.data = {'daily': {}, 'weekly': {}, 'monthly': {}, 'yearly': {}}
    
    def save_data(self):
        with open('study_data.json', 'w') as f:
            json.dump(self.data, f, indent=2)

if __name__ == '__main__':
    TimerApp().run()
