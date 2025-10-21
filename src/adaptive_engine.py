"""
Adaptive Engine Module
Implements rule-based logic to adjust quiz difficulty based on learner performance.
"""

import numpy as np


class AdaptiveEngine:
    """Rule-based adaptive quiz engine that adjusts difficulty dynamically."""
    
    DIFFICULTY_LEVELS = ['easy', 'medium', 'hard']
    DIFFICULTY_MAP = {'easy': 1, 'medium': 2, 'hard': 3}
    REVERSE_MAP = {1: 'easy', 2: 'medium', 3: 'hard'}
    
    def __init__(self, accuracy_threshold_high=0.80, accuracy_threshold_low=0.50,
                 time_threshold_factor=1.0, window_size=5):
        """
        Initialize adaptive engine with configurable thresholds.
        
        Args:
            accuracy_threshold_high: Accuracy above which to increase difficulty (default: 0.80)
            accuracy_threshold_low: Accuracy below which to decrease difficulty (default: 0.50)
            time_threshold_factor: Factor for time-based adjustment (default: 1.0)
            window_size: Number of recent questions to consider (default: 5)
        """
        self.accuracy_threshold_high = accuracy_threshold_high
        self.accuracy_threshold_low = accuracy_threshold_low
        self.time_threshold_factor = time_threshold_factor
        self.window_size = window_size
        
    def get_next_difficulty(self, performance_history, current_difficulty='medium'):
        """
        Determine next question difficulty based on recent performance.
        
        Args:
            performance_history: List of recent performance records
                Each record: {'correct': bool, 'time': float, 'expected_time': float}
            current_difficulty: Current difficulty level
            
        Returns:
            Next difficulty level as string
        """
        if not performance_history:
            return current_difficulty
        
        # Consider only recent performance (window)
        recent_performance = performance_history[-self.window_size:]
        
        # Calculate metrics
        accuracy = self._calculate_accuracy(recent_performance)
        avg_time_ratio = self._calculate_time_ratio(recent_performance)
        
        # Get current difficulty level
        current_level = self.DIFFICULTY_MAP.get(current_difficulty, 2)
        
        # Apply adaptive rules
        new_level = current_level
        
        # Rule 1: High accuracy and fast response → increase difficulty
        if accuracy > self.accuracy_threshold_high and avg_time_ratio < self.time_threshold_factor:
            new_level = min(current_level + 1, 3)
            
        # Rule 2: Low accuracy → decrease difficulty
        elif accuracy < self.accuracy_threshold_low:
            new_level = max(current_level - 1, 1)
            
        # Rule 3: High accuracy but slow response → maintain or slight increase
        elif accuracy > self.accuracy_threshold_high and avg_time_ratio >= self.time_threshold_factor:
            # Stay at current level or increase if very accurate
            if accuracy > 0.9:
                new_level = min(current_level + 1, 3)
                
        # Rule 4: Medium accuracy → maintain current level
        # (implicit - no change needed)
        
        return self.REVERSE_MAP[new_level]
    
    def _calculate_accuracy(self, performance_history):
        """Calculate accuracy from performance history."""
        if not performance_history:
            return 0.5
        
        correct_count = sum(1 for p in performance_history if p.get('correct', False))
        return correct_count / len(performance_history)
    
    def _calculate_time_ratio(self, performance_history):
        """
        Calculate average time ratio (actual time / expected time).
        Ratio < 1.0 means faster than expected.
        """
        if not performance_history:
            return 1.0
        
        ratios = []
        for p in performance_history:
            if p.get('expected_time', 0) > 0:
                ratio = p.get('time', 0) / p['expected_time']
                ratios.append(ratio)
        
        return np.mean(ratios) if ratios else 1.0
    
    def get_difficulty_score(self, difficulty):
        """Convert difficulty level to numerical score (1-3)."""
        return self.DIFFICULTY_MAP.get(difficulty, 2)
    
    def calculate_mastery_index(self, performance_history):
        """
        Calculate mastery index: weighted average of (difficulty × accuracy).
        Higher values indicate better mastery of harder content.
        
        Returns:
            Mastery index (0-3 scale)
        """
        if not performance_history:
            return 0.0
        
        total_weighted_score = 0
        total_questions = len(performance_history)
        
        for p in performance_history:
            difficulty_score = self.DIFFICULTY_MAP.get(p.get('difficulty', 'medium'), 2)
            correct = 1 if p.get('correct', False) else 0
            total_weighted_score += difficulty_score * correct
        
        # Normalize to 0-3 scale
        max_possible = total_questions * 3  # All hard questions correct
        mastery_index = (total_weighted_score / max_possible) * 3 if max_possible > 0 else 0
        
        return mastery_index
    
    def get_adaptation_stats(self, performance_history):
        """Get detailed statistics about adaptations."""
        if not performance_history:
            return {}
        
        difficulties = [p.get('difficulty') for p in performance_history]
        difficulty_scores = [self.DIFFICULTY_MAP.get(d, 2) for d in difficulties]
        
        stats = {
            'total_questions': len(performance_history),
            'accuracy': self._calculate_accuracy(performance_history),
            'avg_time_ratio': self._calculate_time_ratio(performance_history),
            'mastery_index': self.calculate_mastery_index(performance_history),
            'avg_difficulty': np.mean(difficulty_scores),
            'difficulty_progression': difficulty_scores,
            'difficulty_changes': self._count_difficulty_changes(difficulty_scores)
        }
        
        return stats
    
    def _count_difficulty_changes(self, difficulty_scores):
        """Count how many times difficulty changed."""
        if len(difficulty_scores) < 2:
            return 0
        
        changes = 0
        for i in range(1, len(difficulty_scores)):
            if difficulty_scores[i] != difficulty_scores[i-1]:
                changes += 1
        
        return changes


class NonAdaptiveEngine:
    """Non-adaptive (static) quiz engine for comparison."""
    
    def __init__(self, fixed_difficulty='medium'):
        """
        Initialize non-adaptive engine.
        
        Args:
            fixed_difficulty: Fixed difficulty level for all questions
        """
        self.fixed_difficulty = fixed_difficulty
    
    def get_next_difficulty(self, performance_history, current_difficulty=None):
        """Always return the fixed difficulty level."""
        return self.fixed_difficulty
    
    def calculate_mastery_index(self, performance_history):
        """Calculate mastery using same formula as adaptive engine."""
        engine = AdaptiveEngine()
        return engine.calculate_mastery_index(performance_history)


if __name__ == "__main__":
    # Test the adaptive engine
    engine = AdaptiveEngine()
    
    # Simulate good performance
    good_performance = [
        {'correct': True, 'time': 15, 'expected_time': 20, 'difficulty': 'easy'},
        {'correct': True, 'time': 18, 'expected_time': 20, 'difficulty': 'easy'},
        {'correct': True, 'time': 16, 'expected_time': 20, 'difficulty': 'easy'},
    ]
    
    next_diff = engine.get_next_difficulty(good_performance, 'easy')
    print(f"After good performance on easy questions, next difficulty: {next_diff}")
    
    # Simulate poor performance
    poor_performance = [
        {'correct': False, 'time': 45, 'expected_time': 40, 'difficulty': 'hard'},
        {'correct': False, 'time': 50, 'expected_time': 40, 'difficulty': 'hard'},
        {'correct': True, 'time': 48, 'expected_time': 40, 'difficulty': 'hard'},
    ]
    
    next_diff = engine.get_next_difficulty(poor_performance, 'hard')
    print(f"After poor performance on hard questions, next difficulty: {next_diff}")
