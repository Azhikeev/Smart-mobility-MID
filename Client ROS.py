import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class FibonacciActionClient(Node):

    def __init__(self):  # Use "__init__" instead of "init"
        super().__init__('fibonacci_action_client')  # Use double underscores for "__init__"
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order
        self._action_client.wait_for_server()
        self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)
        
    def feedback_callback(self, feedback):
        self.get_logger().info('Received feedback: {0}'.format(feedback.feedback.sequence))

def main(args=None):
    rclpy.init(args=args)
    fibonacci_action_client = FibonacciActionClient()
    fibonacci_action_client.send_goal(10)
    rclpy.spin(fibonacci_action_client)
    fibonacci_action_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
