import pygame
import math
import random

w = 720
screen = pygame.display.set_mode((w, w))
screen.fill((0, 0, 0))

running = True


# mutate val by up to m_rate%, as long as it's between down and up
def mutate(val, down, up, m_rate=0.03):
    amt_redone = val * m_rate * random.randint(1, 100) / 100
    new_val = random.choice([1, -0.95]) * amt_redone
    if not down < val + new_val < up:
        amt_redone = val * m_rate * random.randint(1, 100) / 100
        new_val = random.choice([1, -0.95]) * amt_redone
        return round(val + new_val, 3)
    elif down < val + new_val:
        return val - new_val
    elif val + new_val < up:
        return val - new_val
    else:
        return val * (1 + random.choice([0.01, -0.0095]))


o = 2  # order of individuals per generation, unstable above 5
# stem width, height, color; n. of branches, branch height, width, length, angle.
pool = [{"s_w": w / o / 30, "s_h": (w / o) / 2, "s_c": (100, 100, 100),
         "b_n_l": 4, "b_n_r": 5, "b_b": w / o / 12, "b_w": w / o / 60, "b_l_l": [w / o / 6], "b_l_r": [w / o / 6],
         "b_a_l": [60 for k in range(3)], "b_a_r": [60 for m in range(3)]} for i in range(o * o)]

gen = 0
while 1:
    if not running:
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            gen += 1
            print("gen", gen)
            # selecting a parent in the present generation
            mx, my = pygame.mouse.get_pos()
            picked = pool[math.floor(my / w * o) * o + math.floor(mx / w * o)]

            # all children are clones of the parent before their genes mutate and they are born (doctors HATE him)
            pool = [{"s_w": picked["s_w"], "s_h": picked["s_h"], "s_c": picked["s_c"],
                     "b_b": picked["b_b"], "b_w": picked["b_w"],

                     "b_n_l": picked["b_n_l"],
                     "b_n_r": picked["b_n_r"],

                     # if there's an increase in number of branches, add new default branch
                     "b_l_l": [
                         (picked["b_l_l"] + [w / o / 6 for k in
                                             range(int(picked["b_n_l"]) - len(picked["b_l_l"]))])[b]
                         for b in range(int(picked["b_n_l"]))],
                     "b_l_r": [
                         (picked["b_l_r"] + [w / o / 6 for k in
                                             range(int(picked["b_n_r"]) - len(picked["b_l_r"]))])[b]
                         for b in range(int(picked["b_n_r"]))],
                     "b_a_l": [
                         (picked["b_a_l"] + [60 for k in range(int(picked["b_n_l"]) - len(picked["b_a_l"]))])[b]
                         for b in range(int(picked["b_n_l"]))],
                     "b_a_r": [
                         (picked["b_a_r"] + [60 for k in range(int(picked["b_n_r"]) - len(picked["b_a_r"]))])[b]
                         for b in range(int(picked["b_n_r"]))]} for i in range(o * o)]

            for i in range(o):
                for j in range(o):
                    rec1 = pygame.Rect(w / o * i + 1, w / o * j + 1, w / o - 2, w / o - 2)
                    pygame.draw.rect(screen, (255, 255, 255), rec1)

                    # mutating the children's genes so they diverge from the parent
                    ctree = pool[i * o + j]
                    s_w = mutate(ctree["s_w"], 7, w / o / 2)
                    s_h = mutate(ctree["s_h"], 10, (w / o) / 1.5)
                    s_c = (abs(mutate(ctree["s_c"][0], 1, 250, 0.1) % 255),
                           abs(mutate(ctree["s_c"][1], 1, 250, 0.1) % 255),
                           abs(mutate(ctree["s_c"][2], 0, 250, 0.1) % 255))
                    b_b = mutate(ctree["b_b"], 10, s_h / 2)
                    b_w = mutate(ctree["b_w"], 5, ctree["s_w"] - 2)
                    b_n_l = mutate(ctree["b_n_l"], 1, 6)
                    b_n_r = mutate(ctree["b_n_r"], 1, 6)
                    b_l_l = [mutate(b, 5, w / o / 3) for b in ctree["b_l_l"][:int(b_n_l)]]
                    b_l_r = [mutate(b, 5, w / o / 3) for b in ctree["b_l_r"][:int(b_n_r)]]
                    b_a_l = [mutate(a, 45, 75) for a in ctree["b_a_l"][:int(b_n_l)]]
                    b_a_r = [mutate(a, 45, 75) for a in ctree["b_a_r"][:int(b_n_r)]]
                    b_c = (abs(mutate(ctree["s_c"][0], 1, 250, 0.1) % 255),
                           abs(mutate(ctree["s_c"][1], 1, 250, 0.1) % 255),
                           abs(mutate(ctree["s_c"][2], 1, 250, 0.1) % 255))

                    # convenient that assigning a dict references the original instead of copying it
                    ctree.update({"s_w": s_w, "s_h": s_h, "s_c": s_c,
                                  "b_n_l": b_n_l, "b_n_r": b_n_r, "b_b": b_b, "b_w": b_w,
                                  "b_l_l": b_l_l, "b_l_r": b_l_r, "b_a_l": b_a_l, "b_a_r": b_a_r})

                    # stem
                    base = (w / o * i + w / o / 2, w / o * j + w / o / 2 + w / o / 3)
                    tip = (w / o * i + w / o / 2, w / o * j + w / o / 2 + w / o / 3 - s_h)
                    stem = pygame.draw.line(screen, s_c, base, tip, width=int(s_w))

                    # branches
                    # gap is not inherited since it's due to "environmental" factors (I am lazy)
                    # left
                    for k in range(len(b_l_l)):
                        gap = (s_h - b_b) / int(b_n_l)
                        b_base = (base[0] - s_w / 2 + 1, base[1] - b_b - k * mutate(gap * 0.98, gap * 0.99, gap))
                        # reduce branch length by a factor of 0.2 the higher up it is
                        b_tip = (b_base[0] - (b_l_l[k] - k * 0.2 * b_l_l[k]) * math.sin(math.radians(b_a_l[k])),
                                 b_base[1] - (b_l_l[k] - k * 0.2 * b_l_l[k]) * math.cos(math.radians(b_a_l[k])))
                        branch = pygame.draw.line(screen, b_c, b_base, b_tip, width=int(b_w))

                    # right
                    for k in range(len(b_l_r)):
                        gap = (s_h - b_b) / int(b_n_r)
                        b_base = (base[0] + s_w / 2 + 1, base[1] - b_b - k * mutate(gap * 0.98, gap * 0.99, gap))
                        # reduce branch length by a factor of 0.2 the higher up it is
                        b_tip = (b_base[0] + (b_l_r[k] - k * 0.2 * b_l_r[k]) * math.sin(math.radians(b_a_r[k])),
                                 b_base[1] - (b_l_r[k] - k * 0.2 * b_l_r[k]) * math.cos(math.radians(b_a_r[k])))
                        branch = pygame.draw.line(screen, b_c, b_base, b_tip, width=int(b_w))

            pygame.display.flip()
