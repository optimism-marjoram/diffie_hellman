#
# Author: Aaron Wilson <cardiff@noraa.uk>
#

from manim import *

DEFAULT_FONT=32
TEXT_DROP = 0.75
TEXT_UP = 1

# I have yet to work out how to make the colours
# so this works in practice ... patches welcome !
PUBLIC_COLOUR = YELLOW
SECRET_COLOUR_A = '#ff5a00'
MIX_COLOUR_A = '#ffbf61'
SECRET_COLOUR_B = '#5dcac5'
MIX_COLOUR_B = '#93bbff'
KEY_COLOUR = '#796300'

# Positioning
TITLE_Y = 3
TITLE_X = 5

CHOICES_Y = 2
CHOICES_X = 5

PUBLIC_INFO_Y = 0.5
PUBLIC_INFO_X = 1.5

PRIVATE_X = -3.5
PRIVATE_Y = -1

KEY_Y = -2
KEY_X = 4.5
KEY_VERTICES = 8

class DiffieHellmanKeyExchange(Scene):

    show_text = False

    def _character_intro(self, name, direction):

        name_mid = MarkupText(
                f"<span font_size='small'>{name}</span>")

        name= MarkupText(
                f"<span font_size='small'>{name}</span>")
        name.set_y(TITLE_Y)
        name.set_x((TITLE_X*direction)[0])

        self.play(FadeIn(name_mid))
        self.play(Transform(name_mid,name))

    def character_list(self):

        for person in self.characters:
            self._character_intro(person['name'], person['direction'])

        # Eve is special ...
        self._character_intro('Public Information', np.array((0,0,0)))

        return

    def public_first_choice(self, animate=True):

        #common = Dot(color=YELLOW, fill_color=YELLOW, radius=0.5)
        common = RegularPolygon(n=3, color=YELLOW, radius=0.5)
        common.set_fill(YELLOW, opacity=1)
        common.set_y(CHOICES_Y)
        if animate:
            self.play(FadeIn(common), run_time=2)
            if self.show_text:
               public_label = Tex("modulus $p = 23$, base $g=5$", font_size=DEFAULT_FONT)
               centre = common.get_center()
               public_label.set_x(centre[0])
               public_label.set_y(centre[1]-TEXT_DROP)

               self.add(public_label)
        else:
            self.add(common)

        return common

    def _pick_secret(self, vertices, colour, direction):
        #person_secret = Dot(color=colour, fill_color=colour, radius=0.5)
        person_secret = RegularPolygon(n=vertices, color=colour, radius=0.5)
        person_secret.set_fill(colour, opacity=1)
        person_secret.set_y(CHOICES_Y)
        person_secret.set_x((CHOICES_X*direction)[0])

        return person_secret

    def pick_secrets(self):

        secrets = VGroup()

        for person in self.characters:
            person_secret = self._pick_secret(person['vertices'], person['secret'], person['direction'])
            if self.show_text:
                label = Tex(f"Secret ${person['explabel']} = {person['exp']}$",
                            font_size=DEFAULT_FONT)
                centre = person_secret.get_center()
                label.set_x(centre[0])
                label.set_y(centre[1]-TEXT_DROP)
                secrets.add(label)

            secrets.add(person_secret)

        self.play(FadeIn(secrets), run_time=2)
        self.wait(1)

    def mix_public_secret(self):

        for index in range(0, len(self.characters)):
            person = self.characters[index]

            common = self.public_first_choice()
            character = self._pick_secret(person['vertices'],
                                          person['secret'],
                                          person['direction'])

            group = VGroup(common, character)

            #public_info = Dot(color=person['mix_colour'],
            #              fill_color=person['mix_colour'],radius=0.5)
            public_info = RegularPolygon(n=person['mix_vertices'],
                              color=person['mix_colour'], radius=0.5)
            public_info.set_fill(person['mix_colour'], opacity=1)
            public_info.set_y(PUBLIC_INFO_Y)
            public_info.set_x((PUBLIC_INFO_X*person['direction'])[0])

            if self.show_text:
                label = Tex(f"$g^{person['explabel']} \mod 23$",
                            font_size=DEFAULT_FONT)
                centre = public_info.get_center()
                label.set_x(centre[0])
                label.set_y(centre[1]-TEXT_DROP)

                plabel = Tex(f"${person['sval']}$ mod $23$", font_size=DEFAULT_FONT)
                plabel.set_x(centre[0])
                plabel.set_y(centre[1]-TEXT_DROP)

            self.play(Transform(group, public_info), run_time=5)
            if self.show_text:
                self.add(label)
                self.wait(1)
                self.play(Transform(label, plabel), run_time=1)

            copy = group.copy()
            centre_point = copy.get_center()
            centre_point[0] = PRIVATE_X * (person['direction'])[0]
            centre_point[1] = PRIVATE_Y
            path = Line(copy.get_center(), centre_point)
            self.play(MoveAlongPath(copy, path))

            # This is cheating alot
            if index == 0:
                self.characters[1]['public'] = copy
            elif index == 1:
                self.characters[0]['public'] = copy
            else:
                raise ValueError('Unexpected size of characters array')

        self.wait(1)

    def generate_key(self):

        for index in range(0, len(self.characters)):
            person = self.characters[index]
            # This is cheating alot
            if index == 0 or index == 1:
                other = 1-index
            else:
                raise ValueError('Unexpected size of characters array')

            # Clone secret value
            secret = self._pick_secret(person['vertices'], person['secret'], person['direction'])
            secret.set_y(PRIVATE_Y)

            # Clone public value
            public_info = person['public']

            self.play(FadeIn(secret))

            group = VGroup(secret, public_info)

            #key_obj = Dot(color=KEY_COLOUR, fill_color=KEY_COLOUR, radius=0.5)
            key_obj = RegularPolygon(n=KEY_VERTICES, color=KEY_COLOUR, radius=0.5)
            key_obj.set_fill(KEY_COLOUR, opacity=1)
            key_obj.set_y(KEY_Y)
            key_obj.set_x((KEY_X*person['direction'])[0])

            self.play(Transform(group, key_obj), run_time=2)

            if self.show_text:
                labelkey = Tex("$g^{ab} = (g^a)^b = (g^b)^a \mod 23$", font_size=DEFAULT_FONT)
                centre = public_info.get_center()
                labelkey.set_x(centre[0])
                labelkey.set_y(centre[1]+TEXT_UP)

                self.add(labelkey)
                self.wait(2)

                public_val = self.characters[other]['sval']
                other_exp = self.characters[other]['explabel']
                label_text = f"$(g^{other_exp})^{person['explabel']} = " \
                         f"({public_val})^{person['explabel']} = " \
                         f"({public_val})^{person['exp']} \mod 23$"
                calc_a_label = Tex(label_text, font_size=DEFAULT_FONT)
                calc_a_label.set_x(centre[0])
                calc_a_label.set_y(centre[1]+TEXT_UP)

                self.remove(labelkey)
                self.add(calc_a_label)
                self.wait(2)

                # Yes, this value should not be hard coded. I am a bad person
                keyvalue = Tex(f"$({public_val})^{person['exp']} = 18 \mod 23$",
                    font_size=DEFAULT_FONT)
                keyvalue.set_x(centre[0])
                keyvalue.set_y(centre[1]+TEXT_UP)

                self.remove(calc_a_label)
                self.add(keyvalue)
                self.wait(1)

    def construct(self):
        # Set up some class variables
        self.public_colour = PUBLIC_COLOUR
        self.public_prime = 23
        self.public_root = 4

        self.characters = []

        self.characters.append({})
        self.characters[0]['name'] = 'Alice'
        self.characters[0]['secret'] = SECRET_COLOUR_A
        self.characters[0]['mix_colour'] = MIX_COLOUR_A
        self.characters[0]['mix_vertices'] = 6
        self.characters[0]['direction'] = LEFT
        self.characters[0]['exp'] = 4
        self.characters[0]['explabel'] = 'a'
        self.characters[0]['sval'] = 4
        self.characters[0]['vertices'] = 4

        self.characters.append({})
        self.characters[1]['name'] = 'Bob'
        self.characters[1]['secret'] = SECRET_COLOUR_B
        self.characters[1]['mix_colour'] = MIX_COLOUR_B
        self.characters[1]['mix_vertices'] = 7
        self.characters[1]['direction'] = RIGHT
        self.characters[1]['exp'] = 3
        self.characters[1]['explabel'] = 'b'
        self.characters[1]['sval'] = 10
        self.characters[1]['vertices'] = 5

        self.character_list()

        self.public_first_choice()

        self.pick_secrets()

        self.mix_public_secret()

        self.generate_key()

class DiffieHellmanKeyExchangeText(DiffieHellmanKeyExchange):


    def construct(self):
        self.show_text = True
        # Set up some class variables
        super().construct()
