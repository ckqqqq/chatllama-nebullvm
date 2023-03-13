import json
import os
from beartype import beartype
from plotly import graph_objects as go


class TrainingStats:
    """Training statistics

    Attributes:
        training_loss (List): List of training losses
        training_accuracy (List): List of training accuracies
        value_loss (List): List of value losses
        validation_loss (List): List of validation losses
        validation_accuracy (List): List of validation accuracies
    """

    def __init__(self):
        self.training_loss = []
        self.training_accuracy = []
        self.value_loss = []
        self.validation_loss = []
        self.validation_accuracy = []

    def plot(self):
        """Plot the training statistics using plotly"""
        fig = go.Figure()
        if len(self.training_loss) > 0:
            fig.add_trace(
                go.Scatter(y=self.training_loss, name="Training loss")
            )
        if len(self.training_accuracy) > 0:
            fig.add_trace(
                go.Scatter(y=self.training_accuracy, name="Training accuracy")
            )
        if len(self.value_loss) > 0:
            fig.add_trace(go.Scatter(y=self.value_loss, name="Value loss"))
        if len(self.validation_loss) > 0:
            fig.add_trace(
                go.Scatter(y=self.validation_loss, name="Validation loss")
            )
        if len(self.validation_accuracy) > 0:
            fig.add_trace(
                go.Scatter(
                    y=self.validation_accuracy, name="Validation accuracy"
                )
            )
        fig.update_layout(
            showlegend=True, xaxis_type="log", xaxis_title="steps"
        )
        fig.show()


class ConversationLog:
    """Save the conversation:
    (user input, model output, rewards and learn_counter)
    during the RL training loop.
    """

    def __init__(self, path: str):
        self.conversation = []
        self.path = path
        if self.path is None:
            self.path = "./convesation_log.json"

    @beartype
    def append(
        self,
        user_input: str,
        model_output: str,
        reward: float,
        learn_counter: int,
    ):
        """Add a conversation to the log

        Args:
            user_input (str): User input / initial prompt
            model_output (str): Completion of the LLM model
            reward (float): Reward of the reward model assigned to the output
            learn_counter (int): Number of the learning iteration to
                distinguish the conversations that happens at different
                points of the training loopt
        """
        self.conversation.append(
            {
                "user_input": user_input,
                "model_output": model_output,
                "reward": reward,
                "learn_counter": learn_counter,
            }
        )

    def save(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                conversation = json.load(f)
            self.conversation.extend(conversation)
        with open(self.path, "w") as f:
            json.dump(self.conversation, f)

    def load(self):
        with open(self.path, "r") as f:
            self.conversation = json.load(f)

    def clear(self):
        print("Clearing conversations log")
        self.conversation = []
        # remove the file in path exists
        if os.path.exists(self.path):
            os.remove(self.path)

    def show(self, current_iteration: int = None):
        """Show the conversation log

        Args:
            current_iteration (int): Current iteration of the training loop,
                if not None, print only the conversations that happened at
                <current_iteration>
        """
        for i, c in enumerate(self.conversation):
            if current_iteration is None:
                print(
                    f"##########################################\n"
                    f"Conversation {i} at learn_counter "
                    f"{c['learn_counter']}\n"
                    f"##########################################\n"
                    f"## User Input:\n\n{c['user_input']}\n\n"
                    f"## Model Output:\n\n{c['model_output']}\n\n"
                    f"## Reward: {c['reward']}\n\n"
                )
            else:
                if current_iteration == c["learn_counter"]:
                    print(
                        f"##########################################\n"
                        f"Conversation {i} at learn_counter "
                        f"{c['learn_counter']}\n"
                        f"##########################################\n"
                        f"## User Input:\n\n{c['user_input']}\n\n"
                        f"## Model Output:\n\n{c['model_output']}\n\n"
                        f"## Reward: {c['reward']}\n\n"
                    )
