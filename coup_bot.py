import sys
import random

log_filename, op_coins, my_coins, my_cards = sys.argv[1:5]
available_actions = sys.argv[5:]

# Get the current line. If it has an even length >0 we need to continue it
with open(log_filename, 'r') as hist:
  cur_line = hist.read().split('\n')[-1]

op_coins = int(op_coins)
my_coins = int(my_coins)

def move_opts(symbol, *replies_list):
  replies = {}
  for reply in replies_list:
    replies = { **replies, **reply }
  
  return {
    'symbol': symbol,
    'replies': replies
  }

drop_card_opts = {
  # Note that the only reply for each of these is "ok". Like, "ok, you
  # lost a card, sucka!"
  'drop_ambassador': move_opts('_', { 'ok': move_opts('\n') }),
  'drop_assassin': move_opts('\'', { 'ok': move_opts('\n') }),
  'drop_captain': move_opts('<', { 'ok': move_opts('\n') }),
  'drop_contessa': move_opts('=', { 'ok': move_opts('\n') }),
  'drop_duke': move_opts('0', { 'ok': move_opts('\n') })
}
tolerate_opt = move_opts('p', { 'ok': move_opts('\n') })

move_tree = {
  'income': move_opts('I\n'),
  'foreign_aid': move_opts('F', {
    'duke_block': move_opts('d', {
      'challenge_duke': move_opts('q', drop_card_opts, {
        'show_duke': move_opts('$', drop_card_opts),
      }),
      'tolerate': move_opts('\n')
    }),
    'tolerate': move_opts('\n')
  }),
  'coup': move_opts('C', drop_card_opts),
  'exchange': move_opts('E', {
    'challenge_ambassador': move_opts('q', drop_card_opts, {
      'show_ambassador': move_opts('~', drop_card_opts)
    }),
    'tolerate': tolerate_opt
  }),
  'tax': move_opts('T', {
    'challenge_duke': move_opts('q', drop_card_opts, {
      'show_duke': move_opts('$', drop_card_opts)
    }),
    'tolerate': tolerate_opt
  }),
  'assassinate': move_opts('A', drop_card_opts, {
    'contessa_block': move_opts('s', {
      'challenge_contessa': move_opts('q', drop_card_opts, {
        'show_contessa': move_opts('!', drop_card_opts)
      }),
    }),
    'challenge_assassin': move_opts('q', drop_card_opts, {
      'show_assassin': move_opts('^', drop_card_opts)
    })
  }),
  'steal': move_opts('S', {
    'ambassador_block': move_opts('a', {
      'challenge_ambassador': move_opts('q', drop_card_opts, {
        'show_ambassador': move_opts('~', drop_card_opts)
      }),
      'tolerate': move_opts('\n')
    }),
    'captain_block': move_opts('c', {
      'challenge_captain': move_opts('q', drop_card_opts, {
        'show_captain': move_opts('*', drop_card_opts)
      }),
      'tolerate': move_opts('\n')
    }),
    'challenge_captain': move_opts('q', drop_card_opts, {
      'show_captain': move_opts('*', drop_card_opts)
    }),
    'tolerate': tolerate_opt
  })
}


# Map "move types" to lamdbas which determine if this is the type of
# move we need to make.
determine_move_type = {
  'simple_strategy': lambda: True
}

# A bunch of functions to execute different moves types. Each should
# return the sequence to be written to the log
def do_simple_strategy():
  
  # If it's our turn, coup if possible, and if not, take income.
  
  if len(cur_line) > 1: return available_actions[0]
  
  if my_coins < 7:
    return move_tree['income']['symbol']
  
  return move_tree['coup']['symbol']

if __name__ == '__main__':
  
  # Determine the move type
  move_type = None
  for possible_move_type, func in determine_move_type.items():
    if not func(): continue
    move_type = possible_move_type
    break

  if move_type is None: raise ValueError('OH LAWD')
  
  # Get the function used to execute the move type
  move_func = globals()['do_' + move_type]

  with open(log_filename, 'a') as log_file:
    log_file.write(move_func())
