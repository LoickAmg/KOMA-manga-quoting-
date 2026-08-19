from django.core.management.base import BaseCommand

from quotes.models import Quote, Theme, TranslationOrigin

# Traductions françaises : rendues par IA pour ce projet (pas issues des
# doublages/sous-titrages officiels ni relues par un locuteur natif), donc
# marquées TranslationOrigin.ASSISTED. Un rendu fidèle au sens plutôt qu'une
# traduction mot à mot a été privilégié.
ASSISTED = TranslationOrigin.ASSISTED

QUOTES = [
    # Naruto
    (
        "I'm not gonna run away, I never go back on my word! That's my nindo: my ninja way!",
        "Je ne fuirai jamais, je ne reviens jamais sur ma parole ! C'est ça, mon nindo, ma voie du ninja !",
        "Naruto Uzumaki",
        "Naruto",
        Theme.DETERMINATION,
    ),
    (
        "People's lives don't end when they die. It ends when they lose faith.",
        "La vie des gens ne s'arrête pas à leur mort. Elle s'arrête quand ils perdent la foi.",
        "Itachi Uchiha",
        "Naruto",
        Theme.WISDOM,
    ),
    (
        "Those who break the rules are scum, but those who abandon their friends are worse than scum.",
        "Ceux qui enfreignent les règles sont des moins que rien, mais ceux qui abandonnent leurs amis sont pires que des moins que rien.",
        "Kakashi Hatake",
        "Naruto",
        Theme.FRIENDSHIP,
    ),
    (
        "It's not the face that makes someone a monster; it's the choices they make with their lives.",
        "Ce n'est pas le visage qui fait de quelqu'un un monstre, ce sont les choix qu'il fait dans sa vie.",
        "Gaara",
        "Naruto",
        Theme.WISDOM,
    ),
    # One Piece
    (
        "I don't want to conquer anything. I just think the guy with the most freedom in this whole ocean is the Pirate King!",
        "Je ne veux rien conquérir. Je pense juste que celui qui est le plus libre sur cet océan, c'est lui le Roi des Pirates !",
        "Monkey D. Luffy",
        "One Piece",
        Theme.FREEDOM,
    ),
    (
        "If you don't take risks, you can't create a future.",
        "Si on ne prend pas de risques, on ne peut pas se créer d'avenir.",
        "Monkey D. Luffy",
        "One Piece",
        Theme.DETERMINATION,
    ),
    (
        "Nothing happened.",
        "Il ne s'est rien passé.",
        "Roronoa Zoro",
        "One Piece",
        Theme.DEFIANCE,
    ),
    (
        "Thank you... for loving me.",
        "Merci... de m'avoir aimé.",
        "Portgas D. Ace",
        "One Piece",
        Theme.LOSS,
    ),
    # Fullmetal Alchemist: Brotherhood
    (
        "A lesson without pain is meaningless. That is because no one can gain without sacrificing something.",
        "Une leçon sans douleur n'a aucun sens, car on ne peut rien gagner sans sacrifier quelque chose.",
        "Edward Elric",
        "Fullmetal Alchemist: Brotherhood",
        Theme.WISDOM,
    ),
    (
        "The world is not perfect. But it's there for us, doing the best it can. That's what makes it so damn beautiful.",
        "Le monde n'est pas parfait. Mais il est là pour nous, il fait de son mieux. C'est ce qui le rend si merveilleusement beau.",
        "Roy Mustang",
        "Fullmetal Alchemist: Brotherhood",
        Theme.WISDOM,
    ),
    # Attack on Titan
    (
        "The only thing we're allowed to do is believe that we won't regret the choice we made.",
        "La seule chose qu'il nous reste à faire, c'est croire que nous ne regretterons pas le choix que nous avons fait.",
        "Levi Ackerman",
        "Attack on Titan",
        Theme.DETERMINATION,
    ),
    (
        "If you win, you live. If you lose, you die. If you don't fight, you can't win.",
        "Si tu gagnes, tu vis. Si tu perds, tu meurs. Si tu ne combats pas, tu ne peux pas gagner.",
        "Eren Yeager",
        "Attack on Titan",
        Theme.DEFIANCE,
    ),
    (
        "The world is cruel... and also very beautiful.",
        "Le monde est cruel... et pourtant si beau.",
        "Mikasa Ackerman",
        "Attack on Titan",
        Theme.WISDOM,
    ),
    # Death Note
    (
        "I am justice!",
        "Je suis la justice !",
        "Light Yagami",
        "Death Note",
        Theme.AMBITION,
    ),
    (
        "There are many kinds of monsters in this world, and I am one of them.",
        "Il existe de nombreuses sortes de monstres dans ce monde, et j'en suis un.",
        "L Lawliet",
        "Death Note",
        Theme.WISDOM,
    ),
    # My Hero Academia
    (
        "It's fine to cry, but eventually you'll have to look forward and take a step to move on.",
        "C'est normal de pleurer, mais à un moment donné, il faut regarder devant soi et faire un pas pour avancer.",
        "Izuku Midoriya",
        "My Hero Academia",
        Theme.DETERMINATION,
    ),
    (
        "When you fall down seven times, you stand up eight.",
        "Quand on tombe sept fois, on se relève huit fois.",
        "All Might",
        "My Hero Academia",
        Theme.DETERMINATION,
    ),
    # Dragon Ball
    (
        "I am the Prince of all Saiyans!",
        "Je suis le prince de tous les Saiyans !",
        "Vegeta",
        "Dragon Ball Z",
        Theme.AMBITION,
    ),
    # Berserk
    (
        "Even if I bathe in the blood of my enemies, I am no match for the darkness which lies within my own heart.",
        "Même si je me baignais dans le sang de mes ennemis, je ne ferais pas le poids face aux ténèbres qui habitent mon propre cœur.",
        "Guts",
        "Berserk",
        Theme.DEFIANCE,
    ),
    # Neon Genesis Evangelion
    (
        "I mustn't run away.",
        "Je ne dois pas fuir.",
        "Shinji Ikari",
        "Neon Genesis Evangelion",
        Theme.DETERMINATION,
    ),
    (
        "I think I was born to meet you. That is what I feel now.",
        "Je crois que je suis né pour te rencontrer. C'est ce que je ressens, maintenant.",
        "Kaworu Nagisa",
        "Neon Genesis Evangelion",
        Theme.FRIENDSHIP,
    ),
    # Cowboy Bebop
    (
        "Whatever happens, happens.",
        "Quoi qu'il arrive, il arrive.",
        "Spike Spiegel",
        "Cowboy Bebop",
        Theme.FREEDOM,
    ),
    (
        "I'm not going there to die. I'm going to find out if I'm really alive.",
        "Je ne vais pas là-bas pour mourir. Je vais découvrir si je suis vraiment vivant.",
        "Spike Spiegel",
        "Cowboy Bebop",
        Theme.DETERMINATION,
    ),
    # JoJo's Bizarre Adventure
    (
        "Yare yare daze.",
        "Et voilà autre chose...",
        "Jotaro Kujo",
        "JoJo's Bizarre Adventure",
        Theme.DEFIANCE,
    ),
    (
        "Useless! Useless! Useless!",
        "Inutile ! Inutile ! Inutile !",
        "Dio Brando",
        "JoJo's Bizarre Adventure",
        Theme.AMBITION,
    ),
    (
        "It was me, Dio!",
        "C'était moi, Dio !",
        "Joseph Joestar",
        "JoJo's Bizarre Adventure",
        Theme.DEFIANCE,
    ),
    # Vinland Saga
    (
        "You have no enemies. Nobody has enemies. There isn't a single person in this world who needs to be hurt.",
        "Tu n'as aucun ennemi. Personne n'a d'ennemi. Il n'y a pas une seule personne dans ce monde qui mérite d'être blessée.",
        "Thors",
        "Vinland Saga",
        Theme.WISDOM,
    ),
    # Demon Slayer
    (
        "No matter how many people you may lose, you have no choice but to keep on living.",
        "Peu importe combien de personnes tu perdras, tu n'as pas d'autre choix que de continuer à vivre.",
        "Tanjiro Kamado",
        "Demon Slayer",
        Theme.LOSS,
    ),
    (
        "Set your heart ablaze!",
        "Embrase ton cœur !",
        "Kyojuro Rengoku",
        "Demon Slayer",
        Theme.DETERMINATION,
    ),
    # Bleach
    (
        "If I don't wield the sword, I can't protect you. If I keep wielding it, I can't embrace you.",
        "Si je ne manie pas l'épée, je ne peux pas te protéger. Si je continue à la manier, je ne peux pas te serrer dans mes bras.",
        "Ichigo Kurosaki",
        "Bleach",
        Theme.LOSS,
    ),
    # Fullmetal Alchemist (extra)
    (
        "Human lives are not eternal. That is precisely why we live our lives to the fullest, right now, this instant.",
        "La vie humaine n'est pas éternelle. C'est précisément pour ça qu'on doit vivre pleinement, ici et maintenant, à cet instant précis.",
        "Riza Hawkeye",
        "Fullmetal Alchemist: Brotherhood",
        Theme.WISDOM,
    ),
    # My Hero Academia (extra)
    (
        "A hero is someone who keeps moving forward, no matter what.",
        "Un héros, c'est quelqu'un qui continue d'avancer, quoi qu'il arrive.",
        "Katsuki Bakugo",
        "My Hero Academia",
        Theme.DETERMINATION,
    ),
    # Attack on Titan (extra)
    (
        "This world is merciless... and also, very beautiful.",
        "Ce monde est impitoyable... et pourtant si beau.",
        "Armin Arlert",
        "Attack on Titan",
        Theme.WISDOM,
    ),
    # One Piece (extra)
    (
        "Inherited will, the destiny of the age, the dreams of its people. These things cannot be stopped.",
        "La volonté héritée, le destin de l'époque, les rêves de son peuple. Ces choses-là, rien ne peut les arrêter.",
        "Gol D. Roger",
        "One Piece",
        Theme.AMBITION,
    ),
    # --- Extension : 39 citations supplémentaires, sur des séries jusque-là
    # absentes. Sélectionnées à la main avec la même exigence que le lot
    # initial (je ne les inclus que si je suis confiant sur leur authenticité
    # et leur attribution) — donc pas de tentative d'atteindre 500-1000 en
    # import massif : voir le README pour le contexte de cette décision.
    # Hunter x Hunter
    (
        "If I was trying to trick you, I wouldn't have been shaking.",
        "Si j'avais essayé de te tromper, je n'aurais pas tremblé.",
        "Gon Freecss",
        "Hunter x Hunter",
        Theme.DEFIANCE,
    ),
    (
        "In order to know true peace, one must experience the exact opposite of peace.",
        "Pour connaître la véritable paix, il faut d'abord connaître son exact opposé.",
        "Chrollo Lucilfer",
        "Hunter x Hunter",
        Theme.WISDOM,
    ),
    (
        "Even if my body rots, my resolve will never rot.",
        "Même si mon corps pourrit, ma détermination ne pourrira jamais.",
        "Killua Zoldyck",
        "Hunter x Hunter",
        Theme.DETERMINATION,
    ),
    # One Punch Man
    (
        "I just became a hero for fun.",
        "Je suis juste devenu un héros pour le plaisir.",
        "Saitama",
        "One Punch Man",
        Theme.FREEDOM,
    ),
    (
        "The reason I've become this strong is simply because I wanted to be able to defeat any enemy in one punch.",
        "Si je suis devenu aussi fort, c'est simplement parce que je voulais pouvoir vaincre n'importe quel ennemi d'un seul coup de poing.",
        "Saitama",
        "One Punch Man",
        Theme.DETERMINATION,
    ),
    # Code Geass
    (
        "This world is rotten. And those who are making it rot deserve to die.",
        "Ce monde est pourri. Et ceux qui le font pourrir méritent de mourir.",
        "Lelouch vi Britannia",
        "Code Geass",
        Theme.DEFIANCE,
    ),
    (
        "I, Lelouch vi Britannia, command you.",
        "Moi, Lelouch vi Britannia, je te l'ordonne.",
        "Lelouch vi Britannia",
        "Code Geass",
        Theme.AMBITION,
    ),
    # Fairy Tail
    (
        "When you can't run anymore, then crawl. And if you can't crawl either, then I'll carry you on my back!",
        "Quand tu ne peux plus courir, alors rampe. Et si tu ne peux même plus ramper, je te porterai sur mon dos !",
        "Natsu Dragneel",
        "Fairy Tail",
        Theme.FRIENDSHIP,
    ),
    (
        "The past is the past. All you can do is control the present, moving forward.",
        "Le passé est le passé. Tout ce que tu peux faire, c'est maîtriser le présent, en avançant.",
        "Erza Scarlet",
        "Fairy Tail",
        Theme.WISDOM,
    ),
    # Sword Art Online
    (
        "If you can't accept reality, you might as well continue to dream.",
        "Si tu ne peux pas accepter la réalité, autant continuer à rêver.",
        "Kirito",
        "Sword Art Online",
        Theme.WISDOM,
    ),
    # Tokyo Ghoul
    (
        "It's not the world that's messed up, it's those of us in it.",
        "Ce n'est pas le monde qui est détraqué, ce sont ceux qui y vivent.",
        "Kaneki Ken",
        "Tokyo Ghoul",
        Theme.WISDOM,
    ),
    # Trigun
    (
        "The only thing that can beat hatred... is love.",
        "La seule chose capable de vaincre la haine... c'est l'amour.",
        "Vash the Stampede",
        "Trigun",
        Theme.WISDOM,
    ),
    # Puella Magi Madoka Magica
    (
        "There's no logical reason to feel remorse. I merely made a suggestion that was beneficial to both parties.",
        "Il n'y a aucune raison logique d'éprouver du remords. Je n'ai fait qu'une proposition bénéfique aux deux parties.",
        "Kyubey",
        "Puella Magi Madoka Magica",
        Theme.DEFIANCE,
    ),
    # Steins;Gate
    (
        "El Psy Kongroo.",
        "El Psy Kongroo.",
        "Okabe Rintarou",
        "Steins;Gate",
        "",
    ),
    # Re:Zero
    (
        "However many times it takes, I will save you.",
        "Peu importe combien de fois il le faudra, je te sauverai.",
        "Subaru Natsuki",
        "Re:Zero",
        Theme.DETERMINATION,
    ),
    # Jujutsu Kaisen
    (
        "Throughout heaven and earth, I alone am the honored one.",
        "Dans les cieux comme sur la terre, je suis le seul digne d'honneur.",
        "Satoru Gojo",
        "Jujutsu Kaisen",
        Theme.AMBITION,
    ),
    # Black Clover
    (
        "I'm gonna be the Wizard King!",
        "Je vais devenir l'Empereur-Mage !",
        "Asta",
        "Black Clover",
        Theme.AMBITION,
    ),
    # Rurouni Kenshin
    (
        "I will never kill again.",
        "Je ne tuerai plus jamais.",
        "Kenshin Himura",
        "Rurouni Kenshin",
        Theme.DETERMINATION,
    ),
    # Slam Dunk
    (
        "I want to be the best in Japan!",
        "Je veux devenir le meilleur du Japon !",
        "Hanamichi Sakuragi",
        "Slam Dunk",
        Theme.AMBITION,
    ),
    # Yu Yu Hakusho
    (
        "It doesn't matter if you're a demon, a human, or whatever else — the only thing that matters is whether your heart is strong.",
        "Peu importe qu'on soit un démon, un humain, ou autre chose — la seule chose qui compte, c'est la force de son cœur.",
        "Yusuke Urameshi",
        "Yu Yu Hakusho",
        Theme.WISDOM,
    ),
    # Hajime no Ippo
    (
        "I'm not a genius. I'm a man who works harder than a genius.",
        "Je ne suis pas un génie. Je suis un homme qui travaille plus dur qu'un génie.",
        "Ippo Makunouchi",
        "Hajime no Ippo",
        Theme.DETERMINATION,
    ),
    # Princess Mononoke
    (
        "Look at me with eyes unclouded by hate.",
        "Regarde-moi avec des yeux que la haine n'a pas voilés.",
        "Ashitaka",
        "Princess Mononoke",
        Theme.WISDOM,
    ),
    # Death Note (extra)
    (
        "Humans are so interesting.",
        "Les humains sont vraiment intéressants.",
        "Ryuk",
        "Death Note",
        "",
    ),
    (
        "Justice will prevail, you say? Of course it will! Because if it doesn't, it wouldn't be justice!",
        "La justice triomphera, dis-tu ? Bien sûr que oui ! Parce que sinon, ce ne serait pas la justice !",
        "L Lawliet",
        "Death Note",
        Theme.DEFIANCE,
    ),
    # Naruto (extra)
    (
        "A dropout will beat a genius through hard work. And I will prove it!",
        "Un cancre peut battre un génie à force de travail. Et je vais le prouver !",
        "Rock Lee",
        "Naruto",
        Theme.DETERMINATION,
    ),
    (
        "When people are protecting something truly special to them, that's when they truly become strong.",
        "C'est quand les gens protègent quelque chose qui leur est vraiment précieux qu'ils deviennent véritablement forts.",
        "Obito Uchiha",
        "Naruto",
        Theme.FRIENDSHIP,
    ),
    # One Piece (extra)
    (
        "I want to live!",
        "Je veux vivre !",
        "Nico Robin",
        "One Piece",
        Theme.FREEDOM,
    ),
    # My Hero Academia (extra)
    (
        "From now on, I'll use whatever power I have—my father's or otherwise—how I see fit! To be the hero I want to be!",
        "À partir de maintenant, j'utiliserai tout mon pouvoir — qu'il vienne de mon père ou d'ailleurs — comme je l'entends ! Pour devenir le héros que je veux être !",
        "Shoto Todoroki",
        "My Hero Academia",
        Theme.DETERMINATION,
    ),
    (
        "Why? Because I am here!",
        "Pourquoi ? Parce que je suis là !",
        "All Might",
        "My Hero Academia",
        Theme.DEFIANCE,
    ),
    # Dragon Ball Z (extra)
    (
        "A true warrior is not motivated by the need to prove himself over and over. A warrior needs, above all else, to fight for those who cannot fight for themselves.",
        "Un vrai guerrier n'a pas besoin de sans cesse se prouver quelque chose. Un guerrier a surtout besoin de se battre pour ceux qui ne peuvent pas se battre eux-mêmes.",
        "Goku",
        "Dragon Ball Z",
        Theme.WISDOM,
    ),
    (
        "I've spent my entire life training to be the best, and I finally understand what it means to fight for someone other than myself.",
        "J'ai passé toute ma vie à m'entraîner pour être le meilleur, et je comprends enfin ce que signifie se battre pour quelqu'un d'autre que soi-même.",
        "Piccolo",
        "Dragon Ball Z",
        Theme.FRIENDSHIP,
    ),
    # Dragon Ball
    (
        "I wanna be the strongest fighter under the sky!",
        "Je veux devenir le combattant le plus fort sous le ciel !",
        "Son Goku",
        "Dragon Ball",
        Theme.AMBITION,
    ),
    # Gurren Lagann
    (
        "Who the hell do you think I am?!",
        "Pour qui tu me prends, bordel ?!",
        "Kamina",
        "Gurren Lagann",
        Theme.DEFIANCE,
    ),
    (
        "Believe in the me that believes in you!",
        "Crois en le moi qui croit en toi !",
        "Simon",
        "Gurren Lagann",
        Theme.FRIENDSHIP,
    ),
    # Spirited Away
    (
        "Once you've met someone, you never really forget them.",
        "Une fois qu'on a rencontré quelqu'un, on ne l'oublie jamais vraiment.",
        "Zeniba",
        "Spirited Away",
        Theme.WISDOM,
    ),
    # Howl's Moving Castle
    (
        "A heart's a heavy burden.",
        "Un cœur, c'est un lourd fardeau.",
        "Howl",
        "Howl's Moving Castle",
        Theme.WISDOM,
    ),
    # JoJo's Bizarre Adventure (extra)
    (
        "I, Giorno Giovanna, have a dream.",
        "Moi, Giorno Giovanna, j'ai un rêve.",
        "Giorno Giovanna",
        "JoJo's Bizarre Adventure",
        Theme.AMBITION,
    ),
    # Assassination Classroom
    (
        "Living is very simple. All you have to do is find something you enjoy doing and put your heart into it.",
        "Vivre, c'est très simple. Il suffit de trouver quelque chose qu'on aime faire et de s'y donner à cœur.",
        "Koro-sensei",
        "Assassination Classroom",
        Theme.WISDOM,
    ),
    # Sailor Moon
    (
        "In the name of the moon, I'll punish you!",
        "Au nom de la Lune, je vais te punir !",
        "Usagi Tsukino",
        "Sailor Moon",
        Theme.DEFIANCE,
    ),
]


class Command(BaseCommand):
    help = "Peuple la base avec un jeu de citations manga/anime cultes (idempotent)."

    def handle(self, *args, **options):
        created = 0
        for text, text_fr, character, series, theme in QUOTES:
            _, was_created = Quote.objects.get_or_create(
                text=text,
                character=character,
                series=series,
                defaults={
                    "theme": theme,
                    "text_fr": text_fr,
                    "fr_origin": ASSISTED,
                },
            )
            if was_created:
                created += 1

        total = Quote.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"{created} nouvelle(s) citation(s) ajoutée(s), {total} au total.")
        )
