def is_extra(delivery):
        if 'extras' not in delivery:
            return False
        return 'noballs' in delivery['extras'] or 'wides' in delivery['extras']

def process_first_innings(innings):
    states = []
    runs = 0
    wickets = 0
    balls = 0
    
    for over in innings['overs']:
        for delivery in over['deliveries']:
            runs += delivery['runs']['total']
            wickets += len(delivery.get('wickets', []))
            balls += 0 if is_extra(delivery) else 1
            states.append({ 'runs': runs, 'wickets': wickets, 'balls': balls })
    return states

def process_second_innings(innings):
    assert 'target' in innings, "Second innings data must contain a target"
    states = []
    runs = innings['target']['runs']
    wickets = 10
    balls = 300

    for over in innings['overs']:
        for delivery in over['deliveries']:
            runs -= delivery['runs']['total']
            wickets -= len(delivery.get('wickets', []))
            balls -= 0 if is_extra(delivery) else 1
            states.append({ 'runs': runs, 'wickets': wickets, 'balls': balls })
    return states

def insert_labels(inning_states, label):
    for state in inning_states:
        state['labels'] = label
    return inning_states

def process_data(data):
    first_innings_data, second_innings_data = [], []
    for d in data:
        first_innings_states = process_first_innings(d['innings'][0])
        second_innings_states = process_second_innings(d['innings'][1])

        first_innings_team = d['innings'][0]['team']
        winning_team = d['info']['outcome']['winner']
        label = 1 if first_innings_team == winning_team else 0

        first_innings_states = insert_labels(first_innings_states, label)
        second_innings_states = insert_labels(second_innings_states, label)

        first_innings_data.extend(first_innings_states)
        second_innings_data.extend(second_innings_states)

    return first_innings_data, second_innings_data
