using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using Menus;

namespace Game1 {


    public class Game1 : Game {
        GraphicsDeviceManager graphics;
        SpriteBatch spriteBatch;

        public bool running = true;

        Vector2 resolution = new Vector2(1200, 800);
        Camera camera;
        SpriteFont[] fonts;

        public MenuHandler menuHandler;
        

        public Game1() {
            graphics = new GraphicsDeviceManager(this);
            Content.RootDirectory = "Content";

            // Set resolution of window
            graphics.PreferredBackBufferWidth = (int)resolution.X;
            graphics.PreferredBackBufferHeight = (int)resolution.Y;
            graphics.ApplyChanges();
        }

        protected override void Initialize() {
            // TODO: Add your initialization logic here

            this.IsMouseVisible = true;

            base.Initialize();
        }


        protected override void LoadContent() {
            // Create a new SpriteBatch, which can be used to draw textures.
            spriteBatch = new SpriteBatch(GraphicsDevice);

            // TODO: use this.Content to load your game content here
            // Load fonts
            fonts = new SpriteFont[5];
            fonts[0] = Content.Load<SpriteFont>("font1");
            fonts[1] = Content.Load<SpriteFont>("font2");
            fonts[2] = Content.Load<SpriteFont>("font3");
            fonts[3] = Content.Load<SpriteFont>("font4");
            fonts[4] = Content.Load<SpriteFont>("font5");
            // Init camera
            camera = new Camera(this.resolution, new Vector2(0, 0), 0);

            // Init menus and handler
            menuHandler = new MenuHandler(fonts, camera);
            Events.ButtonEvents.game1 = this;
        }


        protected override void UnloadContent() {
            // TODO: Unload any non ContentManager content here
        }


        protected override void Update(GameTime gameTime) {
            if (GamePad.GetState(PlayerIndex.One).Buttons.Back == ButtonState.Pressed || Keyboard.GetState().IsKeyDown(Keys.Escape))
                Exit();

            if (running == false) {
                this.Exit();
                base.Update(gameTime);
                return;
            }

            if (menuHandler.update() == true) {
                // Menu was updated (game is paused)
            }


            base.Update(gameTime);
        }


        protected override void Draw(GameTime gameTime) {
            GraphicsDevice.Clear(Color.Black);

            // TODO: Add your drawing code here
            spriteBatch.Begin();

            if (menuHandler.render(spriteBatch) == true) {
                // Menu rendered, do not display game
            }

            spriteBatch.End();

            base.Draw(gameTime);
        }
    }
}
