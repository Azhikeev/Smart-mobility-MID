import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from std_msgs.msg import String
from example_interfaces.action import Fibonacci

class FibonacciActionServer(Node):

    def init(self):
        super().init('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]
        for i in range(1, goal_handle.request.order):
            feedback_msg.sequence.append(feedback_msg.sequence[i] + feedback_msg.sequence[i-1])
            self.get_logger().info('Feedback: {0}'.format(feedback_msg.sequence))
            goal_handle.publish_feedback(feedback_msg)
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        return result

def main(args=None):
    rclpy.init(args=args)
    fibonacci_action_server = FibonacciActionServer()
    rclpy.spin(fibonacci_action_server)
    fibonacci_action_server.destroy_node()
    rclpy.shutdown()

if name == 'main':
    main()
