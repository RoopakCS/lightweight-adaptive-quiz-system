"""
Learner Simulation Module
Simulates learners with different abilities and learning patterns.
"""

import numpy as np


class SimulatedLearner:
    """Simulates a learner with specific ability and learning characteristics."""
    
    def __init__(self, learner_id, base_ability=0.7, learning_rate=0.05,
                 speed_factor=1.0, consistency=0.8):
        """
        Initialize a simulated learner.
        
        Args:
            learner_id: Unique identifier for the learner
            base_ability: Base probability of answering correctly (0-1)
            learning_rate: Rate at which learner improves over time
            speed_factor: Response speed multiplier (1.0 = average)
            consistency: How consistent the learner is (0-1, higher = more consistent)
        """
        self.learner_id = learner_id
        self.base_ability = base_ability
        self.learning_rate = learning_rate
        self.speed_factor = speed_factor
        self.consistency = consistency
        self.questions_answered = 0
        self.current_ability = base_ability
        
    def answer_question(self, question):
        """
        Simulate answering a question.
        
        Args:
            question: Dictionary with question details including difficulty and expected_time
            
        Returns:
            Dictionary with answer results (correct, time)
        """
        difficulty = question.get('difficulty', 'medium')
        expected_time = question.get('expected_time', 30)
        
        # Calculate probability of correct answer based on difficulty and ability
        difficulty_modifiers = {
            'easy': 0.3,    # Easier to answer
            'medium': 0.0,  # No modification
            'hard': -0.3    # Harder to answer
        }
        
        modifier = difficulty_modifiers.get(difficulty, 0.0)
        success_probability = min(max(self.current_ability + modifier, 0.1), 0.95)
        
        # Add consistency factor (random variation)
        if self.consistency < 1.0:
            variation = np.random.normal(0, (1 - self.consistency) * 0.2)
            success_probability = min(max(success_probability + variation, 0.1), 0.95)
        
        # Determine if answer is correct
        correct = np.random.random() < success_probability
        
        # Calculate response time
        time_variation = np.random.normal(1.0, 0.2)
        response_time = expected_time * self.speed_factor * time_variation
        
        # Add penalty time if incorrect (more time spent struggling)
        if not correct:
            response_time *= np.random.uniform(1.1, 1.4)
        
        response_time = max(response_time, 5)  # Minimum 5 seconds
        
        # Update learner state
        self.questions_answered += 1
        self._update_ability(correct, difficulty)
        
        return {
            'correct': correct,
            'time': response_time,
            'expected_time': expected_time,
            'difficulty': difficulty,
            'question_id': question.get('id'),
            'topic': question.get('topic')
        }
    
    def _update_ability(self, correct, difficulty):
        """Update learner's ability based on performance (learning effect)."""
        # Learning happens regardless of correctness, but more when correct
        difficulty_weights = {'easy': 0.5, 'medium': 1.0, 'hard': 1.5}
        weight = difficulty_weights.get(difficulty, 1.0)
        
        if correct:
            # Successful answers increase ability
            improvement = self.learning_rate * weight
        else:
            # Incorrect answers still provide some learning, but less
            improvement = self.learning_rate * weight * 0.3
        
        # Apply improvement with diminishing returns
        self.current_ability = min(self.current_ability + improvement * (1 - self.current_ability), 0.98)
    
    def get_profile(self):
        """Get learner profile information."""
        return {
            'learner_id': self.learner_id,
            'base_ability': self.base_ability,
            'current_ability': self.current_ability,
            'learning_rate': self.learning_rate,
            'speed_factor': self.speed_factor,
            'consistency': self.consistency,
            'questions_answered': self.questions_answered
        }
    
    def reset(self):
        """Reset learner to initial state."""
        self.current_ability = self.base_ability
        self.questions_answered = 0


class LearnerPopulation:
    """Manages a population of diverse simulated learners."""
    
    def __init__(self, num_learners=15):
        """
        Create a diverse population of learners.
        
        Args:
            num_learners: Number of learners to create
        """
        self.learners = self._generate_learners(num_learners)
    
    def _generate_learners(self, num_learners):
        """Generate diverse learner profiles."""
        np.random.seed(42)
        learners = []
        
        # Create learners with varied characteristics
        for i in range(num_learners):
            # Distribute abilities across spectrum
            if i < num_learners // 3:
                # Struggling learners
                base_ability = np.random.uniform(0.3, 0.5)
                learning_rate = np.random.uniform(0.03, 0.07)
            elif i < 2 * num_learners // 3:
                # Average learners
                base_ability = np.random.uniform(0.5, 0.75)
                learning_rate = np.random.uniform(0.04, 0.06)
            else:
                # Advanced learners
                base_ability = np.random.uniform(0.75, 0.9)
                learning_rate = np.random.uniform(0.02, 0.05)
            
            speed_factor = np.random.uniform(0.7, 1.5)
            consistency = np.random.uniform(0.6, 0.95)
            
            learner = SimulatedLearner(
                learner_id=f"learner_{i+1:03d}",
                base_ability=base_ability,
                learning_rate=learning_rate,
                speed_factor=speed_factor,
                consistency=consistency
            )
            learners.append(learner)
        
        return learners
    
    def get_learner(self, learner_id):
        """Get a specific learner by ID."""
        for learner in self.learners:
            if learner.learner_id == learner_id:
                return learner
        return None
    
    def get_all_learners(self):
        """Get all learners."""
        return self.learners
    
    def reset_all(self):
        """Reset all learners to initial state."""
        for learner in self.learners:
            learner.reset()
    
    def get_population_stats(self):
        """Get statistics about the learner population."""
        profiles = [l.get_profile() for l in self.learners]
        
        stats = {
            'total_learners': len(self.learners),
            'avg_base_ability': np.mean([p['base_ability'] for p in profiles]),
            'avg_learning_rate': np.mean([p['learning_rate'] for p in profiles]),
            'avg_speed_factor': np.mean([p['speed_factor'] for p in profiles]),
            'ability_distribution': {
                'struggling': sum(1 for p in profiles if p['base_ability'] < 0.5),
                'average': sum(1 for p in profiles if 0.5 <= p['base_ability'] < 0.75),
                'advanced': sum(1 for p in profiles if p['base_ability'] >= 0.75)
            }
        }
        
        return stats


if __name__ == "__main__":
    # Test learner simulation
    learner = SimulatedLearner("test_001", base_ability=0.6)
    
    # Simulate answering a question
    question = {
        'id': 1,
        'difficulty': 'medium',
        'expected_time': 30,
        'topic': 'Math'
    }
    
    result = learner.answer_question(question)
    print("Answer result:", result)
    print("Learner profile:", learner.get_profile())
    
    # Test population
    print("\n--- Population Test ---")
    population = LearnerPopulation(num_learners=15)
    print("Population stats:", population.get_population_stats())
