from nltk.corpus import stopwords

fin_stops = set(stopwords.words('finnish'))
fin_stops.update(['hei', 'moi', 'moikka', 'moro', 'tervehdys', 'terve', 'terveisin', 'siis', 'myös', 'kiitos',
                     'kiitoksia', 'kiitosta', 'ok', 'eli', 'okei', 'no', 'sitten', 'jo', 'vielä', 'aina', 'jotta'])
del_from_finstops = ['en', 'et', 'ei', 'emme', 'ette', 'eivät']
for word in del_from_finstops: fin_stops.remove(word)

swe_stops = set(stopwords.words('swedish'))
swe_stops.remove('min')

en_stops = set(stopwords.words('english'))
del_from_enstops = ['on', 'as', 'a', 'd', 'm', 'o', 's', 't', 'me', 'no', 'y']
for word in del_from_enstops: en_stops.remove(word)

email_stops = set(['mailto', 'subject', 'from', 'to', 'vs', 'message',
                      'original', 'date', 're', 'terv', 'sent', 'from', 'kello'])
final_stops = fin_stops|email_stops # Stopwords used for text preprocessing

