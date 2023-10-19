from storage import RamStorage

def save_new_user(message):

    if str(message.chat.id) not in RamStorage.users_data:
        RamStorage.users_data[str(message.chat.id)] = {
            "selected_base": None,
            "num_mutations": None,
            "synt_method": None,
            "activation_method": None,
        }

def select_molecule(message):
    selected_base = RamStorage.users_data[str(message.chat.id)]['selected_base']
    num_mutations = RamStorage.users_data[str(message.chat.id)]['num_mutations']
    synt_method = RamStorage.users_data[str(message.chat.id)]['synt_method']
    activation_method = RamStorage.users_data[str(message.chat.id)]['activation_method']

    synt_method_thresh = 0.5 if synt_method == 'ecoli' else 0
    select_df = RamStorage.df.loc[RamStorage.df.base == selected_base]
    select_df = select_df.loc[select_df.mut <= int(num_mutations)]
    select_df = select_df.loc[select_df.sodope >= synt_method_thresh]
    select_df = select_df.loc[select_df.action == activation_method]

    if select_df.empty:
        return None

    return select_df.picture.values[0]
