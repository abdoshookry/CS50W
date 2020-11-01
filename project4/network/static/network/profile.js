
//document.addEventListener('DOMContentLoaded', function () {

fetch(`/does_follow/${document.getElementById('id').textContent}`, {
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
})
    .then(response => response.json())
    .then(result => {
        // Print emails
        if (document.getElementById('un/follow')) {
            if (result.is_following.length === 0)
                document.getElementById('un/follow').innerHTML = 'follow'
            else
                document.getElementById('un/follow').innerHTML = 'unfollow'
        }

    });
//})


function follow(id, user) {
    //   document.getElementById(`form`).onsubmit = function (e) {
    // e.preventDefault();
    //const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]');
    //const csrftoken =document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    // var token = '{{csrf_token}}';
    fetch(`/follow/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            //  'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            user: user
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result);

            document.getElementById('followers').innerHTML = ''
            document.getElementById('followers').innerHTML = `${result.no_followers.length}`
            if (result.is_following.length === 0)
                document.getElementById('un/follow').innerHTML = 'follow'
            else
                document.getElementById('un/follow').innerHTML = 'unfollow'

        });
    // }
}
