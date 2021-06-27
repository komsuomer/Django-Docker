const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function like(e) {
    var xhr = new XMLHttpRequest();
    let postID = e.target.getAttribute("value");
    xhr.open('POST', "/like/" + postID + '/');
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (xhr.status === 200) {
            var responseInfo = JSON.parse(xhr.responseText);
            if (responseInfo.like) {
                e.target.innerHTML = 'Unlike';
                document.getElementById('like_count'+postID).innerHTML = (parseInt(document.getElementById('like_count'+postID).getAttribute('value')) + 1).toString() + ' likes';
                document.getElementById('like_count'+postID).setAttribute('value', (parseInt(document.getElementById('like_count'+postID).getAttribute('value')) + 1).toString());
            } else if (responseInfo.unlike) {
                e.target.innerHTML = 'Like';
                document.getElementById('like_count'+postID).innerHTML = (parseInt(document.getElementById('like_count'+postID).getAttribute('value')) - 1).toString() + ' likes';
                document.getElementById('like_count'+postID).setAttribute('value', parseInt(document.getElementById('like_count'+postID).getAttribute('value')) - 1);
            }
        } else {
            alert('Bad request');
        }

    };
    xhr.send("method=" + (e.target.innerHTML == 'Like' ? 'like' : 'unlike'));
}