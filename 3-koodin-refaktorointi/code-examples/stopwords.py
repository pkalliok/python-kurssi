from nltk.corpus import stopwords

fin_extras = set('''hei moi moikka moro tervehdys terve terveisin siis myös kiitos
         kiitoksia kiitosta ok eli okei no sitten jo vielä aina jotta'''.split())
del_from_finstops = set('en et ei emme ette eivät'.split())
fin_stops = set(stopwords.words('finnish')) - del_from_finstops | fin_extras

swe_stops = set(stopwords.words('swedish')) - set(('min',))

del_from_enstops = set('on as a d m o s t me no y'.split())
en_stops = set(stopwords.words('english')) - del_from_enstops

email_stops = set('''mailto subject from to vs message
         original date re terv sent from kello'''.split())
final_stops = fin_stops | email_stops # Stopwords used for text preprocessing

