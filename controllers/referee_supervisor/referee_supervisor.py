from supervisor import SoccerSupervisor
from referee import SoccerReferee
from consts import TIMESTEP
import numpy as np
import cv2

supervisor = SoccerSupervisor()
referee = SoccerReferee(supervisor)

while supervisor.step(TIMESTEP) != -1:
    supervisor.send_camera_frame()
    supervisor.refresh_translations()

    if referee.reset_timer == 0:
        referee.check_goal()
    elif referee.reset_timer > 0:
        referee.reset_timer -= TIMESTEP / 1000.0
    else:
        pass

    print(f"Timer: {referee.reset_timer}")