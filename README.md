# Выстрой меня, если сможешь!
Добрый день! Мы представляем свой проект-игру под названием "Выстрой меня, если сможешь"!
  
  В данном проекте мы вдохновились игрой тетрис, которая несмотря на свою простоту привлекает внимание даже сегодня. В нашей игре основной целью является выстраивание устойчивой башни, заранее заданной высоты, из падающих случайных фигурок произвольного цвета. Сами объекты являются стандартными фигурками из игры Тетрис.
   
  В самом начале на экране появляется область, в которой необходимо выстроить башню. Игрок может нажимать клавиши D,A для того, чтобы двигать фигурку вправо и влево соответственно в пределах темной области(фигурки двигаются с постоянной скоростью вниз до их столкновения). 
  
  Правила игры следующие: для победы необходимо выстраить башню до желтой линии, но это усложняется тем, что каждая упавшая с башни фигурка отнимает 20 очков от счета игрока(* за каждую правильно выставленную фигурку начисляется 10 очков, на начало игры у нас 100 очков). Также игра усложняется тем, что через 15 секунд после начала игры появляется красная линия, которая поднимается снизу вверх. При пересечении серой и красной линии или обнулении счета игра заканчивается проигрышем. Также в игре имеется музыка (кмузыка включается в случайном порядке), которую можно переключать на стрелку вправо и ставить на паузу на пробел.
  
  Для запуска игры надо скачать библиотеку pygame и игровой движок pymunk. Далее загружаем файлы main.py, Shapes.py и файлы с музыкой. 

  Хорошей игры!
