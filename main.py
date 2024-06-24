from user_info.demographics import Demographics
from user_info.explanation import Explanation
from user_info.stress_eval import stressEvaluation
from experiment.practise import EquationTask
from experiment.between_exp import BetweenExp
from experiment.stress import StressTask
from experiment.meditation import Meditation
from experiment.end_screen import End
from pylsl import StreamInfo, StreamOutlet

def start():
    # ----------------- Experimental setup -----------------
    info = StreamInfo('MyMarkerStream', 'Markers', 1, 0, 'int32', 'myuidw43536')

    outlet = StreamOutlet(info)
    print("now sending markers...")

    # trigger list:
    # 1 - instructions
    # 2 - active blocks
    # 3 - rest blocks
    # 4 - between experiment screen (instructions stress task)
    # 5 - equations shown
    # 6 - countdown
    # 7 - negative feedback
    # 8 - too late feedback
    # 9 - feedback screen
    # 10 - instructions to meditation screen
    # 11 - the end

    Demographics()

    outlet.push_sample([1])
    Explanation()

    EquationTask(outlet)    
    
    outlet.push_sample([4])
    BetweenExp()

    reward = 7
    StressTask(reward, outlet)
    stressEvaluation()

    outlet.push_sample([10])
    Meditation()

    reward = StressTask.reward
    StressTask(reward, outlet)
    stressEvaluation()

    outlet.push_sample([11])
    End()
    

if __name__ == "__main__":
    start()

# TODO: remove "toggle_fullscreen" for actual experiment (expect for "meditation.py")
# TODO: send consent form to lisa
# TODO: sign up for Alice lab eefke/lisa -> make the same as QR for participants