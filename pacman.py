import math, kandinsky, ion, time, random

wecran = 320
hecran = 222
wmap = 15
hmap = 10
wcase = 21
hcase = 21
fond = kandinsky.color(0, 0, 0)
violet = kandinsky.color(80, 0, 255)
jaune = kandinsky.color(255, 225, 0)
blanc = kandinsky.color(255, 255, 255)
noir = kandinsky.color(0, 0, 0)
rouge = kandinsky.color(255, 0, 0)
rose = kandinsky.color(255, 159, 159)
cyan = kandinsky.color(0, 220, 255)
orange = kandinsky.color(255, 125, 0)
beige = kandinsky.color(255, 230, 200)
eligne = 2
emur = 4 #2 minimum
gauche = ion.KEY_LEFT
droite = ion.KEY_RIGHT
haut = ion.KEY_UP
bas = ion.KEY_DOWN
ok = ion.KEY_OK
back = ion.KEY_BACK
dire = 1 #1=droite, 2=bas, 3=gauche, 4=haut
px = 100
py = 100

ghosts = [ # x, y, objectifx, objectify initiaux
  [7 * wcase + int(wecran/2 - wmap * 10) - 7, 4 * hcase + int(hecran/2 - hmap * 10) - 2, 7 * wcase + int(wecran/2 - wmap * 10) - 7, 4 * hcase + int(hecran/2 - hmap * 10) - 2, 0],
  [7 * wcase + int(wecran/2 - wmap * 10) - 7, 4 * hcase + int(hecran/2 - hmap * 10) - 2, 7 * wcase + int(wecran/2 - wmap * 10) - 7, 4 * hcase + int(hecran/2 - hmap * 10) - 2, 0],
  [8 * wcase + int(wecran/2 - wmap * 10) - 7, 5 * hcase + int(hecran/2 - hmap * 10) - 2, 8 * wcase + int(wecran/2 - wmap * 10) - 7, 5 * hcase + int(hecran/2 - hmap * 10) - 2, 0],
  [7 * wcase + int(wecran/2 - wmap * 10) - 7, 5 * hcase + int(hecran/2 - hmap * 10) - 2, 7 * wcase + int(wecran/2 - wmap * 10) - 7, 5 * hcase + int(hecran/2 - hmap * 10) - 2, 0]
]

map = [
  ["v", "v", "v", "gho", "bh", "hd", "gbdv", "gd", "gbdv", "gh", "bh", "hdo", "v", "v", "v"],
  ["v", "v", "v", "gd", "gh", "d", "gh", "b", "hd", "g", "hd", "gd", "v", "v", "v"],
  ["gh", "bh", "bh", "", "db", "gd", "g", "hb", "d", "gd", "gb", "", "h", "h", "hd"],
  ["gd", "h", "hdb", "g", "hd", "g", "b", "hb", "b", "d", "gh", "d", "ghb", "hd", "d"],
  ["gb", "", "h", "bd", "b", "d", "gvp", "vp", "dvp", "g", "bd", "gb", "h", "", "bd"],
  ["gh", "d", "g", "hb", "hb", "d", "gbv", "bv", "bdv", "g", "hb", "hb", "d", "g", "hd"],
  ["gd", "gd", "gd", "gh", "hb", "", "hb", "hbc", "hb", "", "hb", "hd", "gd", "gd", "gd"],
  ["gd", "gd", "gbdo", "gd", "gh", "b", "hb", "hb", "hb", "b", "hd", "gd", "gbdo", "gd", "gd"],
  ["g", "b", "h", "b", "b", "h", "hb", "h", "hb", "h", "b", "b", "h", "b", "d"],
  ["gb", "hb", "b", "hb", "hb", "b", "ghdv", "gd", "ghdv", "b", "hb", "hb", "b", "hb", "bd"]
]

def rect(x, y, w, h, e, c, cfond):
  kandinsky.fill_rect(x, y, w, h, c)
  kandinsky.fill_rect(x + e, y + e, w - 2 * e, h - 2 * e, cfond)

def case(x, y, type): #types : g, h, d, b, o, c
  xc = x + 5
  yc = y + 6
  xb = x + 8
  yb = y + 7
  xb2 = x + 10
  yb2 = y + 9
  cerise = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 2, 2, 2, 1, 0, 0, 0, 1, 0, 0, 0],
    [2, 2, 2, 1, 2, 2, 0, 1, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 0, 2, 1, 2, 2, 0, 0],
    [2, 3, 2, 2, 0, 2, 2, 1, 2, 2, 2, 0],
    [2, 2, 3, 2, 0, 2, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 0, 2, 3, 2, 2, 2, 2, 0],
    [0, 0, 0, 0, 0, 2, 2, 3, 2, 2, 2, 0],
    [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0]
  ]
  boule = [
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0]
  ]
  bille = [
    [0, 1, 1, 0],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [0, 1, 1, 0]
  ]
  if "o" in type:
    for num_ligne, ligne in enumerate(boule):
      for num_pixel, pixel in enumerate(ligne):
        if pixel == 1:
          kandinsky.set_pixel(xb+num_pixel, yb+num_ligne, jaune)
  if "c" in type:
    for num_ligne, ligne in enumerate(cerise):
      for num_pixel, pixel in enumerate(ligne):
        if pixel == 1:
          kandinsky.set_pixel(xc+num_pixel, yc+num_ligne, beige)
        elif pixel == 2:
          kandinsky.set_pixel(xc+num_pixel, yc+num_ligne, rouge)
        elif pixel == 3:
          kandinsky.set_pixel(xc+num_pixel, yc+num_ligne, blanc)
  if not "o" in type and not "c" in type and not "v" in type:
    for num_ligne, ligne in enumerate(bille):
      for num_pixel, pixel in enumerate(ligne):
        if pixel == 1:
          kandinsky.set_pixel(xb2+num_pixel, yb2+num_ligne, jaune)
  if "g" in type:
    kandinsky.fill_rect(x, y, int(emur/2), hcase, violet)
  if "h" in type:
    kandinsky.fill_rect(x, y, wcase + 2, int(emur/2), violet)
  elif "p" in type:
    kandinsky.fill_rect(x, y, wcase + 2, int(emur/2), rose)
  if "d" in type:
    kandinsky.fill_rect(x + wcase, y, int(emur/2), hcase, violet)
  if "b" in type:
    kandinsky.fill_rect(x, y + hcase, wcase + 2, int(emur/2), violet)

def draw_map():
  global wcase
  global hcase
  global px
  global py
  global map
  for num_ligne, ligne in enumerate(map):
    for num_pixel, pixel in enumerate(ligne):
      case(num_pixel * wcase, num_ligne * hcase + 6, pixel)
  px = 7 * wcase + int(wecran/2 - wmap * 10) - 7
  py = 7 * hcase + int(hecran/2 - hmap * 10) - 2

pobjectifx = 7 * wcase + int(wecran/2 - wmap * 10) - 7
pobjectify = 7 * hcase + int(hecran/2 - hmap * 10) - 2

def init():
  kandinsky.fill_rect(0, 0, wecran, hecran, fond)
  draw_map()

def bordure(px, py, perso): #perso : 1 = Pacman, 2 = ghost
  marge = 2
  rang = 17
  resultat = [0, 0, 0, 0]
  if perso == 1:
    for i in range(px - marge, px + rang):
      if kandinsky.get_pixel(i, py - marge) == violet or kandinsky.get_pixel(i, py - marge) == rose:
        resultat[0] = resultat[0] + 1
    for i in range(py - marge, py + rang):
      if kandinsky.get_pixel(px + rang, i) == violet or kandinsky.get_pixel(px + rang, i) == rose:
        resultat[1] = resultat[1] + 1
    for i in range(px - marge, px + rang):
      if kandinsky.get_pixel(i, py + rang) == violet or kandinsky.get_pixel(i, py + rang) == rose:
        resultat[2] = resultat[2] + 1
    for i in range(py - marge, py + rang):
      if kandinsky.get_pixel(px - marge, i) == violet or kandinsky.get_pixel(px - marge, i) == rose:
        resultat[3] = resultat[3] + 1
  elif perso == 2:  
    for i in range(px - marge, px + rang):
      if kandinsky.get_pixel(i, py - marge) == violet:
        resultat[0] = resultat[0] + 1
    for i in range(py - marge, py + rang):
      if kandinsky.get_pixel(px + rang, i) == violet:
        resultat[1] = resultat[1] + 1
    for i in range(px - marge, px + rang):
      if kandinsky.get_pixel(i, py + rang) == violet:
        resultat[2] = resultat[2] + 1
    for i in range(py - marge, py + rang):
      if kandinsky.get_pixel(px - marge, i) == violet:
        resultat[3] = resultat[3] + 1
  
  return resultat

def ghost(x, y, couleur):
  ghost = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 0, 0],
    [0, 0, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 0, 0],
    [0, 0, 1, 2, 2, 3, 3, 1, 1, 2, 2, 3, 3, 1, 0, 0],
    [0, 1, 1, 1, 2, 3, 3, 1, 1, 1, 2, 3, 3, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ]
  for num_ligne, ligne in enumerate(ghost):
    for num_pixel, pixel in enumerate(ligne):
      if pixel == 0:
        kandinsky.set_pixel(x + num_pixel, y + num_ligne, fond)
      elif pixel == 1:
        kandinsky.set_pixel(x + num_pixel, y + num_ligne, couleur)
      elif pixel == 2:
        kandinsky.set_pixel(x + num_pixel, y + num_ligne, blanc)
      elif pixel == 3:
        kandinsky.set_pixel(x + num_pixel, y + num_ligne, noir)

def pacman(x, y, ori, ouverture):
  pcm_ferme = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ]
  pcm_ouvert_droite = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ]
  pcm_ouvert_bas = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ]
  pcm_ouvert_gauche = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ]
  pcm_ouvert_haut = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ]
  if ouverture == 1:
    if ori == 1:#vers la droite
      for num_ligne, ligne in enumerate(pcm_ouvert_droite):
        for num_pixel, pixel in enumerate(ligne):
          if pixel == 1:
            kandinsky.set_pixel(x+num_pixel, y+num_ligne, jaune)
          elif pixel == 0:
            kandinsky.set_pixel(x+num_pixel, y+num_ligne, fond)
    elif ori == 2:#vers le bas
      for num_ligne, ligne in enumerate(pcm_ouvert_bas):
        for num_pixel, pixel in enumerate(ligne):
          if pixel == 1:
            kandinsky.set_pixel(x+num_pixel, y+num_ligne, jaune)
          elif pixel == 0:
            kandinsky.set_pixel(x+num_pixel, y+num_ligne, fond)
    elif ori == 3:#vers la gauche
      for num_ligne, ligne in enumerate(pcm_ouvert_gauche):
        for num_pixel, pixel in enumerate(ligne):
          if pixel == 1:
            kandinsky.set_pixel(x+num_pixel, y+num_ligne, jaune)
          elif pixel == 0:
            kandinsky.set_pixel(x+num_pixel, y+num_ligne, fond)
    elif ori == 4:#vers le haut
      for num_ligne, ligne in enumerate(pcm_ouvert_haut):
        for num_pixel, pixel in enumerate(ligne):
          if pixel == 1:
            kandinsky.set_pixel(x+num_pixel, y+num_ligne, jaune)
          elif pixel == 0:
            kandinsky.set_pixel(x+num_pixel, y+num_ligne, fond)
  elif ouverture == 0:
    for num_ligne, ligne in enumerate(pcm_ferme):
        for num_pixel, pixel in enumerate(ligne):
          if pixel == 1:
            kandinsky.set_pixel(x+num_pixel, y+num_ligne, jaune)
          elif pixel == 0:
            kandinsky.set_pixel(x+num_pixel, y+num_ligne, fond)

def objectif_pacman(x, y):
  global pobjectifx
  global pobjectify
  global hcase
  global wcase
  global px
  global py
  casx = math.floor(px / wcase)
  casy = math.floor(py / hcase)
  case = map[casy][casx]
  if pobjectify == y:
    if ion.keydown(droite) and not bordure(px, py, 1)[1] >= 2 and pobjectifx == x:
      pobjectifx = x + wcase
    elif ion.keydown(gauche) and not bordure(px, py, 1)[3] >= 2 and pobjectifx == x:
      pobjectifx = x - wcase
  if pobjectifx == x:
    if ion.keydown(haut) and not bordure(px, py, 1)[0] >= 2 and pobjectify == y:
      pobjectify = y - hcase
    elif ion.keydown(bas) and not bordure(px, py, 1)[2] >= 2 and pobjectify == y and not "b" in case:
      pobjectify = y + hcase

def objectif_ghost(x, y, num_ghost):
  global ghosts
  casx = math.floor(ghosts[num_ghost][0] / wcase)
  casy = math.floor(ghosts[num_ghost][1] / hcase)
  case = map[casy][casx]
  casxobj = math.floor(ghosts[num_ghost][2] / wcase)
  casyobj = math.floor(ghosts[num_ghost][3] / wcase)
  caseobj = map[casyobj][casxobj]
  if ghosts[num_ghost][2] == ghosts[num_ghost][0] and ghosts[num_ghost][3] == ghosts[num_ghost][1]:
    ghosts[num_ghost][4] = random.randint(1, 4)

  if "p" in case and not bordure(x, y, 2)[0] >= 2 and ghosts[num_ghost][3] == ghosts[num_ghost][1]:
    ghosts[num_ghost][3] = y - hcase
        
  if ghosts[num_ghost][2] == ghosts[num_ghost][0]:
    if ghosts[num_ghost][4] == 1 and not "h" in case and not bordure(x, y, 2)[0] >= 2 and not bordure(ghosts[num_ghost][2], ghosts[num_ghost][3], 2)[0] >= 2:
        ghosts[num_ghost][3] = y - hcase
    elif ghosts[num_ghost][4] == 3 and not "b" in case and not bordure(x, y, 2)[2] >= 2 and not bordure(ghosts[num_ghost][2], ghosts[num_ghost][3], 2)[2] >= 2:
        ghosts[num_ghost][3] = y + hcase

  if ghosts[num_ghost][3] == ghosts[num_ghost][1]:
    if ghosts[num_ghost][4] == 2 and not "d" in case and not bordure(x, y, 2)[1] >= 2 and not bordure(ghosts[num_ghost][2], ghosts[num_ghost][3], 2)[1] >= 2:
        ghosts[num_ghost][2] = x + wcase
    elif ghosts[num_ghost][4] == 4 and not "g" in case and not bordure(x, y, 2)[3] >= 2 and not bordure(ghosts[num_ghost][2], ghosts[num_ghost][3], 2)[3] >= 2: 
        ghosts[num_ghost][2] = x - wcase
  #kandinsky.fill_rect(ghosts[num_ghost][2] - 1, ghosts[num_ghost][3] - 1, 3, 3, cyan)

def mouv_pacman(ouverture):
  global px
  global py
  global dire
  objectif_pacman(px, py)
  if pobjectifx < px and not bordure(px, py, 1)[3] >= 2:
    px = px - 1
    dire = 3
  elif pobjectifx > px and not bordure(px, py, 1)[1] >= 2:
    px = px + 1
    dire = 1
  
  if pobjectify < py and not bordure(px, py, 1)[2] >= 2:
    py = py - 1
    dire = 4
  elif pobjectify > py: #and not bordure(px, py, 1)[0] >= 2:
    py = py + 1
    dire = 2

  pacman(px, py, dire, ouverture)

def mouv_ghost(num_ghost, comp):
  global ghosts
  #comportement aleatoire tah Jean :
  if comp == 1: #si le ghost est comportement aleatoire
    
    objectif_ghost(ghosts[num_ghost][0], ghosts[num_ghost][1], num_ghost)
    if ghosts[num_ghost][2] < ghosts[num_ghost][0]:
      ghosts[num_ghost][0] = ghosts[num_ghost][0] - 1
    elif ghosts[num_ghost][2] > ghosts[num_ghost][0]:
      ghosts[num_ghost][0] = ghosts[num_ghost][0] + 1
    elif ghosts[num_ghost][3] < ghosts[num_ghost][1]:
      ghosts[num_ghost][1] = ghosts[num_ghost][1] - 1
    elif ghosts[num_ghost][3] > ghosts[num_ghost][1]:
      ghosts[num_ghost][1] = ghosts[num_ghost][1] + 1

init()
acc = 0
ouvert = True

while True:
  pastouche = pobjectifx == px and pobjectify == py
  if acc < 10:
    acc = acc + 1
  else:
    acc = 0
    ouvert = not ouvert
  if pastouche:
    mouv_pacman(1)
  else:
    mouv_pacman(ouvert)
  
  for i in range(0, 4):
    mouv_ghost(i, 1)
    if i == 0:
      col = rouge
    elif i == 1:
      col = rose
    elif i == 2:
      col = orange
    elif i == 3:
      col = cyan
    ghost(ghosts[i][0], ghosts[i][1], col)
  time.sleep(0.02)