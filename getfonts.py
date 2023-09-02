import pygame

fonts = pygame.font.get_fonts()

def main():
    print([f for f in fonts if 'mono' in f])

if __name__ == '__main__':
    main()