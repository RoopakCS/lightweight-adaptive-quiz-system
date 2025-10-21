"""
Question Bank Module
Creates and manages a synthetic question bank with difficulty levels and topics.
"""

import pandas as pd
import numpy as np


class QuestionBank:
    """Manages the question database with difficulty levels and topics."""
    
    DIFFICULTY_LEVELS = ['easy', 'medium', 'hard']
    TOPICS = ['Math', 'Science', 'History', 'Literature', 'Geography']
    
    def __init__(self, num_questions=100):
        """
        Initialize question bank with synthetic questions.
        
        Args:
            num_questions: Total number of questions to generate
        """
        self.questions = self._generate_questions(num_questions)
        
    def _generate_questions(self, num_questions):
        """Generate synthetic question bank."""
        np.random.seed(42)
        
        questions = []
        for i in range(num_questions):
            question = {
                'id': i + 1,
                'topic': np.random.choice(self.TOPICS),
                'difficulty': np.random.choice(self.DIFFICULTY_LEVELS),
                'text': f"Question {i + 1}",
                'correct_answer': np.random.choice(['A', 'B', 'C', 'D']),
                # Expected time to answer (in seconds) based on difficulty
                'expected_time': self._get_expected_time(self.DIFFICULTY_LEVELS[i % 3])
            }
            questions.append(question)
        
        # Balance difficulty distribution
        df = pd.DataFrame(questions)
        df['difficulty'] = pd.Categorical(
            np.tile(self.DIFFICULTY_LEVELS, len(df) // 3 + 1)[:len(df)],
            categories=self.DIFFICULTY_LEVELS,
            ordered=True
        )
        
        return df.to_dict('records')
    
    def _get_expected_time(self, difficulty):
        """Get expected time to answer based on difficulty."""
        time_map = {
            'easy': np.random.uniform(10, 20),
            'medium': np.random.uniform(20, 40),
            'hard': np.random.uniform(40, 60)
        }
        return time_map.get(difficulty, 30)
    
    def get_question(self, difficulty=None, topic=None):
        """
        Get a random question based on criteria.
        
        Args:
            difficulty: Filter by difficulty level
            topic: Filter by topic
            
        Returns:
            Dictionary containing question details
        """
        filtered = self.questions.copy()
        
        if difficulty:
            filtered = [q for q in filtered if q['difficulty'] == difficulty]
        if topic:
            filtered = [q for q in filtered if q['topic'] == topic]
        
        if not filtered:
            filtered = self.questions
        
        return np.random.choice(filtered)
    
    def get_questions_by_difficulty(self, difficulty):
        """Get all questions of a specific difficulty."""
        return [q for q in self.questions if q['difficulty'] == difficulty]
    
    def get_statistics(self):
        """Get statistics about the question bank."""
        df = pd.DataFrame(self.questions)
        stats = {
            'total_questions': len(self.questions),
            'by_difficulty': df['difficulty'].value_counts().to_dict(),
            'by_topic': df['topic'].value_counts().to_dict(),
            'avg_expected_time': df.groupby('difficulty')['expected_time'].mean().to_dict()
        }
        return stats
    
    def export_to_csv(self, filepath='data/question_bank.csv'):
        """Export question bank to CSV file."""
        df = pd.DataFrame(self.questions)
        df.to_csv(filepath, index=False)
        print(f"Question bank exported to {filepath}")


if __name__ == "__main__":
    # Test the question bank
    qb = QuestionBank(num_questions=90)
    print("Question Bank Statistics:")
    print(qb.get_statistics())
    print("\nSample Easy Question:")
    print(qb.get_question(difficulty='easy'))
