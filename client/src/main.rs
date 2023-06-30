use raylib::prelude::*;

fn main() {
    let (mut rl, thread) = raylib::init()
        .size(800, 800)
        .title("Cards")
        .build();

    let i = Image::load_image("../assets/icon.png").unwrap();
    let t = rl
        .load_texture_from_image(&thread, &i)
        .expect("could not load texture from image");
    
    rl.set_target_fps(60);
    while !rl.window_should_close() {
        let mut d = rl.begin_drawing(&thread);

        d.clear_background(Color::BLACK);
        d.draw_texture(&t, 0, 0, Color::WHITE);
    }
}

