# Snake Game
 
## Intro:
 
Een klassiek Snake spel gemaakt met Python en Pygame.
Beweeg de slang, eet de rode stippen en groei zo lang mogelijk zonder in jezelf te botsen.
Het spel wordt sneller naarmate je meer punten scoort.
 
 
## Hoe kan je installeren
 
Zorg dat je Python hebt geïnstalleerd. Daarna:
 
1. Clone de repository:
```bash
git clone https://github.com/ShihabA02/snake-game.git
cd snake-game
```
 
2. Installeer de benodigde packages:
```bash
pip install pygame
```
Of via requirements.txt:
```bash
pip install -r requirements.txt
```
 
3. Start het spel:
```bash
python snake_game.py
```
 
## Hoe kan je spelen
 
| Pijltje omhoog / W | Omhoog |
| Pijltje omlaag / S | Omlaag |
| Pijltje links / A | Links |
| Pijltje rechts / D | Rechts |
| Spatie / Enter | Start / Opnieuw starten |
 
- Eet de **rode stip** voor +10 punten
- De slang groeit elke keer als je eet
- Botsen in jezelf = game over
- Botsen tegen de muur = game over
- De snelheid neemt toe naarmate je score stijgt
 
## Design
 
Het spel is opgebouwd met polymorphism via een `Unit` basisklasse:
 
- `Unit` — abstracte basisklasse voor alle objecten in het spel
- `SnakeSegment` — erft van `Unit`, stelt een segment van de slang voor
- `Food` — erft van `Unit`, stelt het eten voor
- `SnakeGame` — beheert de game loop, input, update en draw
 
 
## Auteurs
 
- Lina,Sarah,Shihab,Yasmine
 
## License
 
This project is for educational purposes at the Universiteit van Amsterdam.
