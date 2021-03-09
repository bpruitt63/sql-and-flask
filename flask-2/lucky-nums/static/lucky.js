const BASE_URL = 'http://localhost:5000'

/** processForm: get data from form and make AJAX call to our API. */

function processForm(evt) {
    evt.preventDefault();
    clearErrors()
    const name = document.querySelector('#name').value;
    const year = document.querySelector('#year').value;
    const email = document.querySelector('#email').value;
    const color = document.querySelector('#color').value.toLowerCase();
    getResponse(name, year, email, color)
}

async function getResponse(name, year, email, color) {
    const resp = await axios({
        method: "POST",
        url: `${BASE_URL}/api/get-lucky-num`,
        data: {
            "name": name,
            "year": year,
            "email": email,
            "color": color
        }
    })
    handleResponse(resp)
}

/** handleResponse: deal with response from our lucky-num API. */

function handleResponse(resp) {
    if (resp.data.num){
        const num = resp.data.num.num;
        const numFact = resp.data.num.fact;
        const yr = resp.data.year.year;
        const yrFact = resp.data.year.fact;
        const results = document.querySelector('#lucky-results')
        results.innerHTML = `<p>Your lucky number is ${num} (${numFact}).</p>
                            <p>Your birth year (${yr}) fact is ${yrFact}.</p>`
    }
    else {
        console.log(resp.data)
        for (let key in resp.data){
            let x = document.querySelector(`#${key}-err`)
            x.innerText = resp.data[key]
        }
    }
}

/** clearErrors: remove errors from html if user resubmits data, 
 * so error list can be updated accurately */
function clearErrors(){
    const a = document.querySelector('#name-err')
    const b = document.querySelector('#year-err')
    const c = document.querySelector('#email-err')
    const d = document.querySelector('#color-err')
    a.innerText = ''
    b.innerText = ''
    c.innerText = ''
    d.innerText = ''
}

$("#lucky-form").on("submit", processForm);
