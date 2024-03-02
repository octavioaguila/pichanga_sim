from consts import (TEAM_B_GOAL_X_RANGE, TEAM_B_GOAL_Y_RANGE,
                    POST_GOAL_WAIT_TIME, TEAM_A_GOAL_X_RANGE,
                    TEAM_A_GOAL_Y_RANGE)


class SoccerReferee:

    def __init__(self, supervisor) -> None:
        self.supervisor = supervisor
        self.team_a_score = 0
        self.team_b_score = 0
        self.reset_timer = 0

    def check_goal(self):
        x_translation, y_translation, z_translation = self.supervisor.ball_translation

        if TEAM_B_GOAL_X_RANGE[0] < x_translation < TEAM_B_GOAL_X_RANGE[1]:
            if TEAM_B_GOAL_Y_RANGE[0] > y_translation > TEAM_B_GOAL_Y_RANGE[1]:
                self.team_a_score += 1
                self.supervisor.draw_score(self.team_a_score, self.team_b_score)
                self.supervisor.draw_goal_message(0.0)
                self.reset_timer = POST_GOAL_WAIT_TIME
                return
        
        if TEAM_A_GOAL_X_RANGE[0] < x_translation < TEAM_A_GOAL_X_RANGE[1]:
            if TEAM_A_GOAL_Y_RANGE[0] < y_translation < TEAM_A_GOAL_Y_RANGE[1]:
                self.team_b_score += 1
                self.supervisor.draw_score(self.team_a_score, self.team_b_score)
                self.supervisor.draw_goal_message(0.0)
                self.reset_timer = POST_GOAL_WAIT_TIME
                return



