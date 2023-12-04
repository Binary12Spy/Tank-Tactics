class Player extends Phaser.Scene {

    username;
    health;
    is_player;
    is_alive;
    action_points;
    range;
    primary_color;
    secondary_color;

    preload() {
        this.load.setBaseURL('http://localhost:8000/static/');

        
    }

    create() {
        
    }
}