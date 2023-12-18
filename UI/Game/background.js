class Background {
    static load(scene, base64string, mapWidth, mapHeight) {
        let ground_vector = Background.base64To2DArray(base64string, mapWidth);
        let border_vector = Background.createBoundaryVector(mapWidth, mapHeight);

        let map = scene.make.tilemap({ width: mapWidth, height: mapHeight, tileWidth: 64, tileHeight: 64 });
        let ground_tileset = map.addTilesetImage('ground-tiles-asset', null, 64, 64, 2, 4);
        let border_tileset = map.addTilesetImage('border-tiles-asset', null, 64, 64, 2, 4);

        let groundLayer = map.createBlankLayer(0, ground_tileset, 0, 0, mapWidth, mapHeight, 64, 64);
        let borderLayer = map.createBlankLayer(1, border_tileset, 0, 0, mapWidth, mapHeight, 64, 64);

        groundLayer.putTilesAt(ground_vector, 0, 0);
        borderLayer.putTilesAt(border_vector, 0, 0);

        return map;
    }

    static base64To2DArray(base64, width) {
        // Step 1: Decode the base64 string to a byte array
        let decodedBytes = Uint8Array.from(atob(base64), c => c.charCodeAt(0));
    
        // Step 2: Convert the byte array to an array of 32-bit integers
        let intArray = [];
        for (let i = 0; i < decodedBytes.length; i += 4) {
            let value = (decodedBytes[i] |
                (decodedBytes[i + 1] << 8) |
                (decodedBytes[i + 2] << 16) |
                (decodedBytes[i + 3] << 24)) >>> 0;
            intArray.push(value);
        }
    
        // Step 3: Split the array into chunks based on the known width
        let result = [];
        for (let i = 0; i < intArray.length; i += width) {
            let chunk = intArray.slice(i, i + width);
            result.push(chunk);
        }
    
        return result;
    }
    
    static createBoundaryVector(width, height) {
        let arr = new Array(height);
    
        for (let i = 0; i < height; i++) {
            arr[i] = new Array(width);
            for (let j = 0; j < width; j++) {
                if (i === 0 && j === 0) arr[i][j] = 0; // top left corner
                else if (i === 0 && j === width - 1) arr[i][j] = 2; // top right corner
                else if (i === height - 1 && j === 0) arr[i][j] = 6; // bottom left corner
                else if (i === height - 1 && j === width - 1) arr[i][j] = 8; // bottom right corner
                else if (i === 0) arr[i][j] = 1; // top edge
                else if (i === height - 1) arr[i][j] = 7; // bottom edge
                else if (j === 0) arr[i][j] = 3; // left edge
                else if (j === width - 1) arr[i][j] = 5; // right edge
                else arr[i][j] = 4; // interior
            }
        }
    
        return arr;
    }
}