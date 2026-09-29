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
    def __init__(self, data, to_insert_team_indices=False):
        self.data = data
        self.to_insert_team_indices = to_insert_team_indices
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

    def process_data(self):
        first_innings_data, second_innings_data = [], []
        for d in self.data:
            first_innings_states = process_first_innings(d)
            second_innings_states = process_second_innings(d)

            label = get_label(d)

            first_innings_states = insert_labels(first_innings_states, label)
            second_innings_states = insert_labels(second_innings_states, label)

            first_inning_batting_team = d['innings'][0]['team']
            second_inning_batting_team = d['innings'][1]['team']

            if self.to_insert_team_indices:
                first_innings_states = self.insert_team_indices(first_innings_states, first_inning_batting_team, second_inning_batting_team)
                second_innings_states = self.insert_team_indices(second_innings_states, second_inning_batting_team, first_inning_batting_team)

            first_innings_data.append(first_innings_states)
            second_innings_data.append(second_innings_states)

        self.key_order = list(first_innings_data[0][0].keys()) if first_innings_data else []
        return first_innings_data, second_innings_data

    def get_data_non_sequential(self):
        first_innings_data, second_innings_data = self.process_data()
        first_innings_data = [state for match in first_innings_data for state in match]
        second_innings_data = [state for match in second_innings_data for state in match]
        return first_innings_data, second_innings_data

    def to_innings_labels(self, innings):
        innings_array = [[state[v] for v in self.key_order if v != 'labels'] for state in innings]
        labels = innings[-1]['labels']
        return {
            'innings': innings_array,
            'labels': labels
        }

    def get_data_sequential(self):
        first_innings_data, second_innings_data = self.process_data()
        first_innings_data = [
            self.to_innings_labels(match) for match in first_innings_data
        ]
        second_innings_data = [
            self.to_innings_labels(match) for match in second_innings_data
        ]
        return first_innings_data, second_innings_data
