function starOutGrid(grid) {
    const stars = [];
    for (let i = 0; i < grid.length; i++) {
        for (let x = 0; x < grid[i].length; x++) {
            if (grid[i][x] === '*'){
                stars.push([i, x])
            }
        }
    }
    for (let coords of stars) {
        let i = coords[0];
        for (ind in grid[i]){
            grid[i][ind] = '*';
        }
        let x = coords[1];
        for (row of grid){
            row[x] = '*';
        }
    }
    console.log(grid)
    return grid;
}
