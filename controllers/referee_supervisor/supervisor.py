from controller import Supervisor
from consts import TIMESTEP

class SoccerSupervisor(Supervisor):
    """SoccerSupervisor is in charge of simulation related tasks. Logic can be found in referee."""

    def __init__(self):
        super().__init__()

        self.camera = self.getDevice("camera")
        self.emitter = self.getDevice("emitter")

        self.ball = self.getFromDef("BALL")
        self.ball_translation_field = self.ball.getField("translation")
        self.ball_translation = self.ball_translation_field.getSFVec3f()

        self.draw = True

        self.camera.enable(TIMESTEP)

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
            str(team_a_score),
            0.92,  # X position
            0.01,  # Y position
            0.1,  # Size
            0x0000FF,  # Color
            0.0,  # Transparency
            "Tahoma",  # Font
        )
        self.setLabel(
            2, # ID
            str(team_b_score),
            0.05,  # X position
            0.01,  # Y position
            0.1,  # Size
            0xFFFF00,  # Color
            0.0,  # Transparency
            "Tahoma",  # Font
        )