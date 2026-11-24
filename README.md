# CRY Labo 1

## 1. Quel est l’avantage d’utiliser le test du χ2 plutôt que de comparer simplement la lettre la plus fréquente dans le texte chiffré par rapport aux statistiques du langage de base ?

L'avantage est que le test du χ2 prend en compte l'ensemble des fréquences des lettres au lieu de se concentrer
uniquement sur la lettre la plus fréquente. Cela permet d'avoir une meilleure idée de la distribution des lettres dans
le
texte chiffré et donc de mieux déterminer la clef utilisée pour le chiffrement.

## 2. Pourquoi est-ce que le test du χ2 ne fonctionne-t-il pas directement sur un texte chiffré à l’aide du chiffre de Vigenère ?

Parce que chaque lettre du texte chiffré est décalée par une valeur différente en fonction de la clé utilisée. Ce qui
signifie que la fréquence des lettres dans le texte chiffré n'est pas représentative de la fréquence des lettres dans la
le texte clair.

## 3. Que mesure l’indice de coïncidence ?

L'indice de coïncidence mesure la probabilité que deux caractères choisis au hasard dans un texte soient identiques.

## 4. Pourquoi est-ce que l’indice de coïncidence n’est-il pas modifié lorsque l’on applique le chiffre de César généralisé sur un texte ?

Parce que le chiffre de César généralisé ne modifie pas la distribution des lettres dans le texte chiffré. Il décale
simplement chaque lettre du texte clair par une valeur fixe.

## 5. Est-il possible de coder un logiciel permettant de décrypter un document chiffré avec le chiffre de Vigenère et une clef ayant la même taille que le texte clair ? Justifiez.

Non. En effet, cela correspond au chiffrement du masque jetable qui est une méthode de chiffrement inconditionnellement
sûre. Étant donné que la clé n'est pas répétée, il n'y a aucun moyen de la retrouver et donc de déchiffrer le texte.

## 6. Expliquez votre attaque sur la version améliorée du chiffre de Vigenère

J'ai commencé par poser mathématiquement la méthode de chiffrement.

- **Mi** : texte clair du bloc i, par exemple M1 = LACRYP
- **Ki** : clé du bloc i, par exemple K1 = MAISON
- **Ci** : texte chiffré du bloc i, par exemple C1 = XAKJMC

```
C1 = M1 + K1 
K2 = K1 + C1
C2 = M2 + K2 = M2 + K1 + C1
K3 = K2 + C2
C3 = M3 + K3 = M3 + K1 + C1 + C2
```

*Note : + représente l'action de chiffrement et - l'action de déchiffrement.*

Nous pouvons voir que si nous déchiffrons C2 avec C1, nous obtenons M2 + K1. De même, si nous déchiffrons C3 avec C1
chiffré avec C2, nous obtenons M3 + K1. Cela nous permet de revenir à un chiffrement de Vigenère classique qui réutilise
la clé K1 à chaque bloc.

```
C2 - C1 = M2 + K1
C3 - (C1 + C2) = M3 + K1
Cn - (C1 + … + Cn-1) = Mn + K1, n > 1
```

Pour trouver la clé, il faut grouper tous les "nouveaux" blocs (C1, C2 - C1, C3 - (C1 + C2), ...) en un seul texte pour
chaque longueur de clé possible, de 1 à 20 dans notre cas. Ainsi, nous avons 20 textes chiffrés différents. Pour chaque
texte chiffré, nous calculons la moyenne des indices de coïncidence pour chaque longueur de clé possible. La moyenne la
plus proche de l'indice de coïncidence de notre texte de référence nous donne la longueur de la clé utilisée pour
chiffrer le texte. Enfin, nous pouvons appliquer une attaque par fréquence pour retrouver la clé.

## 7. Trouvez une méthode statistique (proche de ce qu’on a vu dans ce labo) permettant de distinguer un texte en anglais d’un texte en français. Qu’en pensez-vous ? Testez votre méthode et présentez les résultats.

Une méthode consiste à calculer χ2 pour un texte en anglais et un texte en français en utilisant les fréquences des
lettres du texte à analyser. Il suffit ensuite de comparer l'indice de coïncidence du texte à analyser avec les indices
de coïncidence des textes en anglais et en français ainsi que les deux χ2.

La fonction suivante permet de détérminer si un texte est en anglais ou en français :

```python
def guess_text_language(text, ref_freq_fr, ref_ci_fr, ref_freq_en, ref_ci_en):
    """
    Parameters
    ----------
    text: the text to analyse
    ref_freq_fr: the output of the freq_analysis function on a reference French text
    ref_ci_fr: the output of the coincidence_index function on a reference French text
    ref_freq_en: the output of the freq_analysis function on a reference English text
    ref_ci_en: the output of the coincidence_index function on a reference English text

    Returns
    -------
    the language of the text
    """
    if len(text) == 0:
        print("The text is empty")
        return ''

    text_freq = freq_analysis(text)
    text_ci = coincidence_index(text)

    chi2_fr = sum((f - r) ** 2 / r if r != 0 else 1 for f, r in zip(text_freq, ref_freq_fr))
    chi2_en = sum((f - r) ** 2 / r if r != 0 else 1 for f, r in zip(text_freq, ref_freq_en))

    if abs(text_ci - ref_ci_fr) < abs(text_ci - ref_ci_en) and chi2_fr < chi2_en:
        return "French"
    else:
        return "English"
```

En utilisant comme référence les textes `ref_text.txt` pour le français et `ref_text_en.txt` pour l'anglais, nous
obtenons les résultats suivants :

```python
    text_en = """
        From the physiologist's or psychologist's point of view we may seem to
        be making an unwarrantable abstraction in desiring to handle the subject
        of speech without constant and explicit reference to that basis.
        However, such an abstraction is justifiable. We can profitably discuss
        the intention, the form, and the history of speech, precisely as we
        discuss the nature of any other phase of human culture--say art or
        religion--as an institutional or cultural entity, leaving the organic
        and psychological mechanisms back of it as something to be taken for
        granted. Accordingly, it must be clearly understood that this
        introduction to the study of speech is not concerned with those aspects
        of physiology and of physiological psychology that underlie speech. Our
        study of language is not to be one of the genesis and operation of a
        concrete mechanism; it is, rather, to be an inquiry into the function
        and form of the arbitrary systems of symbolism that we term languages.
    """
text_en = sanitize_text(text_en)
print("English text:", guess_text_language(text_en, ref_freq, ref_ci, ref_freq_en, ref_ci_en))
```

```
English text: English
```

```python
    text_fr = """
        Je le pris par la main, cet excellent jeune homme. Je le fis asseoir sur
        le meilleur banc du jardin, car nous en avons deux. Il m’apprit qu’il
        était botaniste et qu’il avait une mission du Jardin des Plantes de
        Hambourg. Tout en complétant son herbier, il avait observé de son mieux
        le pays, les bêtes et les gens. Ses descriptions naïves, ses vues,
        courtes mais justes, me rappelaient un peu la manière du bonhomme
        Hérodote. Il s’exprimait lourdement, mais avec une candeur qui imposait
        la confiance; il appuyait sur ses paroles du ton d’un homme profondément
        convaincu. Il put me donner des nouvelles, sinon de toute la ville
        d’Athènes, au moins des principaux personnages que j’ai nommés dans mon
        livre. Dans le cours de la conversation, il énonça quelques idées
        générales qui me parurent d’autant plus judicieuses que je les avais
        développées avant lui. Au bout d’une heure d’entretien, nous étions
        intimes.
    """
text_fr = sanitize_text(text_fr)
print("French text:", guess_text_language(text_fr, ref_freq, ref_ci, ref_freq_en, ref_ci_en))
```

```
French text: French
```

Cette méthode est rapide et simple à implémenter, mais elle présente quelques limitations. En effet, elle ne fonctionne
pas bien sur les textes courts et les textes qui ne sont pas représentatifs de la langue comme les textes techniques ou
les textes poétiques. D'autre part, cette méthode peut induire des erreurs si les langues ont des fréquences de lettres
similaires.

> 8. Quelles étaient les clefs et les textes clairs correspondants aux textes chiffrés dans les fichiers vigenere.txt et
     vigenere_improved.txt ?

**vigenere.txt**

Clef: `ASTERIXOBELIX`

Texte clair :

`VOUSSAVEZMOIJENECROISPASQUILYAITDEBONNEOUDEMAUVAISESITUATIONMOISIJEDEVAISRESUMERMAVIEAUJOURDHUIAVECVOUSJEDIRAISQUECESTDABORDDESRENCONTRESDESGENSQUIMONTTENDULAMAINPEUTETREAUNMOMENTOUJENEPOUVAISPASOUJETAISSEULCHEZMOIETCESTASSEZCURIEUXDESEDIREQUELESHASARDSLESRENCONTRESFORGENTUNEDESTINEEPARCEQUEQUANDONALEGOUTDELACHOSEQUANDONALEGOUTDELACHOSEBIENFAITELEBEAUGESTEPARFOISONNETROUVEPASLINTERLOCUTEURENFACEJEDIRAISLEMIROIRQUIVOUSAIDEAAVANCERALORSCANESTPASMONCASCOMMEJEDISAISLAPUISQUEMOIAUCONTRAIREJAIPUETJEDISMERCIALAVIEJELUIDISMERCIJECHANTELAVIEJEDANSELAVIEJENESUISQUAMOURETFINALEMENTQUANDDESGENSMEDISENTMAISCOMMENTFAISTUPOURAVOIRCETTEHUMANITEJELEURREPONDSTRESSIMPLEMENTQUECESTCEGOUTDELAMOURCEGOUTDONCQUIMAPOUSSEAUJOURDHUIAENTREPRENDREUNECONSTRUCTIONMECANIQUEMAISDEMAINQUISAITPEUTETRESIMPLEMENTAMEMETTREAUSERVICEDELACOMMUNAUTEAFAIRELEDONLEDONDESOI`

**vigenere_improved.txt**

Clef: `JUSTELEBLANC`

Texte clair :

`JEPRENDSLACCENTBELGENONALLOOPOURRAISJEPARLERAMONSIEURLEBLANCJUSTEUNEFOECESTMOIBONSOERMONSIEURLEBLANCGEORGEVANBRUGELALAPPAREILJEVOUSAPPELLEPARCEQUEJESUISPRODUCTEURNESTCEPASJARRIVEDEBELGIQUEUNEFOEETJESUISTRESINTERESSEPARVOTREROMANVOTREROMANLEPETITCHEVALDEMANEGELEPETITCHEVALDEMANEGEETJAIMERAISDISCUTERLACHATDESDROEPOURLECINEMECESTUNEBLAGUEOUQUOINONNONPASDUTOUTPOURQUOIUNEBLEGUE`