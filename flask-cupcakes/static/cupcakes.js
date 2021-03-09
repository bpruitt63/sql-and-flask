const BASE_URL = 'http://localhost:5000/'

document.addEventListener('load', showCupcakes());

document.addEventListener('submit', function(e) {
    e.preventDefault(); 
    const flavor = document.querySelector('#flavor').value;
    const size = document.querySelector('#size').value;
    const rating = document.querySelector('#rating').value;
    const image = document.querySelector('#image').value;
    addCupcake(flavor, size, rating, image)
});

async function showCupcakes(){
    const res = await axios.get(`${BASE_URL}/api/cupcakes`)
    const cupcakes = res.data.cupcakes
    const list = document.querySelector('#list');
    for (let i = 0; i < cupcakes.length; i++){
        let li = document.createElement('li');
        li.innerText = cupcakes[i].flavor;
        list.append(li);
    }
}

async function addCupcake(flavor, size, rating, image){
    const res = await axios({
        method: "POST",
        url: `${BASE_URL}/api/cupcakes`,
        data: {
            'flavor': flavor,
            'size': size,
            'rating': rating,
            'image': image
        }
    })
    const newFlav = res.data.cupcake.flavor;
    listAppend(newFlav);
}

function listAppend(newFlav){
    const list = document.querySelector('#list');
    const li = document.createElement('li');
    li.innerText = newFlav;
    list.append(li);
}