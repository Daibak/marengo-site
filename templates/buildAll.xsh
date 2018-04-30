#!/usr/bin/env xonsh

comp = ['index', 'contrattualistica', 'diritto-condominiale',
        'diritto-intellettuale', 'diritto-famiglia',
        'diritto-successorio', 'diritto-assicurativo',
        'diritto-immobiliare', 'recupero-credito', 'diritto-lavoro']

for c in comp:
    genFromTemplate generic.tpl -i base.yaml ./competenze/base.yaml @('./competenze/' + c + '.yaml') -o @('../www/competenze/' + c + '.html')

genFromTemplate index.tpl -i base.yaml index.yaml -o ../www/index.html
