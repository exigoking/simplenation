from datetime import datetime, tzinfo
from django.utils.timezone import utc


def last_posted_date(post_date):
   now = datetime.utcnow()
   naive_now = now.replace(tzinfo=None)
   naive_post_date = post_date.replace(tzinfo=None)

   # If happening time is in the PAST
   if naive_now >= naive_post_date:
      diff = naive_now-naive_post_date
      s = diff.seconds
      weeks = diff.days/7
      months = diff.days/30
      years = diff.days/365
   
      if diff.days > 1000 or diff.days < 0:
         return post_date.strftime('%d %b %y')
      elif years == 1:
         return '1 year ago'
      elif years > 1:
         return '{} years ago'.format(years)
      elif months == 1:
         return '1 month ago'
      elif months > 1:
         return '{} months ago'.format(months)
      elif weeks == 1:
         return '1 week ago'
      elif weeks > 1:
         return '{} weeks ago'.format(weeks)
      elif diff.days == 1:
         return '1 day ago'
      elif diff.days > 1:
         return '{} days ago'.format(diff.days)
      elif s <= 1:
         return 'just now'
      elif s < 60:
         return '{} seconds ago'.format(s)
      elif s < 120:
         return '1 minute ago'
      elif s < 3600:
         return '{} minutes ago'.format(s/60)
      elif s < 7200:
         return '1 hour ago'
      else:
         return '{} hours ago'.format(s/3600)

   # If happening time is in the FUTURE
   else:
      diff = naive_post_date - naive_now
      s = diff.seconds
      weeks = diff.days/7
      months = diff.days/30
      years = diff.days/365

      if diff.days > 1000 or diff.days < 0:
         return post_date.strftime('%d %b %y')
      elif years == 1:
         return 'in 1 year'
      elif years > 1:
         return 'in {} years'.format(years)
      elif months == 1:
         return 'in 1 month'
      elif months > 1:
         return 'in {} months'.format(months)
      elif weeks == 1:
         return 'in 1 week'
      elif weeks > 1:
         return 'in {} weeks'.format(weeks)
      elif diff.days == 1:
         return 'in 1 day'
      elif diff.days > 1:
         return 'in {} days'.format(diff.days)
      elif s <= 1:
         return 'just now'
      elif s < 60:
         return 'in {} seconds'.format(s)
      elif s < 120:
         return 'in 1 minute'
      elif s < 3600:
         return 'in {} minutes'.format(s/60)
      elif s < 7200:
         return 'in 1 hour'
      else:
         return 'in {} hours'.format(s/3600)




arrBad = [
'2g1c',
'2 girls 1 cup',
'acrotomophilia',
'anal',
'anilingus',
'anus',
'arsehole',
'ass',
'asshole',
'assmunch',
'auto erotic',
'autoerotic',
'babeland',
'baby batter',
'ball gag',
'ball gravy',
'ball kicking',
'ball licking',
'ball sack',
'ball sucking',
'balls',
'bangbros',
'bareback',
'barely legal',
'barenaked',
'bastardo',
'bastinado',
'bbw',
'bdsm',
'beaver cleaver',
'beaver lips',
'bestiality',
'bi curious',
'big black',
'big breasts',
'big knockers',
'big tits',
'bimbos',
'birdlock',
'bitch',
'black cock',
'blonde action',
'blonde on blonde action',
'blow j',
'blow your l',
'blue waffle',
'blumpkin',
'bollocks',
'bondage',
'boner',
'boob',
'boobs',
'booty call',
'brown showers',
'brunette action',
'bukkake',
'bulldyke',
'bullet vibe',
'bung hole',
'bunghole',
'busty',
'butt',
'buttcheeks',
'butthole',
'camel toe',
'camgirl',
'camslut',
'camwhore',
'carpet muncher',
'carpetmuncher',
'chocolate rosebuds',
'circlejerk',
'cleveland steamer',
'clit',
'clitoris',
'clover clamps',
'clusterfuck',
'cock',
'cocks',
'coprolagnia',
'coprophilia',
'cornhole',
'cum',
'cumming',
'cunnilingus',
'cunt',
'darkie',
'date rape',
'daterape',
'deep throat',
'deepthroat',
'dick',
'dildo',
'dirty pillows',
'dirty sanchez',
'dog style',
'doggie style',
'doggiestyle',
'doggy style',
'doggystyle',
'dolcett',
'domination',
'dominatrix',
'dommes',
'donkey punch',
'double dong',
'double penetration',
'dp action',
'eat my ass',
'ecchi',
'ejaculation',
'erotic',
'erotism',
'escort',
'ethical slut',
'eunuch',
'faggot',
'fecal',
'felch',
'fellatio',
'feltch',
'female squirting',
'femdom',
'figging',
'fingering',
'fisting',
'foot fetish',
'footjob',
'frotting',
'fuck',
'fucking',
'fuck buttons',
'fudge packer',
'fudgepacker',
'futanari',
'g-spot',
'gang bang',
'gay sex',
'genitals',
'giant cock',
'girl on',
'girl on top',
'girls gone wild',
'goatcx',
'goatse',
'gokkun',
'golden shower',
'goo girl',
'goodpoop',
'goregasm',
'grope',
'group sex',
'guro',
'hand job',
'handjob',
'hard core',
'hardcore',
'hentai',
'homoerotic',
'honkey',
'hooker',
'hot chick',
'how to kill',
'how to murder',
'huge fat',
'humping',
'incest',
'intercourse',
'jack off',
'jail bait',
'jailbait',
'jerk off',
'jigaboo',
'jiggaboo',
'jiggerboo',
'jizz',
'juggs',
'kike',
'kinbaku',
'kinkster',
'kinky',
'knobbing',
'leather restraint',
'leather straight jacket',
'lemon party',
'lolita',
'lovemaking',
'make me come',
'male squirting',
'masturbate',
'menage a trois',
'milf',
'missionary position',
'motherfucker',
'mound of venus',
'mr hands',
'muff diver',
'muffdiving',
'nambla',
'nawashi',
'negro',
'neonazi',
'nig nog',
'nigga',
'nigger',
'nimphomania',
'nipple',
'nipples',
'nsfw images',
'nude',
'nudity',
'nympho',
'nymphomania',
'octopussy',
'omorashi',
'one cup two girls',
'one guy one jar',
'orgasm',
'orgy',
'paedophile',
'panties',
'panty',
'pedobear',
'pedophile',
'pegging',
'penis',
'phone sex',
'piece of shit',
'piss pig',
'pissing',
'pisspig',
'playboy',
'pleasure chest',
'pole smoker',
'ponyplay',
'poof',
'poop chute',
'poopchute',
'porn',
'porno',
'pornography',
'prince albert piercing',
'pthc',
'pubes',
'pussy',
'queaf',
'raghead',
'raging boner',
'rape',
'raping',
'rapist',
'rectum',
'reverse cowgirl',
'rimjob',
'rimming',
'rosy palm',
'rosy palm and her 5 sisters',
'rusty trombone',
's&m',
'sadism',
'scat',
'schlong',
'scissoring',
'semen',
'sex',
'sexo',
'sexy',
'shaved beaver',
'shaved pussy',
'shemale',
'shibari',
'shit',
'shota',
'shrimping',
'slanteye',
'slut',
'smut',
'snatch',
'snowballing',
'sodomize',
'sodomy',
'spic',
'spooge',
'spread legs',
'strap on',
'strapon',
'strappado',
'strip club',
'style doggy',
'suck',
'sucks',
'suicide girls',
'sultry women',
'swastika',
'swinger',
'tainted love',
'taste my',
'tea bagging',
'threesome',
'throating',
'tied up',
'tight white',
'tit',
'tits',
'titties',
'titty',
'tongue in a',
'topless',
'tosser',
'towelhead',
'tranny',
'tribadism',
'tub girl',
'tubgirl',
'tushy',
'twat',
'twink',
'twinkie',
'two girls one cup',
'undressing',
'upskirt',
'urethra play',
'urophilia',
'vagina',
'venus mound',
'vibrator',
'violet blue',
'violet wand',
'vorarephilia',
'voyeur',
'vulva',
'wank',
'wet dream',
'wetback',
'white power',
'women rapping',
'wrapping men',
'wrinkled starfish',
'xx',
'xxx',
'yaoi',
'yellow showers',
'yiffy',
'zoophilia']

def profanityFilter(text):
   brokenStr1 = text.split()
   
   count = 0

   for word in brokenStr1:
      if arrBad.__contains__(word):
        count = count + 1

   return count
