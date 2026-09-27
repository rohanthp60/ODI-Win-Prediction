def is_extra(delivery):
        if 'extras' not in delivery:
            return False
        return 'noballs' in delivery['extras'] or 'wides' in delivery['extras']

def process_first_innings(data_item):
    innings = data_item['innings'][0]
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

def process_second_innings(data_item):
    innings = data_item['innings'][1]
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


def get_label(data_item):
    first_innings_team = data_item['innings'][0]['team']
    winning_team = data_item['info']['outcome']['winner']
    return 1 if first_innings_team == winning_team else 0


class Dataset:
    def __init__(self, data):
        self.data = data
        self.team_to_index = self.get_all_teams_to_index()

    def get_all_teams_to_index(self):
        teams = set()
        for d in self.data:
            for inning in d['innings']:
                teams.add(inning['team'])
        return {team: index for index, team in enumerate(sorted(teams))}

    def num_teams(self):
        return len(self.team_to_index)

    def get_team_index(self, team):
        return self.team_to_index.get(team, -1)

    def insert_team_indices(self, inning_states, batting_team, bowling_team):
        for state in inning_states:
            state['batting_team'] = self.get_team_index(batting_team)
            state['bowling_team'] = self.get_team_index(bowling_team)
        return inning_states

    def process_data(self, insert_team_indices=False):
        first_innings_data, second_innings_data = [], []
        for d in self.data:
            first_innings_states = process_first_innings(d)
            second_innings_states = process_second_innings(d)

            label = get_label(d)

            first_innings_states = insert_labels(first_innings_states, label)
            second_innings_states = insert_labels(second_innings_states, label)

            first_inning_batting_team = d['innings'][0]['team']
            second_inning_batting_team = d['innings'][1]['team']

            if insert_team_indices:
                first_innings_states = self.insert_team_indices(first_innings_states, first_inning_batting_team, second_inning_batting_team)
                second_innings_states = self.insert_team_indices(second_innings_states, second_inning_batting_team, first_inning_batting_team)

            first_innings_data.extend(first_innings_states)
            second_innings_data.extend(second_innings_states)

        return first_innings_data, second_innings_data
