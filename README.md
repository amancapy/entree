# entree
**artificial selection in a gene pool of asexually reproducing trees.**

***EDIT: I'm an idiot and didn't consider that a "tree" class would make everything here 1000x more trivial. but I'm not rewriting the project as it's simple as is***

when I read Dawkins' The Greatest Show On Earth as a kid I found the idea of rudimentary trees mutating and having traits selected for on a computer screen fascinating. fun little weekend project, very rough around the edges but it gets the idea right. crashes occassionally into the 100s of generations, but I just wanted to see if I could implement the concept.

currently all children in a generation are mutated clones of the selected parent, "mimicing" asexual reproduction. Will maybe implement 2-parent reproduction in a future iteration, with recessive and dominant genes.

11/09: mutation function highly unstable, trying to fix sudden explosions.

12/09: mutation now completely stable (i'm not responsible if it still breaks color), added automatic selection for multiple attributes (except color), fixed exploding mutations with a lot of calculations (my laptop will never physically recover from this). oh also it doesn't crash now.

04/11: sexual reproduction implemented with OOP this time as opposed to the incomprehensible dict-list nightmare that was the asexual one, with a somewhat impressive (if i say so myself) reproduction function. 
