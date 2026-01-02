import numpy as np

class GridWorld:
    def __init__(self, R1, R2):
        # Grid dimensions (5x5)
        self.rows = 5
        self.cols = 5
        
        # R1 = reward in top-left cell (0,0)
        # R2 = reward in top-right cell (0,4)

        # Rewards matrix
        self.rewards = np.array([
            [R1,   1,   0,  -1,  R2],
            [ 2,   1,   0,  -1,  -2],
            [ 2,   1,   0,  -1,  -2],
            [ 2,   1,   0,  -1,  -2],
            [ 2,   1,   0,  -1,  -2]
        ])
        
        # Discount factor (as specified in requirements)
        self.gamma = 0.95
        
        # Action definitions and mappings
        self.action_names = ["UP", "DOWN", "LEFT", "RIGHT"]
        self.num_actions = 4
        
        # Action vectors (row_change, col_change)
        self.action_vectors = {
            0: (-1, 0),   # UP
            1: (1, 0),    # DOWN
            2: (0, -1),   # LEFT
            3: (0, 1)     # RIGHT
        }
        
        # Transition probabilities
        # Format: {intended_action: {actual_action: probability}}
        self.transition_probs = {
            0: {0: 0.7, 1: 0.1, 2: 0.1, 3: 0.1},  # Intended UP
            1: {1: 0.7, 0: 0.1, 2: 0.1, 3: 0.1},  # Intended DOWN
            2: {2: 0.7, 3: 0.1, 1: 0.1, 0: 0.1},  # Intended LEFT
            3: {3: 0.7, 2: 0.1, 1: 0.1, 0: 0.1}   # Intended RIGHT
        }
    
    # Check if a state (row, col) is within grid boundaries
    def is_valid_state(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    # Calculate the next state given current state and intended action
    def get_next_state(self, row, col, action):
        # Calculate next state
        row_change, col_change = self.action_vectors[action]
        next_row, next_col = row + row_change, col + col_change
        
        # Check for wall collision - stay in current state if invalid
        if not self.is_valid_state(next_row, next_col):
            return (row, col)
        
        return (next_row, next_col)
    
    # Get the probability distribution over next states for a given state and intended action
    def get_transition_distribution(self, row, col, intended_action):
        # Store probability distribution in here
        distribution = {}
        
        # For each possible actual action and its probability
        for actual_action, prob in self.transition_probs[intended_action].items():
            next_row, next_col = self.get_next_state(row, col, actual_action)
            next_state = (next_row, next_col)
            
            # Accumulate probability for this next state
            distribution[next_state] = distribution.get(next_state, 0) + prob
        
        return distribution
    
    # Get the reward for a given state
    def get_reward(self, row, col):
        return self.rewards[row, col]
    
    # Get all possible states in the grid
    def get_all_states(self):
        states = []
        for row in range(self.rows):
            for col in range(self.cols):
                states.append((row, col))
        return states
    
    # Convert (row, col) to a flat index (0-24)
    def get_state_index(self, row, col):
        return row * self.cols + col
    
    # Get (row, col) coordinates from a flat index
    def get_coordinates_from_index(self, index):
        row = index // self.cols
        col = index % self.cols
        return (row, col)
    
    # Print the reward grid
    def print_rewards(self):
        print(f"Reward Grid (R1={self.rewards[0,0]}, R2={self.rewards[0,4]}):")
        for row in range(self.rows):
            print("  ", end="")
            for col in range(self.cols):
                print(f"{self.rewards[row, col]:4}", end=" ")
            print()
    
    # ============ VALUE ITERATION IMPLEMENTATION ============
    
    def value_iteration(self, theta=0.01, max_iterations=1000):
        """
        Implement Value Iteration algorithm.
        
        Based on Bellman Optimality Equation:
        V(s) = max_a [R(s,a) + gamma * sum(P(s'|s,a) * V(s'))]
        
        Args:
            theta: Convergence threshold
            max_iterations: Maximum number of iterations
            
        Returns:
            V: Value function (2D array)
            num_iterations: Number of iterations until convergence
        """
        # Initialize value function to zeros
        V = np.zeros((self.rows, self.cols))
        
        iteration = 0
        
        for iteration in range(max_iterations):
            # Store old value function for convergence check
            V_old = V.copy()
            delta = 0
            
            # Update value for each state
            for row in range(self.rows):
                for col in range(self.cols):
                    # Compute Q-value for each action
                    q_values = []
                    
                    for action in range(self.num_actions):
                        # Get transition distribution for this action
                        transition_dist = self.get_transition_distribution(row, col, action)
                        
                        # Compute expected value: sum over all possible next states
                        q_value = 0
                        for (next_row, next_col), prob in transition_dist.items():
                            # Bellman equation: R + gamma * V(s')
                            reward = self.get_reward(next_row, next_col)
                            q_value += prob * (reward + self.gamma * V_old[next_row, next_col])
                        
                        q_values.append(q_value)
                    
                    # Take maximum over all actions (Bellman Optimality)
                    V[row, col] = max(q_values)
                    
                    # Track maximum change for convergence
                    delta = max(delta, abs(V[row, col] - V_old[row, col]))
            
            # Check for convergence
            if delta < theta:
                print(f"Value Iteration converged after {iteration + 1} iterations")
                break
        
        if iteration == max_iterations - 1:
            print(f"Value Iteration reached maximum iterations ({max_iterations})")
        
        return V, iteration + 1
    
    def extract_policy(self, V):
        """
        Extract the optimal policy from the value function.
        For each state, choose the action with highest Q-value.
        
        Args:
            V: Value function (2D array)
            
        Returns:
            policy: 2D array of optimal actions (0=UP, 1=DOWN, 2=LEFT, 3=RIGHT)
        """
        policy = np.zeros((self.rows, self.cols), dtype=int)
        
        for row in range(self.rows):
            for col in range(self.cols):
                # Compute Q-value for each action
                q_values = []
                
                for action in range(self.num_actions):
                    # Get transition distribution
                    transition_dist = self.get_transition_distribution(row, col, action)
                    
                    # Compute expected value
                    q_value = 0
                    for (next_row, next_col), prob in transition_dist.items():
                        reward = self.get_reward(next_row, next_col)
                        q_value += prob * (reward + self.gamma * V[next_row, next_col])
                    
                    q_values.append(q_value)
                
                # Choose action with maximum Q-value
                policy[row, col] = np.argmax(q_values)
        
        return policy
    
    def display_policy(self, policy):
        """
        Display the policy as a grid with arrows.
        """
        arrow_map = {
            0: "↑",  # UP
            1: "↓",  # DOWN
            2: "←",  # LEFT
            3: "→"   # RIGHT
        }
        
        print("\nOptimal Policy:")
        for row in range(self.rows):
            print("  ", end="")
            for col in range(self.cols):
                print(f"{arrow_map[policy[row, col]]:^4}", end=" ")
            print()
    
    def display_values(self, V):
        """
        Display the value function as a grid.
        """
        print("\nValue Function:")
        for row in range(self.rows):
            print("  ", end="")
            for col in range(self.cols):
                print(f"{V[row, col]:7.2f}", end=" ")
            print()
    
    # ============ BONUS: POLICY ITERATION IMPLEMENTATION ============
    
    def policy_iteration(self, theta=0.01, max_iterations=100):
        """
        BONUS: Policy Iteration Algorithm
        Starts with random policy, alternates between evaluation and improvement
        """
        # Start with random policy
        policy = np.random.randint(0, self.num_actions, size=(self.rows, self.cols))
        
        for iteration in range(max_iterations):
            # Policy Evaluation
            V = np.zeros((self.rows, self.cols))
            while True:
                delta = 0
                V_old = V.copy()
                for row in range(self.rows):
                    for col in range(self.cols):
                        action = policy[row, col]
                        transition_dist = self.get_transition_distribution(row, col, action)
                        v = sum(prob * (self.get_reward(nr, nc) + self.gamma * V_old[nr, nc]) 
                               for (nr, nc), prob in transition_dist.items())
                        V[row, col] = v
                        delta = max(delta, abs(v - V_old[row, col]))
                if delta < theta:
                    break
            
            # Policy Improvement
            policy_stable = True
            new_policy = self.extract_policy(V)
            if not np.array_equal(policy, new_policy):
                policy_stable = False
                policy = new_policy
            
            if policy_stable:
                print(f"Policy Iteration converged after {iteration + 1} iterations")
                return policy, V, iteration + 1
        
        return policy, V, max_iterations


# ============ MAIN EXECUTION FOR ALL TEST CASES ============

def run_experiment(R1, R2):
    """
    Run value iteration for a specific reward configuration.
    """
    print("\n" + "="*60)
    print(f"EXPERIMENT: R1 = {R1}, R2 = {R2}")
    print("="*60)
    
    # Create gridworld
    env = GridWorld(R1, R2)
    env.print_rewards()
    
    # Run value iteration
    print("\nRunning Value Iteration...")
    V, num_iterations = env.value_iteration()
    
    # Extract policy
    policy = env.extract_policy(V)
    
    # Display results
    env.display_values(V)
    env.display_policy(policy)
    
    return V, policy


if __name__ == "__main__":
    # Test cases from assignment
    test_cases = [
        (100, 110),
        (10, 100),
        (1, 10),
        (10, 15)
    ]
    
    print("ASSIGNMENT 4 - VALUE ITERATION")
    print("Discount Factor (gamma) = 0.95")
    
    results = []
    for R1, R2 in test_cases:
        V, policy = run_experiment(R1, R2)
        results.append((R1, R2, V, policy))
    
    # ============ INTUITIVE EXPLANATIONS ============
    print("\n" + "="*60)
    print("INTUITIVE EXPLANATIONS")
    print("="*60)
    
    print("\n1. R1=100, R2=110:")
    print("   Both goals are highly rewarding with R2 slightly better.")
    print("   The agent will prefer paths to R2 (top-right) as it's marginally")
    print("   better, but the difference is small relative to the high values.")
    
    print("\n2. R1=10, R2=100:")
    print("   R2 is significantly more valuable than R1 (10x more).")
    print("   The agent will strongly prefer moving toward R2 (top-right)")
    print("   and avoid R1 unless it's much closer.")
    
    print("\n3. R1=1, R2=10:")
    print("   Similar to case 2 but with smaller absolute values.")
    print("   R2 is 10x more valuable, so the agent will navigate toward")
    print("   R2, though the smaller rewards mean less dramatic preferences.")
    
    print("\n4. R1=10, R2=15:")
    print("   R2 is only 50% more valuable than R1.")
    print("   The agent will prefer R2 but the difference is modest,")
    print("   so proximity matters more - the agent may go to whichever")
    print("   goal is closer or easier to reach.")
    
    print("\n" + "="*60)
    
    # ============ BONUS: POLICY ITERATION ============
    print("\n\n" + "="*60)
    print("BONUS - POLICY ITERATION")
    print("="*60)
    
    for R1, R2 in test_cases:
        print(f"\n>>> R1={R1}, R2={R2}")
        env = GridWorld(R1, R2)
        policy, V, iters = env.policy_iteration()
        env.display_policy(policy)