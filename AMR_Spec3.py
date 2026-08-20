import Interpreter as DG
import time

start = time.time()

def main():
    knowledge_base =["forall w. on(w,4) implies available(w)",
                     "forall w. on(w,3) implies available(w)",
                     "forall w,p. on(w,p) and equal(p,2) implies delivered(p,w)",
                     "at(6) implies located(charging)",
                     "at(7) implies located(charging)",
                     "at(8) implies located(charging)",
                     "battery(1) implies safe1",
                     "battery(2) implies safe1",
                     "exists p. at(p) and not at(9) implies safe2",
                     #Error implication
                     "E1 implies fatal",
                     "E2 implies fatal",
                     "E3 implies fatal",
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
        #Ensure the decision-making module will not generate decisions before the revision of goals and beliefs when encountering errors.
        "forall p. at(p) and fatal implies M(p)",
        "nonfatal implies Dummy",
        "forall w,y in D2 . a-goal-holding(w) and docked(p) and not holding(y) and docked(4) and available(w) implies A(w)",
        "forall w,y in D2 . a-goal-holding(w) and docked(p) and not holding(y) and docked(3) and available(w) implies A(w)",
        "a-goal-docked(2)  implies H(2)",
        "a-goal-docked(3)  implies H(3)",
        "a-goal-docked(4)  implies H(4)",
        "a-goal-docked(6)  implies H(6)",
        "a-goal-docked(7)  implies H(7)",
        "a-goal-docked(8)  implies H(8)",
        #From P4 to P2
        "exists w. a-goal-at(2) and docked(4) and holding(w) and assigned(2) implies B(4)",
        # From P3 to P2
        "exists w. a-goal-at(2) and docked(3) and holding(w) and assigned(2) implies B(3)",
        #Request location permission for P2.
        "exists x,w. a-goal-at(2) and docked(x) and holding(w) implies S(2)",
        #AMR goes from P1 to P3 or P4, from P6, P7, P8 to P3 or P4, from P2 to P5, from P5 to P6, P7,P8
        "forall p,w in D2 . a-goal-at(p) and not holding(w) and not equal(p,2) and assigned(p) implies C(p)",
        "forall p,w in D2 . a-goal-at(p) and not holding(w) and not equal(p,2) implies S(p)",
        "forall w. a-goal-on(w,2) and at(2) and docked(2) and holding(w) implies D(w,2)",
        "forall p. a-goal-battery(2) and assigned(p) and battery(1) and docked(p) implies E(p)",
        "a-goal-located(charging) and at(5) implies F",
        "exists x,y. reserved(x,y) implies G"
    ]
    enableness_of_actions = [
        "forall w. A(w) implies pickup(w)",
        "forall p. H(p) implies dock(p)",
        #from P3,P4 to P2
        "forall x. B(x) implies move3(x,2)",
        #from P1 to P2,P3,P4,P6,P7,P8
        "forall p,y. C(p) and at(y) and equal(y,1) and not equal(p,5) implies move1(y,p)",
        #from P2,P3,P4,P6,P7,P8 to P5
        "forall p,y. C(p) and at(y) and docked(y) and not equal(y,1) and equal(p,5) implies move4(y,p)",
        # from P2,P3,P4,P6,P7,P8 to P5 Docking Error handling
        "forall p,y. C(p) and at(y) and not equal(y,1) and equal(p,5) implies move5(y,p)",
        # from P2,P3,P4,P6,P7,P8 to P2,P3,P4,P6,P7,P8
        "forall p,y. C(p) and at(y) and not equal(y,1) and not equal(y,5) and not equal(p,1) and not equal(p,5) implies move3(y,p)",
        #from P5 to P6,P7,P8
        "forall p,y. C(p) and at(y) and equal(y,5) and implies move2(y,p)",
        "forall w. D(w,2) implies dropoff(w,2)",
        "forall p. E(p) implies charging(p)"
    ]
    sent_message_update = [
        "F implies send!(C) idle(_)",
        "G implies send?(allother) released(_)",
        "forall p. S(p) implies send!(C) idle(p)",
        "forall y. M(y) implies send!(C) at(y)"
                           ]

    event_processing = [
        #Error handling
        "fatal implies drop all",
        "fatal implies delete all",
        "nonfatal and not goal_change implies drop all",
        "nonfatal and not goal_change implies adopt located(charging)",
        "nonfatal and not goal_change implies adopt at(5)",
        "nonfatal and not goal_change implies insert goal_change",
        "nonfatal and E1 implies delete E1",
        "nonfatal and E2 implies delete E2",
        "nonfatal and E3 implies delete E3",
        #Normal event processing
        "forall z. exists x,y. sent!(x) at(y) and reserved(x,z) and not equal(z,y) implies insert idle(z)",
        "forall x,z. exists y. sent!(x) at(y) and reserved(x,z) and not equal(z,y) implies delete reserved(x,z)",
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
        "forall p,w. a-goal-delivered(p,w) implies adopt on(w,p)",
        "exists p,w. a-goal-delivered(p,w) implies adopt located(charging)",
        "forall p. exists x,w. a-goal-on(w,2) and on(w,p) and at(x) implies adopt at(p)",
        "forall p. exists w. a-goal-on(w,2) and on(w,p) and at(5) implies adopt at(p)",
        "forall p. exists w. a-goal-on(w,2) and on(w,p) and docked(6) implies adopt at(p)",
        "forall p. exists w. a-goal-on(w,2) and on(w,p) and docked(7) implies adopt at(p)",
        "forall p. exists w. a-goal-on(w,2) and on(w,p) and docked(8) implies adopt at(p)",
        "exists w. a-goal-on(w,2) and not at(2) implies adopt at(2)",
        "forall w,y in D2 . a-goal-on(w,2) and not holding(y) implies adopt holding(w)",
        "forall y in D2 . exists p. a-goal-located(charging) and docked(2) and not holding(y) implies adopt at(5)",
        "forall p. a-goal-located(charging) and at(5) and assigned(p) implies adopt at(p)",
        "a-goal-at(6) and battery(1) and at(5) implies adopt battery(2)",
        "a-goal-at(7) and battery(1) and at(5) implies adopt battery(2)",
        "a-goal-at(8) and battery(1) and at(5) implies adopt battery(2)"
    ]

    action_specification = {
        "pickup": "forall w,p,y in D2 . pickup(w) and not holding(y) and on(w,p) implies holding(w) and not on(w,p)",
        #move1: from P1 to P2, P3, P4, P6, P7, P8
        "move1": "forall x,y. move1(x,y) and at(x) implies at(y) and and docked(y) not at(x)",
        #move2: from P5 to P2, P3, P4, P5, P6, P7, P8
        "move2": "forall x,y. move2(x,y) and at(x) implies at(y) and not at(x) and docked(y) and not assigned(x)",
        #move3: from P2, P3, P4, P5, P6, P7, P8 to P2, P3, P4, P5, P6, P7, P8
        "move3":"forall x,y. move3(x,y) and at(x) and docked(x) implies at(y) and not at(x) and docked(y) and not docked(x) and not assigned(x)",
        #move4: from P2, P3, P4, P5, P6, P7, P8 to P5
        "move4": "forall x,y. move4(x,y) and at(x) and docked(x) implies at(y) and not at(x) and not docked(x) and not assigned(x)",
        # move5: from undocked P2, P3, P4, P5, P6, P7, P8  to P5
        "move5": "forall x,y. move5(x,y) and at(x) implies at(y) and not at(x) and not assigned(x)",
        "dropoff": "forall w. dropoff(w) and holding(w) implies on(w,2) and not holding(w)",
        "charging": "exists p. charging(p) and battery(1) implies battery(2) and not battery(1)"
    }
    domain = { "D2": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
              "D4":["6", "7", "8"],"D6": ["A1", "A2","A3"]}
    constants = ["0", "1", "2","3", "4", "5", "6", "7", "8",  "9", "10","charging","allother", "all", '_',"A1","A2","A3","C","D"]
    belief_base4 = ["idle(2)", "idle(3)", "idle(4)","idle(5)", "reserved(A1,6)", "reserved(A2,8)", "reserved(A3,7)"]
    goal_base1 = ['delivered(2,1)']
    goal_base2 = ["delivered(2,2)"]
    goal_base3 = ['delivered(2,3)']
    goal_base4 = ["delivered(2,4)"]
    goals1=[goal_base1]
    goals2 = [goal_base2]
    goals3 = [goal_base3,goal_base4]
    goals4 = []
    dummy_agents=["C"]
    safety = {"A1": ["safe1","safe2"], "A2": ["safe1","safe2"], "A3": ["safe1","safe2"]}
    A1 = DG.Agent("A1", [], goals1)
    A2 = DG.Agent("A2", [], goals2)
    A3 = DG.Agent("A3", [], goals3)
    C = DG.Agent("C", belief_base4, goals4)
    Agents = [A1,A2,A3,C]
    prior_beliefs=["on(1,3)","on(2,4)","on(3,3)","on(4,3)"]
    agent_test = DG.interpreter(Agents, knowledge_base, constraints_of_action_generation,
                                 enableness_of_actions, action_specification, sent_message_update,
                                 event_processing, domain, constants, dummy_agents, safety,prior_beliefs)

    end = time.time()
    f = open("Record.txt", "w+")
    f.write("The duration time is :" + str(end - start))
    f.close()

main()
