from reader import PageReader


f = open('links.txt', 'w')

base_url = 'https://informatica.mercadolivre.com.br/portateis/notebook/notebook_Desde_'
user_id = ''#'_CustId_20173305_seller*id_20173305'
#'http://informatica.mercadolivre.com.br/_Desde_' + str(idx) \
#        + '_CustId_20173305_seller*id_20173305'
filter_in = ('apple')
filter_out = ('173', '17', 'touch', 'omen', 'gamer')
for idx in range(1,50):
    pg = PageReader(base_url + str(idx) + user_id,
        ['<a.*?href\s*=\s*["\']([^"\'>]+-[^"\'>]*)["\'][^>]*>.*?<\/a>'],
        [], [])

    links = pg.get_links()
    #f.write(links)

    for l in links:
        is_in = True
        for fo in filter_out:
            if fo.upper() in l.upper():
                is_in = False
                continue

        if is_in:
            for fi in filter_in:
                if not fi.upper() in l.upper():
                    is_in = False
                    continue

        if is_in:
            f.write(l + '\n')

f.close()

#<a.*?href\s*=\s*["\']([^"\'>]+(i7-dell)[^"\'>]*)["\'][^>]*>.*?<\/a>
