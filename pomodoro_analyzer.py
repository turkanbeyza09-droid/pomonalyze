# -*- coding: utf-8 -*-
import random
from datetime import datetime

class PomodoroAnalyzer:
    def __init__(self, default_work_time=25):
        self.default_work_time = default_work_time
        self.history = []

    def _calculate_productivity(self, target_duration, actual_duration):
        if actual_duration <= target_duration:
            return 1.0
        else:
            return target_duration / actual_duration

    def start_work_session(self, target_duration, actual_duration_minutes):
        productivity = self._calculate_productivity(target_duration, actual_duration_minutes)
        session_data = {
            'hedef_sure': target_duration,
            'gercek_sure': round(actual_duration_minutes, 2),
            'verimlilik_skoru': round(productivity, 2),
            'tarih': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(session_data)
        return productivity

    def analyze_and_suggest_time(self):
        if not self.history:
            return self.default_work_time

        recent_sessions = self.history[-5:] 
        total_productivity = sum([s['verimlilik_skoru'] for s in recent_sessions])
        avg_productivity = total_productivity / len(recent_sessions)
        
        current_target = recent_sessions[-1]['hedef_sure']
        new_target = current_target
        
        if avg_productivity >= 0.9:
            increase = random.randint(2, 5)
            new_target = current_target + increase
        elif avg_productivity < 0.7:
            decrease = random.randint(2, 5)
            new_target = max(5, current_target - decrease) 

        return int(new_target)