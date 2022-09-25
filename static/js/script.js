//use code to fetch playlists
//when playlist is chosen, send post request to python

//window.history.pushState("", "", redirect_uri); // remove param from url

const plArea = document.getElementById("playlists");

console.log(playlistItems)

for(let i = 0; i < playlistItems.length; i++) {
  if (playlistItems[i].owner.id === username){

    if(playlistItems[i].images.length > 0){
      plArea.insertAdjacentHTML("beforeend",
                              `
      <div class="playlist" onclick="sendPostForShuffle('${playlistItems[i].id}', '${playlistItems[i].tracks.total}', '${playlistItems[i].name}')">
      <div class="playlistImg" style="background: url(${playlistItems[i].images[0].url}) 50% 50% no-repeat;background-size: cover;"></div>
        <h2 class="playlistName">${playlistItems[i].name}</h2>
      </div>                
    `)
    }
    else{
      plArea.insertAdjacentHTML("beforeend",
                              `
      <div class="playlist" onclick="sendPostForShuffle('${playlistItems[i].id}', '${playlistItems[i].tracks.total}', '${playlistItems[i].name}')">
      <div class="playlistImg" style="background: url('/static/images/blankPlaylist.png') 50% 50% no-repeat;background-size: cover;"></div>
        <h2 class="playlistName">${playlistItems[i].name}</h2>
      </div>                
    `)
    }
  }
}

function sendPostForShuffle(playlistId, playlistLength, playlistName) {

  plArea.style.display = "none";
  document.getElementById("load").style.display = "inline";

  window.location.href = `https://true-spotify-shuffle.brendawg.repl.co/finished?plID=${playlistId}&plLength=${playlistLength}&plName=${playlistName}&refreshToken=${refreshToken}`;
}

//<img class="playlistImg" src="${playlistItems[i].images[0].url}">