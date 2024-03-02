from controller import Supervisor
from consts import TIMESTEP, TEAM_A_STARTING_POSITION, BALL_STARTING_POSITION

class SoccerSupervisor(Supervisor):
    """SoccerSupervisor is in charge of simulation related tasks. Logic can be found in referee."""

    def __init__(self):
        super().__init__()

        self.camera = self.getDevice("camera")
        self.camera.enable(TIMESTEP)

        self.emitter = self.getDevice("emitter")

        self.ball = self.getFromDef("BALL")
        self.ball_translation_field = self.ball.getField("translation")
        self.ball_translation = self.ball_translation_field.getSFVec3f()

        self.a_robot = self.getFromDef("A")
        self.a_robot_translation_field = self.a_robot.getField("translation")

        self.draw_score(0, 0)


    def send_camera_frame(self):
        img_data = self.camera.getImage()
        self.emitter.send(img_data)

        # width = self.camera.getWidth()
        # height = self.camera.getHeight()
        # img = np.frombuffer(img_data, dtype=np.uint8)
        # img = np.reshape(img, (640, 640, 4))
        # cv2.imshow('Image from Supervisor', img)
        # cv2.waitKey(1)

    def refresh_translations(self):
        self.ball_translation = self.ball_translation_field.getSFVec3f()
    
    def draw_score(self, team_a_score, team_b_score):

        self.setLabel(
            1, # ID
            "Blue Team Score\n" + " "*10 +f"{team_a_score}",
            0.05,  # X position
            0.01,  # Y position
            0.11,  # Size
            0x0000FF,  # Color
            0.0,  # Transparency
            "Tahoma",  # Font
        )
        self.setLabel(
            2, # ID
            "Purple Team Score\n" + " "*12 +f"{team_b_score}",
            0.77,  # X position
            0.01,  # Y position
            0.11,  # Size
            0x81007F,  # Color
            0.0,  # Transparency
            "Tahoma",  # Font
        )
    
    def draw_goal_message(self, transparency):
        
        self.setLabel(
            3, # ID
            "GOLAZO",
            0.3,  # X position
            0.4,  # Y position
            0.3,  # Size
            0x000000,  # Color
            transparency,  # Transparency
            "Verdana",  # Font
        )

    def move_robots_to_start(self):
        
        self.a_robot_translation_field.setSFVec3f(TEAM_A_STARTING_POSITION)
        
        self.ball_translation_field.setSFVec3f(BALL_STARTING_POSITION)
        self.ball.setVelocity([0, 0, 0, 0, 0, 0])
        self.ball.resetPhysics()