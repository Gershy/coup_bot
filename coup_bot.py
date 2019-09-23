import sys
import random

history_filename, othercoins, mycoins, mycards = sys.argv[1:5]

print('HIST FILE:', history_filename)

'''
legalActions = sys.argv[5:]

actions_dict = {'E': '_', 'T': '0', 'A': "'", 'S': '<', 'd': '0', 'a': '_', 'c': '<', 's': '='}
punishment_to_reveal = {'_': '~', "'": '^', '<': '*', '=': '!', '0': '$'}
reveal_to_punishment = {punishment_to_reveal[k]: k for k in punishment_to_reveal}

obviousActions = ['~', '^', '*', '!', '$']
lossActions = ['_', "'", '<', '=', '0']

statefilename = './state.txt'
flags = set()
# Flags:
# 1 We went first
# $ Attacking with Duke
# * Attacking with Captain
# ^ Attacking with Assassin
# d Opponent used Duke
# c Opponent used Captain
# A Opponent used Assassin
# F Opponent used Foreign Aid

with open(statefilename, "a+") as statefile:
  statefile.seek(0)
  if statefile.readline().strip() == filename:
    flags = set(statefile.readline().strip())

with open(filename, "r+") as history:
  line = "\n"
  turn = 0
  oppcardcount = 4 - len(mycards)
  for a in history:
    line = a
    turn += 1
    if [c for c in line if c in lossActions]:
      oppcardcount -= 1
  else:
    flags.add("1")

  mycoins = int(mycoins)
  othercoins = int(othercoins)
  mycardcount = len(mycards)

  if line == 'T':
    othercoins += 3
    flags.add('d')
  elif line == 'S':
    othercoins += (2 if mycoins > 2 else mycoins)
    mycoins -= (2 if mycoins > 2 else mycoins)
    flags.add('c')
  elif line == 'A':
    othercoins -= 3
    mycardcount -= 1
    flags.add('A')
  elif line == 'F':
    flags.add('F')
  elif line == 'I\n':
    # If opponent is backing down, they're not so scary anymore
    flags.discard('d')
    flags.discard('c')
    flags.discard('F')

  # What's the least aggressive play that still wins?
  iGetStolen = ('c' in flags and not '*' in mycards and not '~' in mycards)
  iGetAssassinated = ('A' in flags and not '!' in mycards)
  incomeTimeToWin = max(0,7*oppcardcount-mycoins)+oppcardcount if not iGetStolen else 1000
  faidTimeToWin = max(0,7*oppcardcount-mycoins+1)//2+oppcardcount if not iGetStolen else 1000
  dukeTimeToWin = max(0,7*oppcardcount+(2*(oppcardcount-mycardcount) if iGetStolen else 0)-mycoins+2)//(3 if not iGetStolen else 1)+oppcardcount
  assassinTimeToWin = max(0,3*oppcardcount-mycoins)+oppcardcount if not iGetStolen else oppcardcount if mycoins >= 5*oppcardcount-2 else 1000
  captainTimeToWin = max(0,7*oppcardcount-mycoins+1)//2+oppcardcount
  faidAssassinTimeToWin = max(0,3*oppcardcount-mycoins+1)//2+oppcardcount if not iGetStolen else 1000
  dukeAssassinTimeToWin = max(0,3*oppcardcount+(2*(oppcardcount-mycardcount) if iGetStolen else 0)-mycoins+2)//(3 if not iGetStolen else 1)+oppcardcount
  captainAssassinTimeToWin = max(0,3*oppcardcount-mycoins+1)//2+oppcardcount
  opponentMoneySpeed = (2 if iGetStolen else 3 if 'd' in flags else 2 if 'F' in flags and not '$' in mycards else 1)
  opponentTimeToWin = max(0,(3 if iGetAssassinated else 7)*mycardcount-othercoins+opponentMoneySpeed-1)//opponentMoneySpeed+mycardcount
  opponentTimeToWinCaptained = max(0,(3 if iGetAssassinated else 7)*mycardcount+2*(mycardcount-oppcardcount)-(othercoins-2 if othercoins>2 else 0)+opponentMoneySpeed-3)//(opponentMoneySpeed-2)+mycardcount if opponentMoneySpeed > 2 else 1000

  def pickCardToLose():
    favoriteCards = []
    if dukeTimeToWin < opponentTimeToWin and '$' in mycards:
      favoriteCards = ['$', '!', '*', '~', '^']
    elif dukeAssassinTimeToWin < opponentTimeToWin and ('$' in mycards or '$' in flags) and '^' in mycards:
      favoriteCards = ['^', '$', '!', '*', '~']
    elif assassinTimeToWin < opponentTimeToWin and '^' in mycards:
      favoriteCards = ['^', '!', '*', '~', '$']
    elif captainTimeToWin < opponentTimeToWinCaptained and '*' in mycards:
      favoriteCards = ['*', '!', '$', '^', '~']
    elif faidTimeToWin < opponentTimeToWin and '^' in mycards and not 'd' in flags:
      favoriteCards = ['!', '*', '~', '$', '^']
    elif faidAssassinTimeToWin < opponentTimeToWin and '^' in mycards and not 'd' in flags:
      favoriteCards = ['^', '!', '*', '~', '$']
    elif captainAssassinTimeToWin < opponentTimeToWinCaptained and '*' in mycards and '^' in mycards:
      favoriteCards = ['^', '*', '!', '$', '~']
    else:
      favoriteCards = ['!', '*', '~', '$', '^']
    # Losing a card.  Decide which is most valuable.
    for k in favoriteCards:
      if k in mycards:
        cardToLose = k
    return reveal_to_punishment[cardToLose]

  action = legalActions[0]
  if line == "\n":
    # First turn behavior
    if '$' in mycards and 'T' in legalActions:
      action = 'T'
      flags.add('$')
    elif '*' in mycards and 'S' in legalActions:
      action = 'S'
      flags.add('*')
    elif '^' in mycards and 'I\n' in legalActions:
      action = 'I\n'
      flags.add('^')
    elif '~' in mycards and 'E' in legalActions:
      action = 'E'
    elif 'T' in legalActions:
      # Contessa/Contessa?  Need to lie.
      action = 'T'
      flags.add('$')
  elif set(obviousActions).intersection(legalActions):
    # Always take these actions if possible
    for a in set(obviousActions).intersection(legalActions):
      action = a
    # This might change our strategy
    flags.discard(action)
  elif '$' in mycards and 'd' in legalActions:
    action = 'd'
  elif '~' in mycards and 'a' in legalActions:
    action = 'a'
  elif '*' in mycards and 'c' in legalActions:
    action = 'c'
  elif '!' in mycards and 's' in legalActions:
    action = 's'
  elif 'q' in legalActions and line[-1] in 'dacs':
    # We're committed at this point
    action = 'q'
  elif 'q' in legalActions and '*' in flags and line[-1] in 'SE':
    # Don't allow these when using a steal strategy
    action = 'q'
  elif 'q' in legalActions and turn == 1:
    if line == 'T':
      if mycards == '$$' or mycards == '^^' or mycards == '!!':
        action = 'q'
      else:
        action = 'p'
        flags.add('d')
    elif line == 'S':
      if '$' in mycards and '^' in mycards:
        action = 'p'
        flags.add('c')
      else:
        action = 'q'
    elif line == 'E':
      action = 'p'
  elif line == 'A' and len(mycards) > 1:
    # Don't challenge the first assasination.  We'll get 'em later.
    action = pickCardToLose()
    flags.add('A')
  elif line == 'A':
    # Can't let this pass
    action = 'q'
  elif line == 'C':
    # Taking damage
    action = pickCardToLose()
  elif len(line) == 2 and line[1] == 'q':
    # My base action was successfully challenged
    action = pickCardToLose()+"\n"
    # Also stop claiming what we were challenged for
    if line == "Tq":
      flags.discard('$')
    elif line == "Sq":
      flags.discard('*')
    elif line == "Aq":
      flags.discard('^')
  elif len(line) == 3 and line[1] == 'q':
    # I failed challenging a base action
    action = pickCardToLose()
  elif len(line) == 3 and line[2] == 'q':
    # My block was successfully challenged
    action = pickCardToLose()
  elif len(line) == 4 and line[2] == 'q':
    # I failed challenging a block
    action = pickCardToLose()+"\n"
  else:
    if 'p' in legalActions:
      # Default to pass if no other action is chosen
      action = 'p'

    if dukeTimeToWin <= opponentTimeToWin and ('$' in mycards or '$' in flags):
      if 'C' in legalActions:
        action = 'C'
      elif 'T' in legalActions:
        action = 'T'
    elif incomeTimeToWin <= opponentTimeToWin:
      if 'C' in legalActions:
        action = 'C'
      elif 'I\n' in legalActions:
        action = "I\n"
    elif dukeAssassinTimeToWin <= opponentTimeToWin and ('$' in mycards or '$' in flags) and '^' in mycards and mycardcount > 1:
      if 3*oppcardcount <= mycoins - (2*(oppcardcount-1) if iGetStolen else 0) and 'A' in legalActions:
        action = 'A'
      elif 'T' in legalActions:
        action = 'T'
      flags.add('^');
    elif assassinTimeToWin <= opponentTimeToWin and '^' in mycards:
      if 'A' in legalActions:
        action = 'A'
      elif 'I\n' in legalActions:
        action = 'I\n'
      flags.add('^');
    elif captainTimeToWin <= opponentTimeToWinCaptained and '*' in mycards:
      if 'C' in legalActions:
        action = 'C'
      elif 'S' in legalActions:
        action = 'S'
      elif 'I\n' in legalActions:
        action = 'I\n'
      flags.add('*');
    elif faidTimeToWin <= opponentTimeToWin and not 'd' in flags:
      if 'C' in legalActions:
        action = 'C'
      elif 'F' in legalActions:
        action = 'F'
    elif faidAssassinTimeToWin <= opponentTimeToWin and '^' in mycards and not 'd' in flags:
      if 'A' in legalActions:
        action = 'A'
      elif 'F' in legalActions:
        action = 'F'
      flags.add('^');
    elif captainAssassinTimeToWin <= opponentTimeToWinCaptained and '*' in mycards and '^' in mycards:
      if 'A' in legalActions:
        action = 'A'
      elif 'S' in legalActions:
        action = 'S'
      flags.add('^');
      flags.add('*');
    elif 'q' in legalActions:
      action = 'q'
    # No winning strategy.  Find something useful to do anyway.
    elif 'C' in legalActions and not '^' in flags:
      action = 'C'
    elif 'S' in legalActions and '*' in flags:
      action = 'S'
    elif 'A' in legalActions and '^' in flags:
      action = 'A'
    elif 'E' in legalActions and '~' in mycards and dukeAssassinTimeToWin < opponentTimeToWin:
      action = 'E'
    elif 'F' in legalActions and not 'd' in flags:
      action = 'F'
    elif 'T' in legalActions:
      action = 'T'
      flags.add('$');
  if action == 'q':
    if line == 'T' or line == 'Fd':
      flags.discard('d')
    elif line == 'S' or line == 'Sc':
      flags.discard('c')
    elif line == 'A':
      flags.discard('A')
  history.write(action)

if len(mycards) > 2:
  favoriteCards = []
  if dukeTimeToWin < opponentTimeToWin and '$' in mycards:
    favoriteCards = ['$', '!', '*', '~', '^']
  elif dukeAssassinTimeToWin < opponentTimeToWin and ('$' in mycards or '$' in flags) and '^' in mycards:
    favoriteCards = ['^', '$', '!', '*', '~']
  elif assassinTimeToWin < opponentTimeToWin and '^' in mycards:
    favoriteCards = ['^', '!', '*', '~', '$']
  elif captainTimeToWin < opponentTimeToWinCaptained and '*' in mycards:
    favoriteCards = ['*', '!', '$', '^', '~']
  elif faidTimeToWin < opponentTimeToWin and '^' in mycards and not 'd' in flags:
    favoriteCards = ['!', '*', '~', '$', '^']
  elif faidAssassinTimeToWin < opponentTimeToWin and '^' in mycards and not 'd' in flags:
    favoriteCards = ['^', '!', '*', '~', '$']
  elif captainAssassinTimeToWin < opponentTimeToWinCaptained and '*' in mycards and '^' in mycards:
    favoriteCards = ['^', '*', '!', '$', '~']
  else:
    favoriteCards = ['!', '*', '~', '$', '^']
  # Losing two cards.  Decide which is most valuable.
  possibleCards = [k for k in favoriteCards if k in mycards]
  if len(possibleCards) < len(mycards) - 2:
    possibleCards = list(mycards)
    random.shuffle(possibleCards)
  mycards = ''.join(possibleCards[:(len(mycards)-2)])
  print mycards

with open(statefilename, "w") as statefile:
  statefile.write(filename+"\n")
  statefile.write(''.join(list(flags))+"\n")
'''
