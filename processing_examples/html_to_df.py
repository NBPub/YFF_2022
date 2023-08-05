import pandas as pd

tables = pd.read_html() # saved webpage

# Positions Abbreviation
positions = tables[3]
positions.rename(mapper = dict(zip(positions.columns, positions.iloc[0,:])), 
                 axis = 'columns', inplace=True)
positions = positions.iloc[1:,:]
positions.to_csv('positions.csv')

# Stats Abbreviations
stats = tables[2]
stats.rename(mapper = dict(zip(stats.columns, stats.iloc[1,:])), 
             axis = 'columns', inplace=True)
stats = stats.iloc[2:,:]
stats.index = stats.index-1 
stats.to_csv('stats.csv')

# Player Status Abbreviations
player_status = tables[1]
player_status.columns = ['Player Status', 'What it Means']
player_status = player_status.iloc[8:25,:]
player_status.index = player_status.index-7
player_status.to_csv('player_status.csv')

# main fantasy table, run following function

data = tables[0].copy()

def table_processing(data):
    # make new col names, removing "Unnamed: ..."
    new_cols = []
    for i,val in enumerate(data.columns):
        swap = []
        for name in val:
            swap.append(name if name.find('Unnamed:') == -1 else '')
        new_cols.append(tuple(swap))
    
    # change to new names, combine to one level, drop empty
    data.columns = pd.MultiIndex.from_tuples(new_cols)
    data.columns = data.columns.map('_'.join).str.strip('_')
    data.drop(labels = '', axis=1, inplace=True)
    
    # individual renames, drops. remove "*"
    data.drop(labels=['Roster Status', 'Bye'], axis=1, inplace=True)
    data.rename(columns = {data.columns[2]:'Fantasy Pts'}, inplace=True)
    data.columns = data.columns.str.replace('*','', regex=False)
    
    # player name, team extraction
    player_names = data.Offense.str.replace('  ',' ').str.split(' ')
    player_teams = []
    for i,val in enumerate(player_names):
        if val[0] == 'No':
            player_names[i] = ' '.join(val[4:6])
            player_teams.append(val[6])
        elif val[0] == 'New':
            player_names[i] = ' '.join(val[3:5])
            player_teams.append(val[5])        
        else:
            player_names[i] = ' '.join(val[2:4])
            player_teams.append(val[4])    
    
    # add back to DataFrame, rename
    data.Offense = player_names
    data.loc[:,'Team'] = player_teams
    data.rename(columns = {'Offense':'Name'}, inplace=True)
    
    return data