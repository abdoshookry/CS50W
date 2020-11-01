
function edit(id) {

    // console.log(content);

    document.getElementById(`for${id}`).style.display = 'block';
    document.getElementById(`${id}`).style.display = 'none';

    document.getElementById(`for${id}`).onsubmit = function (e) {

        e.preventDefault();
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // document.getElementById(`${id}`).innerHTML = document.getElementById('con').value

        fetch(`/edit/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                content: document.getElementById(`con${id}`).value
            })
        })
            .then(response => response.json())
            .then(result => {

                document.getElementById(`for${id}`).style.display = 'none';
                document.getElementById(`${id}`).innerHTML = ``
                document.getElementById(`${id}`).append(document.getElementById(`con${id}`).value)
                document.getElementById(`${id}`).style.display = 'block';
            });

    }

}




document.addEventListener('DOMContentLoaded', function () {

    fetch(`/does_like`, {
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    })
        .then(response => response.json())
        .then(result => {
            // Print emails

            //  console.log(result)

            result.forEach(like => {
                console.log(like.post.id)
                if (document.getElementById(`un/like${like.post.id}`))
                    document.getElementById(`un/like${like.post.id}`).innerHTML = '<i class="fas fa-heart"></i>'
            });
        });
})

function like(id, user) {
    // e.preventDefault();
    // const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(`/like/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            // 'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            user: user
        })

    })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            document.getElementById(`like${id}`).innerHTML = ``
            document.getElementById(`like${id}`).innerHTML = `${result.no_likes} like`

            if (result.exists) {

                document.getElementById(`un/like${id}`).innerHTML = '<i class="fas fa-heart"></i>'
            }
            else {
                document.getElementById(`un/like${id}`).innerHTML = '<i class="far fa-heart"></i>'
            }

        });

}















/*
    document.getElementById(`${id}`).innerHTML =
        `<form id = "for">
            <textarea class="text" id="con"> ${content} </textarea >
    <input type = "submit" value = "save edit">
    </form>`
*/


/*
e.onsubmit = function () {

      fetch(`/edit/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          content: e.getAttribute("textarea")
        })
      });
    }
*/

/*
e = document.getElementById(`${id}`).innerHTML =
`<form action = "{% url 'edit' id %}>
<textarea> ${content} </textarea>
<input type = "submit" value = "save edit">
</form>`
*/


/*
document.addEventListener("DOMContentLoaded", function () {


    try {
        get_posts();
    } catch (err) {
        document.getElementById("posts").innerHTML = err;

    }


});

function get_posts() {

 document.getElementById("posts").innerHTML = `<div> hello </div>`;

    fetch('/posts', {
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    })
        .then(response => response.json())
        .then(posts => {
            // Print emails

            console.log(posts);

            const post = document.createElement('div');
            post.innerHTML = `<div>${posts.user.username} </div>
            <div>${posts.content} </div>
            <div>${posts.timestamp} </div>
            <div>${posts.no_likes} </div>
            <div> hello </div>`
            document.getElementById("posts").append(posts);


        });

}
*/
/*
document.addEventListener("DOMContentLoaded", function () {

    document.querySelector('#all_posts').addEventListener('click', () => load_page('all_posts'));
    document.querySelector('#user_profile').addEventListener('click', () => load_page('profile'));

    load_page("all_posts");
});

function load_page(page) {

    switch (page) {
        case "all_posts":
            document.querySelector('#posts').style.display = 'block';
            document.querySelector('#profile').style.display = 'none';
            break;
        case "profile":
            document.querySelector('#posts').style.display = 'none';
            document.querySelector('#profile').style.display = 'block';
            break;

        //document.querySelector('#emails').style.display = 'block';
        //document.querySelector('#compose-view').style.display = 'none';
    }


}*/
