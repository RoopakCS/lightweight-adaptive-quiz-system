"""
Main execution script for Lightweight Adaptive Quiz System (LAQS)
Runs complete simulation and generates all results.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.question_bank import QuestionBank
from src.adaptive_engine import AdaptiveEngine, NonAdaptiveEngine
from src.learner_simulation import LearnerPopulation
from src.quiz_simulation import ExperimentRunner
from src.visualization import VisualizationEngine
from src.analysis import StatisticalAnalyzer


def create_directories():
    """Create necessary output directories."""
    directories = ['data', 'results']
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True, parents=True)
    print("Output directories created.")


def run_full_simulation(num_learners=15, num_sessions=5, num_questions=20):
    """
    Run the complete LAQS simulation.
    
    Args:
        num_learners: Number of simulated learners
        num_sessions: Number of quiz sessions per learner per type
        num_questions: Number of questions per session
    """
    print("\n" + "=" * 80)
    print("LIGHTWEIGHT ADAPTIVE QUIZ SYSTEM (LAQS) - FULL SIMULATION")
    print("=" * 80)
    
    # Create output directories
    create_directories()
    
    # Initialize components
    print("\n[1/6] Initializing system components...")
    question_bank = QuestionBank(num_questions=100)
    learner_population = LearnerPopulation(num_learners=num_learners)
    experiment_runner = ExperimentRunner(
        question_bank=question_bank,
        num_questions_per_session=num_questions
    )
    
    print(f"  ✓ Question bank created: {len(question_bank.questions)} questions")
    print(f"  ✓ Learner population created: {num_learners} learners")
    print(f"  ✓ Experiment runner initialized")
    
    # Display population statistics
    pop_stats = learner_population.get_population_stats()
    print(f"\n  Learner Distribution:")
    print(f"    - Struggling (ability < 0.5): {pop_stats['ability_distribution']['struggling']}")
    print(f"    - Average (0.5 ≤ ability < 0.75): {pop_stats['ability_distribution']['average']}")
    print(f"    - Advanced (ability ≥ 0.75): {pop_stats['ability_distribution']['advanced']}")
    
    # Run experiment
    print(f"\n[2/6] Running simulation...")
    print(f"  Configuration:")
    print(f"    - Learners: {num_learners}")
    print(f"    - Sessions per type: {num_sessions}")
    print(f"    - Questions per session: {num_questions}")
    print(f"    - Total sessions: {num_learners * num_sessions * 2}")
    print()
    
    results = experiment_runner.run_population_experiment(
        learner_population,
        num_sessions=num_sessions
    )
    
    print(f"\n  ✓ Simulation completed successfully!")
    
    # Get tracker
    tracker = experiment_runner.get_tracker()
    
    # Export raw data
    print("\n[3/6] Exporting raw data...")
    experiment_runner.export_results('data')
    question_bank.export_to_csv('data/question_bank.csv')
    print("  ✓ Data exported to 'data/' directory")
    
    # Statistical analysis
    print("\n[4/6] Performing statistical analysis...")
    analyzer = StatisticalAnalyzer(tracker)
    analyzer.print_summary()
    report_path = analyzer.generate_report('results/statistical_report.txt')
    print(f"  ✓ Full report saved: {report_path}")
    
    # Generate visualizations
    print("\n[5/6] Generating visualizations...")
    visualizer = VisualizationEngine(output_dir='results')
    visualizer.generate_all_plots(tracker)
    
    # Summary
    print("\n[6/6] Generating final summary...")
    comparison_stats = tracker.get_comparison_stats()
    
    print("\n" + "=" * 80)
    print("SIMULATION RESULTS SUMMARY")
    print("=" * 80)
    
    if comparison_stats:
        print("\nKEY FINDINGS:")
        print(f"\n  Accuracy:")
        print(f"    Adaptive:     {comparison_stats['adaptive']['mean_accuracy']:.2%}")
        print(f"    Non-Adaptive: {comparison_stats['non_adaptive']['mean_accuracy']:.2%}")
        print(f"    Improvement:  {comparison_stats.get('accuracy_improvement', 0):+.2f}%")
        
        print(f"\n  Mastery Index:")
        print(f"    Adaptive:     {comparison_stats['adaptive']['mean_mastery']:.3f}")
        print(f"    Non-Adaptive: {comparison_stats['non_adaptive']['mean_mastery']:.3f}")
        print(f"    Improvement:  {comparison_stats.get('mastery_improvement', 0):+.2f}%")
        
        print(f"\n  Average Time per Question:")
        print(f"    Adaptive:     {comparison_stats['adaptive']['mean_time_per_question']:.2f} seconds")
        print(f"    Non-Adaptive: {comparison_stats['non_adaptive']['mean_time_per_question']:.2f} seconds")
        
        print(f"\n  Difficulty Adaptations:")
        print(f"    Avg changes per session: {comparison_stats['adaptive']['mean_difficulty_changes']:.1f}")
    
    print("\n" + "=" * 80)
    print("CONCLUSION:")
    print("=" * 80)
    
    if comparison_stats.get('accuracy_improvement', 0) > 0 and comparison_stats.get('mastery_improvement', 0) > 0:
        print("""
The adaptive quiz system demonstrates superior performance compared to the
non-adaptive (static) approach. Key benefits include:

  ✓ Higher accuracy scores
  ✓ Improved mastery of content
  ✓ Dynamic difficulty adjustment based on learner performance
  ✓ Better learning efficiency

The rule-based adaptive engine successfully tailors quiz difficulty to
individual learner needs, providing evidence that adaptive assessment can
improve learning outcomes even in lightweight, offline-capable systems.
        """)
    else:
        print("""
The simulation has completed. Please review the detailed statistical report
and visualizations for comprehensive analysis of the results.
        """)
    
    print("=" * 80)
    print("\nOUTPUT FILES:")
    print("  Data:          data/session_results.csv, data/question_responses.csv")
    print("  Report:        results/statistical_report.txt")
    print("  Visualizations: results/*.png")
    print("\n" + "=" * 80 + "\n")


def run_quick_demo():
    """Run a quick demonstration with fewer learners."""
    print("\n🎯 Running QUICK DEMO (5 learners, 3 sessions, 15 questions)")
    print("For full simulation, run: python main.py --full\n")
    run_full_simulation(num_learners=5, num_sessions=3, num_questions=15)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Lightweight Adaptive Quiz System (LAQS) Simulation'
    )
    parser.add_argument(
        '--full',
        action='store_true',
        help='Run full simulation (15 learners, 5 sessions, 20 questions)'
    )
    parser.add_argument(
        '--learners',
        type=int,
        default=None,
        help='Number of simulated learners'
    )
    parser.add_argument(
        '--sessions',
        type=int,
        default=None,
        help='Number of sessions per learner per quiz type'
    )
    parser.add_argument(
        '--questions',
        type=int,
        default=None,
        help='Number of questions per session'
    )
    
    args = parser.parse_args()
    
    if args.full:
        # Full simulation
        num_learners = args.learners or 15
        num_sessions = args.sessions or 5
        num_questions = args.questions or 20
        print(f"\n🚀 Running FULL SIMULATION")
        run_full_simulation(num_learners, num_sessions, num_questions)
    elif args.learners or args.sessions or args.questions:
        # Custom parameters
        num_learners = args.learners or 5
        num_sessions = args.sessions or 3
        num_questions = args.questions or 15
        print(f"\n⚙️ Running CUSTOM SIMULATION")
        run_full_simulation(num_learners, num_sessions, num_questions)
    else:
        # Quick demo
        run_quick_demo()


if __name__ == "__main__":
    main()
