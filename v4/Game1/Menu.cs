using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using Game1;


namespace Menus {

    class Menu {

        MenuText[] menuText;


        public Menu (MenuText[] menuText) {
            this.menuText = menuText;
        }

        public void render(SpriteBatch spriteBatch, Camera camera) {
            // Render menu text items
            for (int i = 0; i < this.menuText.Length; i++) {
                this.menuText[i].render(spriteBatch);
            }
        }

        public void update() {

        }
    }

    class MenuText {

        public SpriteFont font;
        public string text;
        public Vector2 pos;
        public Color color;

        public MenuText(SpriteFont font, string text, Vector2 pos, Color color) {
            // Find the center point of the text and set the new position so the text is rendered centered on the given position
            this.font = font;
            this.text = text;
            Vector2 size = font.MeasureString(text);
            Vector2 centerPos = new Vector2(pos.X - size.X / 2, pos.Y - size.Y / 2);
            this.pos = centerPos;
            this.color = color;
        }

        public void render(SpriteBatch spriteBatch) {
            // Render the given text
            spriteBatch.DrawString(this.font, this.text, this.pos, this.color);
        }
    }

    class MenuGenerator {

        SpriteFont[] fonts;

        public MenuGenerator(SpriteFont[] fonts) {
            this.fonts = fonts;
        }

        public Menu mainMenu(Camera camera) {
            Vector2 titleSplashPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 3);
            MenuText titleSplash = new MenuText(this.fonts[4], "Solaris", titleSplashPos, Color.White);

            MenuText[] menuText = new MenuText[1];
            menuText[0] = titleSplash;
            Menu mainMenu = new Menu(menuText);
            return mainMenu;
        }
    }
}
