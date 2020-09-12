import cityflow
eng = cityflow.Engine("test_sim/config.json", thread_num=1)

eng.next_step()
import pdb; pdb.set_trace()
