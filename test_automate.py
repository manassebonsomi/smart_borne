from services.state_machine import StateMachine

sm = StateMachine()

print(sm.current_state())

print(sm.transition("START"))

print(sm.transition("PROFILE_OK"))

print(sm.transition("SURVEY_DONE"))

print(sm.transition("ANALYSIS_DONE"))

print(sm.transition("FINISH"))