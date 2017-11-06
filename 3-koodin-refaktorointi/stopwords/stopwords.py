from nltk.corpus import stopwords

fin_stops = set(stopwords.words('finnish'))
fin_extras = set('''hei moi moikka moro tervehdys terve terveisin siis myös kiitos
         kiitoksia kiitosta ok eli okei no sitten jo vielä aina jotta'''.split())
fin_stops.update(fin_extras)
del_from_finstops = set('en et ei emme ette eivät'.split())
for word in del_from_finstops: fin_stops.remove(word)

swe_stops = set(stopwords.words('swedish'))
swe_stops.remove('min')

en_stops = set(stopwords.words('english'))
del_from_enstops = set('on as a d m o s t me no y'.split())
for word in del_from_enstops: en_stops.remove(word)

email_stops = set('''mailto subject from to vs message
         original date re terv sent from kello'''.split())
final_stops = fin_stops|email_stops # Stopwords used for text preprocessing

