class RootScene extends Phaser.Scene {
    preload() {
        this.load.setBaseURL('http://localhost:8000/static/');
        
        this.load.tilemapTiledJSON('map', './assets/background.json');
        this.load.image('ground-tiles-asset', './assets/ground-plains-tileset.png');
        this.load.image('border-tiles-asset', './assets/border-trees-tileset.png');
    }

    create() {
        const map = this.make.tilemap({ key: 'map', tileWidth: 64, tileHeight: 64 });
        const groudTileset = map.addTilesetImage('ground-plains-tileset', 'ground-tiles-asset');
        const borderTileset = map.addTilesetImage('border-trees-tileset', 'border-tiles-asset');
        const groundLayer = map.createLayer("ground", groudTileset, 0, 0);
        const borderLayer = map.createLayer("border", borderTileset, 0, 0);

        this.input.on("wheel",  (pointer, gameObjects, deltaX, deltaY, deltaZ) => {
            let minZoomX = this.cameras.main.width / map.widthInPixels;
            let minZoomY = this.cameras.main.height / map.heightInPixels;
            let minZoom = Math.max(minZoomX, minZoomY);

            if (deltaY > 0) {
                var newZoom = this.cameras.main.zoom - 0.1;
                if (newZoom > minZoom) {
                    this.cameras.main.zoom = newZoom;     
                }
                else {
                    this.cameras.main.zoom = minZoom;
                }
            }
          
            if (deltaY < 0) {
                var newZoom = this.cameras.main.zoom + 0.1;
                if (newZoom < 1) {
                    this.cameras.main.zoom = newZoom;     
                }
                else {
                    this.cameras.main.zoom = 1;
                }
            }
          
          });
    
        this.input.on('pointermove', (pointer) => {
            if (!pointer.isDown) return;
    
            this.cameras.main.scrollX -= (pointer.x - pointer.prevPosition.x) / this.cameras.main.zoom;
            this.cameras.main.scrollY -= (pointer.y - pointer.prevPosition.y) / this.cameras.main.zoom;
        });

        this.cameras.main.setBounds(0, 0, map.widthInPixels, map.heightInPixels);
    }
}

const config = {
    type: Phaser.AUTO,
    width: 1280,
    height: 720,
    scale: {
        mode: Phaser.Scale.ScaleModes.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH
    },
    scene: RootScene,
    physics: {
        default: 'none'
    }
};

const game = new Phaser.Game(config);