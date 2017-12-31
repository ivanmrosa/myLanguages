from reader import PageReader


f = open('links.txt', 'w')

filter_in = ('ssd', 'i7', 'asus')
filter_out = ('8gb', 'omen', '173')
for idx in range(1,29):
    pg = PageReader('http://informatica.mercadolivre.com.br/_Desde_' + str(idx) \
        + '_CustId_20173305_seller*id_20173305',
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
