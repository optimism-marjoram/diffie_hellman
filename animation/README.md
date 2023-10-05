# README

This is a python script using manim to produce animantions.

Details on Manim are at https://www.manim.community/

I compiled this in a python3.11 virutal environment via:

   manim -pql colour_shape_maths.py <Scene>

There are two scenes:
 - DiffieHellmanKeyExchange uses the colours and shapes only
 - DiffieHellmanKeyExchangeText has text following and example

## Notes

This is far from perfect code, so only copy as a bad example.

Note: on my ageing Mac I had to add the file:

    cat  lib/python3.11/site-packages/cairo.pth
    /usr/local/Cellar/py3cairo/1.24.0/lib/python3.11/site-packages

to my virutal environment to make it work

## Bugs

I would really like the colours to be additive here (so public + private == real colours)
