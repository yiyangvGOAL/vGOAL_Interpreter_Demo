import Interpreter_V2 as DG
import time

start = time.time()

def main():
    knowledge_base =["forall p. dropped(p) implies delivered(p)",
                     "at(6) implies located(charging)",
                     "at(7) implies located(charging)",
                     "at(8) implies located(charging)",
                     "battery(1) implies safe1",
                     "battery(2) implies safe1",
                     "exists p. at(p) and not at(9) implies safe2",
                     #Error implication
                     "E1 implies nonfatal",
                     "E2 implies nonfatal",
                     "E3 implies nonfatal",
                     "E4 implies fatal",
                     "equal(1,1)",
                     "equal(2,2)",
                     "equal(3,3)",
                     "equal(4,4)",
                     "equal(5,5)",
                     "equal(6,6)",
                     "equal(7,7)",
                     "equal(8,8)",
                     "equal(9,9)",
                     "equal(10,10)",
                     "equal(A1,A1)",
                     "equal(A2,A2)",
                     "equal(A3,A3)",
                     "equal(_,_)",
                     "equal(charging,charging)"]
    constraints_of_action_generation = [
        # Ensure the decision-making module will not generate decisions before the revision of goals and beliefs when encountering errors.
        "forall p. at(p) and fatal implies M(p)",
        "a-goal-holding and not holding and docked(3) and not nonfatal and not E2 and not fatal implies A",
        "a-goal-holding and not holding and docked(4) and not nonfatal and not E2 and not fatal implies A",
        # From P4 to P2
        "a-goal-at(2) and docked(4) and holding and assigned(2) and not E1 and not fatal implies B(4)",
        # From P3 to P2
        "a-goal-at(2) and docked(3) and holding and assigned(2) and not E1 and not fatal implies B(3)",
        # Request location permission for P2.
        "exists x. a-goal-at(2) and docked(x) and holding and not fatal implies S(2)",
        # AMR goes from P1 to P3 or P4, from P6, P7, P8 to P3 or P4, from P2 to P5, from P5 to P6, P7,P8
        "forall p. a-goal-at(p) and not holding and not equal(p,2) and assigned(p) and not fatal implies C(p)",
        "exists p. a-goal-at(p) and holding and holding_error and assigned(p) and not fatal implies C(p)",
        "exists p. a-goal-at(p) and holding and docking_error and assigned(p) and not fatal implies C(p)",
        "exists p. a-goal-at(p) and docking_error and assigend(p) and not fatal implies C(p)",
        "forall p. a-goal-at(p) and not holding and not equal(p,2) and not fatal implies S(p)",
        "exists p. a-goal-at(p) and holding and holding_error and not fatal implies S(p)",
        "a-goal-at(5) and docking_error and at(2) and not assigned(5) and not fatal implies S(5)",
        "a-goal-at(5) and docking_error and at(3) and not assigned(5) and not fatal implies S(5)",
        "a-goal-at(5) and docking_error and at(4) and not assigned(5) and not fatal implies S(5)",
        # To be changed
        "forall p. a-goal-dropped(p) and at(p) and docked(p) and holding and not E3 and not fatal implies D(p)",

        "forall p. a-goal-battery(2) and assigned(p) and battery(1) and docked(p) and not fatal implies E(p)",
        "a-goal-located(charging) and at(5) and not fatal implies F",
        "exists x,y. reserved(x,y) implies G"
    ]
    enableness_of_actions = [
        "A implies pickup",
        "A implies pickup_fail",
        # from P3,P4 to P2
        "forall x. B(x) implies move3(x,2)",
        "forall x. B(x) implies move3_fail(x,2)",
        "forall x. B(x) implies move3_fail2(x,2)",
        # from P2,P3,P4,P6,P7,P8 to P5
        "forall y. C(5) and at(y) and docked(y) and not equal(y,1) implies move4(y,5)",
        "forall y. C(5) and at(y) and docked(y) and not equal(y,1) implies move4_fail(y,5)",
        # from P2,P3,P4,P6...,P7,P8 to P5 Docking Error handling
        "forall p. C(p) and at(2) and docking_error implies move5(2,p)",
        "forall p. C(p) and at(2) and docking_error implies move5_fail(2,p)",
        "forall p. C(p) and at(3) and docking_error implies move5(3,p)",
        "forall p. C(p) and at(3) and docking_error implies move5_fail(3,p)",
        "forall p. C(p) and at(4) and docking_error implies move5(4,p)",
        "forall p. C(p) and at(4) and docking_error implies move5_fail(4,p)",
        # from P2,P3,P4,P6,P7,P8 to P2,P3,P4,P6,P7,P8
        "forall p,y. C(p) and at(y) and not equal(y,1) and not equal(y,5) and not equal(p,1) and not equal(p,5) implies move3(y,p)",
        "forall p,y. C(p) and at(y) and not equal(y,1) and not equal(y,5) and not equal(p,1) and not equal(p,5) implies move3_fail(y,p)",
        "forall y. C(2) and at(y) and not equal(y,1) and not equal(y,5) and not E1 implies move3_fail2(y,2)",
        "forall y. C(3) and at(y) and not equal(y,1) and not equal(y,5) and not E1 implies move3_fail2(y,3)",
        "forall y. C(4) and at(y) and not equal(y,1) and not equal(y,5) and not E1 implies move3_fail2(y,4)",

        # from P5 to P6,P7,P8
        "forall p. C(p) and at(5) and implies move2(5,p)",
        "forall p. C(p) and at(5) and implies move2_fail(5,p)",
        "forall p. C(p) and at(5) and implies move2_fail2(5,p)",
        "exists p. D(p) implies dropoff(p)",
        "exists p. D(p) implies dropoff_fail(p)",
        "forall p. E(p) implies charging(p)",
        "forall p. E(p) implies charging_fail(p)",
    ]
    sent_message_update = [
        "F implies send!(C) idle(_)",
        "G implies send?(allother) released(_)",
        "forall p. S(p) implies send!(C) idle(p)",
        "forall y. M(y) implies send!(C) at(y)"
                           ]

    event_processing = [
        # Fatal Error handling
        "E4 implies insert charging_error",
        "fatal implies drop allgoals",
        "fatal implies delete all",
        "located(charging) and pick_error implies delete pick_error",
        # Fix error rules for the static verification
        "exists x. holding and located(charging) and holding_error implies delete holding",
        "located(charging) and holding_error implies delete holding_error",
        "exists x. holding and located(charging) and docking_error implies delete holding",
        "located(charging) and docking_error implies delete docking_error",
        "forall p. at(2) and dropped(p) implies delete dropped(p)",
        # Nonfatal Error handling
        "nonfatal and not located(charging) implies drop all",
        "nonfatal and not located(charging) implies adopt located(charging)",
        "nonfatal and not located(charging) implies adopt at(5)",
        "E1 implies insert docking_error",
        "E2 implies insert pick_error",
        "E3 implies insert holding_error",
        # "nonfatal and not goal_change implies insert goal_change",
        "nonfatal and E1 implies delete E1",
        "nonfatal and E2 implies delete E2",
        "nonfatal and E3 implies delete E3",
        # Release location permission for the fatal agent
        "forall z. exists x,y. sent!(x) at(y) and reserved(x,z) implies insert idle(z)",
        "forall x,z. exists y. sent!(x) at(y) and reserved(x,z) implies delete reserved(x,z)",
        # Normal event processing
        "forall x,z in D6 . exists y. sent!(x) idle(y) and idle(y) and not reserved(z,y) implies insert reserved(x,y)",
        "forall x. exists y. sent!(x) idle(y) and reserved(x,y) implies send:(x) assigned(y)",
        "forall y. exists x,z. sent!(x) idle(y) and reserved(z,y) and equal(x,z) implies delete idle(y)",
        "forall x,y. sent?(x) released(_) and released(y) implies send:(x) idle(y)",
        "forall y. exists x. sent?(x) released(_) and released(y) implies delete released(y)",
        "forall y. exists x. sent:(x) idle(y) implies insert idle(y)",
        "forall y. exists x. sent:(x) idle(y) implies delete reserved(x,y)",
        "forall x,z in D6 ,m in D4 . sent!(x) idle(_) and idle(6) and not reserved(z,6) and not reserved(x,m) implies insert reserved(x,6)",
        "forall x. sent!(x) idle(_) and idle(6) and reserved(x,6) implies send:(x) assigned(6)",
        "exists x. sent!(x) idle(_) and reserved(x,6) implies delete idle(6)",
        "forall x,z in D6 ,m in D4 . sent!(x) idle(_) and idle(7) and not reserved(z,7) and not reserved(x,m) implies insert reserved(x,7)",
        "forall x. sent!(x) idle(_) and idle(7) and reserved(x,7) implies send:(x) assigned(7)",
        "exists x. sent!(x) idle(_) and reserved(x,7) implies delete idle(7)",
        "forall x,z in D6 ,m in D4 . sent!(x) idle(_) and idle(8) and not reserved(z,8) and not reserved(x,m) implies insert reserved(x,8)",
        "forall x. sent!(x) idle(_) and idle(8) and reserved(x,8) implies send:(x) assigned(8)",
        "exists x. sent!(x) idle(_) and reserved(x,8) implies delete idle(8)",
        "forall y. exists x. sent:(x) assigned(y) implies insert assigned(y)",
        "forall p. exists s. a-goal-transport(s,p) implies adopt dropped(p)",
        "forall s. exists p. a-goal-transport(s,p) implies adopt at(s)",
        "forall p. exists s. a-goal-transport(s,p#) implies adopt at(p)",
        "exists s,p. a-goal-dropped(p) implies adopt located(charging)",
        "exists p. a-goal-dropped(p) and not holding implies adopt holding",
        "exists p. a-goal-located(charging) and docked(2) and not holding implies adopt at(5)",
        "forall p. a-goal-located(charging) and at(5) and assigned(p) implies adopt at(p)",
        "forall s,p. a-goal-transport(s,p) implies drop transport(s,p)",
        "at(6) and battery(1) implies adopt battery(2)",
        "at(7) and battery(1) implies adopt battery(2)",
        "at(8) and battery(1) implies adopt battery(2)",
        "a-goal-at(6) and battery(1) and at(5) implies adopt battery(2)",
        "a-goal-at(7) and battery(1) and at(5) implies adopt battery(2)",
        "a-goal-at(8) and battery(1) and at(5) implies adopt battery(2)"
    ]

    action_specification = {
        "pickup": "pickup and not holding implies holding",
        "pickup_fail": "pickup_fail implies E2",
        "dropoff": "fora ll p. dropoff(p) and holding implies dropped(p) and not holding",
        "dropoff_fail": "dropoff_fail implies E3",
        # move2: from P5 to P6, P7, P8
        "move2": "forall x,y. move2(x,y) and at(x) implies at(y) and not at(x) and docked(y) and not assigned(x)",
        "move2_fail": "exists x,y. move2_fail(x,y) implies E5",
        "move2_fail2": "exists x,y. move2_fail2(x,y) and at(x) implies E1 and at(y) and not at(x) and not assigned(x)",
        # move3: from P2, P3, P4, P5, P6, P7, P8 to P2, P3, P4,  P6, P7, P8
        "move3": "forall x,y. move3(x,y) and at(x) and docked(x) implies at(y) and not at(x) and docked(y) and not docked(x) and not assigned(x)",
        "move3_fail": "exists x,y. move3_fail(x,y) implies E5",
        "move3_fail2": "forall x,y. move3_fail2(x,y) and at(x) and docked(x) implies E1 and at(y) and not at(x) and not docked(x) and not assigned(x)",
        # move4: from P2, P3, P4, P5, P6, P7, P8 to P5
        "move4": "forall x,y. move4(x,y) and at(x) and docked(x) implies at(y) and not at(x) and not docked(x) and not assigned(x)",
        "move4_fail": "exists x,y. move4_fail(x,y) implies E5",
        # move5: from undocked P2, P3, P4, P5, P6, P7, P8  to P5
        "move5": "forall x,y. move5(x,y) and at(x) implies at(y) and not at(x) and not assigned(x)",
        "move5_fail": "exists x,y. move5_fail(x,y) implies E5",
        "charging": "exists p. charging(p) and battery(1) implies battery(2) and not battery(1)",
        "charging_fail": "exists p. charging(p) and battery(1) implies E4"
    }
    domain = {
              "D4":["6", "7", "8"],"D6": ["A1", "A2","A3"]}
    constants = ["0", "1", "2","3", "4", "5", "6", "7", "8",  "9", "10","charging","allother", "all", '_',"A1","A2","A3","C","D"]
    belief_base4 = ["idle(2)", "idle(3)", "idle(4)","idle(5)", "reserved(A1,6)", "reserved(A2,7)", "reserved(A3,8)"]
    goal_base1 = ['transport(3,2)']
    goal_base2 = ['transport(4,2)']
    goals1=[goal_base1]
    goals2 = [goal_base2]
    goals3 = [goal_base1,goal_base1]
    goals4 = []
    dummy_agents=["C"]
    safety = {"A1": ["safe1","safe2"], "A2": ["safe1","safe2"], "A3": ["safe1","safe2"]}
    A1 = DG.Agent("A1", [], goals1)
    A2 = DG.Agent("A2", [], goals2)
    A3 = DG.Agent("A3", [], goals3)
    C = DG.Agent("C", belief_base4, goals4)
    Agents = [A1,C]
    prior_beliefs=[]
    agent_test = DG.interpreter(Agents, knowledge_base, constraints_of_action_generation,
                                 enableness_of_actions, action_specification, sent_message_update,
                                 event_processing, domain, constants, dummy_agents, safety,prior_beliefs)

    end = time.time()
    f = open("Record.txt", "w+")
    f.write("The duration time is :" + str(end - start))
    f.close()

main()
