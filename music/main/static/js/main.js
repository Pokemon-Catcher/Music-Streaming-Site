likeButton=document.getElementById('like')

function mulberry32(a) {
      var t = a += 0x6D2B79F5;
      t = Math.imul(t ^ t >>> 15, t | 1);
      t ^= t + Math.imul(t ^ t >>> 7, t | 61);
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
}

function like(id,type){
    fetch('/like?' + new URLSearchParams({
        type: type,
        id: id,
    })).then(response =>{
        if(response.status==200){
            response.text().then(text=>{
                likeButton.innerText='👍'+text
                if(likeButton.classList.contains('btn-primary')){
                    likeButton.classList.replace('btn-primary','btn-success')
                } else{
                    likeButton.classList.replace('btn-success','btn-primary')
                }
            })
        }
    })
}
listened={}

function listen(id){
    if(listened[id]) return;
    listened[id]=1
    fetch('/listen?' + new URLSearchParams({
        id: id,
    }))
}

function addToPlaylist(){
    addToPlaylist
}

let noimages=document.querySelectorAll('img[src*=noimage]')

for(let i=0;i<noimages.length;i++){
    noimages[i].style.filter = 'hue-rotate('+360*mulberry32(noimages[i].getAttribute('seed'))+'deg)';
}