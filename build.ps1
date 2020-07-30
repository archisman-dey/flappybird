pyinstaller `
--noconfirm `
--clean `
--onefile `
--name "Flappy Bird" `
--add-data "resources/background.png;resources" `
--add-data "resources/piller_down.png;resources" `
--add-data "resources/piller_up.png;resources" `
--add-data "resources/bird.png;resources" `
--add-data "resources/game_over.png;resources" `
--windowed `
--icon ".\icon.ico" `
.\main.py